import collections
import wave
import time
import pyaudio
import scipy.io.wavfile as sciwave
import numpy as np


class Audio(object):
    CHUNK = 1024
    FREQS = np.array([22.5, 100, 500, 2000, 4000, 22050])
    THRESHOLD = 1.5
    def __init__(self, f):
        self.file = f
        self.rate, self.samples = self.getSamples()
        if self.isStereo():
            self.toMono()
        self.numChunks = int(np.ceil(self.samples.size/self.CHUNK))
        self.shape = (self.numChunks, self.CHUNK)
        self.samples.resize(self.shape)
        self.window = np.hamming(self.CHUNK)
        # self.spectrum = self.fftOfSamples()
        self.fftFreqs = np.fft.rfftfreq(self.CHUNK, 1/self.rate)[1:]
        self.historySize = (self.rate//self.CHUNK)//(4)
        self.energies = np.zeros((len(self.FREQS)-1,))
        self.energyHistories = [collections.deque(maxlen=self.historySize)\
                                for i in range(len(self.FREQS)-1)]
        self.avgEnergies = np.zeros((len(self.FREQS)-1,))
        self.fluxBins = np.zeros((self.numChunks, len(self.FREQS)-1))
        self.fluxAvgs = np.zeros((self.numChunks, len(self.FREQS)-1))
        self.onsets = np.zeros((len(self.FREQS)-1,), dtype=int)

    def getSamples(self):
        rate, data = sciwave.read(self.file)
        return rate, data

    def isStereo(self):
        return self.samples[0].shape == (2,)

    def toMono(self):
        self.samples = np.mean(self.samples, axis=1)
        self.samples = self.samples.astype(np.dtype("int16"), copy=False)

    def fftAtChunk(self, index):
        return np.fft.rfft(self.samples[index]*self.window, n=self.CHUNK)[1:]

    def fftOfSamples(self):
        spectrum = np.zeros((self.numChunks, self.CHUNK//2), dtype=complex)
        for i in range(self.numChunks):
            spectrum[i] = self.fftAtChunk(i)
        return np.abs(spectrum)

    def freqToIndex(self, freq):
        return (freq*self.CHUNK/self.rate)

    def getFreqIndeces(self):
        return np.round((self.FREQS*self.CHUNK/self.rate))

    def getSpectralFlux(self):
        # flux = np.zeros((self.numChunks, self.CHUNK//2))
        fluxBins = np.zeros((self.numChunks, len(self.FREQS)-1))
        lastSpectrum = np.zeros((self.CHUNK//2,))
        curSpectrum = np.zeros((self.CHUNK//2,))
        numOfBins = len(self.FREQS) - 1
        for curChunk in range(self.numChunks):
            lastSpectrum = curSpectrum
            curSpectrum = np.abs(self.fftAtChunk(curChunk))
            diff = curSpectrum - lastSpectrum
            isNeg = (diff < 0) # only care about positive flux - onset of beat
            diff[isNeg] = 0 # set negative values to 0
            for i in range(len(diff)):
                freq = self.fftFreqs[i]
                for j in range(numOfBins):
                    if freq > self.FREQS[j] and freq <= self.FREQS[j+1]:
                        fluxBins[curChunk][j] += diff[i]
                        break 
            # flux[curChunk] = diff
        # self.flux = flux
        self.fluxBins = fluxBins

    def getFluxAvgs(self):
        for curChunk in range(self.numChunks):
            start = max(0, curChunk - self.historySize)
            end = min(self.numChunks - 1, curChunk + self.historySize)
            for binIndex in range(len(self.fluxBins[0])):
                self.fluxAvgs[curChunk][binIndex] = \
                    self.THRESHOLD*np.mean(self.fluxBins[start:end, binIndex])

    def getInstantFluxMinusAvgFlux(self):
        deltaFlux = self.fluxBins - self.fluxAvgs
        neg = deltaFlux < 0
        deltaFlux[neg] = 0
        self.deltaFlux = deltaFlux

    def findBeatsInFlux(self):
        self.beats = np.zeros(self.deltaFlux.shape)
        for binIndex in range(len(self.deltaFlux[0])):
            for chunk in range(len(self.deltaFlux[:, binIndex])-1):
                if (self.deltaFlux[chunk][binIndex] >
                    self.deltaFlux[chunk+1][binIndex]):
                    self.beats[chunk][binIndex] = self.deltaFlux[chunk][binIndex]

    def getBeats(self):
        self.getSpectralFlux()
        self.getFluxAvgs()
        self.getInstantFluxMinusAvgFlux()
        self.findBeatsInFlux()

    def energiesAtChunk(self, index):
        numOfBands = len(self.FREQS)-1
        data = self.spectrum[index]
        counters = [0]*numOfBands
        energies = np.zeros((numOfBands,))
        for i in range(len(data)):
            freq = self.fftFreqs[i]
            for j in range(numOfBands):
                if freq > self.FREQS[j] and freq <= self.FREQS[j+1]:
                    energies[j] += data[i]
                    counters[j] += 1
        for i in range(numOfBands):
            energies[i] /= counters[i]
            self.energyHistories[i].append(energies[i])
        self.energies = energies

    def getAvgEnergyHistory(self):
        numOfBands = len(self.FREQS)-1
        for i in range(numOfBands):
            self.avgEnergies[i] = sum(self.energyHistories[i])/self.historySize

def main():
    f = 'Music/The SeatBelts - Tank.wav'
    audio = Audio(f)
    audio.getBeats()
    # for i in range(256):
    #     print(i)
    #     audio.energiesAtChunk(i)
    #     energies = audio.energies
    #     audio.getAvgEnergyHistory()
    #     for j, k in enumerate(energies):
    #         print(j, k, audio.avgEnergies[j])
    #         time.sleep(.07)

if __name__ == "__main__":
    main()