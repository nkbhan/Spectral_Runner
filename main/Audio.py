"""
Audio.py

contains the class for the song and beat detection that goes on.
A wav file is taken and spectral flux onset analysis is done to locate beats
and stored in pickle file so that repeatted analysis doesn't have to be done
if the game is shut and reopened.
"""

import collections
import pickle
import os
import pygame
import Player
import scipy.io.wavfile as sciwave
import scipy.signal as sig
import numpy as np
from Colors import *

class Audio(object):
    CHUNK = 1024
    FREQS = np.array([22.5, 63, 125, 250, 500, 1000, 2000, 4000, 8000, 16000, 22050])
    #                   0    1   2    3    4   5      6      7    8      9      10
    THRESHOLD = 2
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
        self.spectrum = np.abs(spectrum)

    def freqToIndex(self, freq):
        return freq*self.CHUNK/self.rate

    def getFreqIndeces(self):
        return np.round((self.FREQS*self.CHUNK/self.rate))

    def getSpectralFlux(self):
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
        self.fluxBins = fluxBins

    def getFluxAvgs(self):
        for curChunk in range(self.numChunks):
            start = max(0, curChunk - self.historySize)
            end = min(self.numChunks - 1, curChunk + self.historySize)
            for binIndex in range(len(self.fluxBins[0])):
                self.fluxAvgs[curChunk][binIndex] = \
                    self.THRESHOLD*np.mean(self.fluxBins[start:end, binIndex])
        for binIndex in range(len(self.fluxBins[0])):
            self.fluxAvgs[:, binIndex] += np.max(self.fluxAvgs[:, binIndex])/10

    def rectifySpectralFlux(self):
        neg = self.fluxBins < 0 #find locations where values are negative
        self.fluxBins[neg] = 0 #set those values equal to 0

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
        if self.beatsDataExists():
            self.loadBeatsData()
        else:
            self.getSpectralFlux()
            self.rectifySpectralFlux()
            self.getFluxAvgs()
            self.getInstantFluxMinusAvgFlux()
            self.findBeatsInFlux()
            self.saveBeatsData()

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
            self.avgEnergies[i] = \
                sum(self.energyHistories[i])/self.historySize

    def getCurrentIndex(self, time):
        # time in ms so convert to sec
        index = int(np.round(time/1000*self.rate/self.CHUNK))
        return index

    def isBeat(self, index):
        numOfBands = len(self.FREQS) - 1
        if  index >= self.samples.shape[0]:
            return [0]*numOfBands
        return self.beats[index, :]

    def getName(self):
        return self.file[6:-4]
        
    def getDataFileName(self):
        return 'Data/' + self.getName() + '.pkl'

    def saveBeatsData(self):
        data = (self.samples, self.fluxBins, self.fluxAvgs,
                self.deltaFlux, self.beats)
        dataFileName = self.getDataFileName()
        with open(dataFileName, 'wb') as pickleFile:
            pickle.dump(data, pickleFile)

    def loadBeatsData(self):
        dataFileName = self.getDataFileName()
        with open(dataFileName, 'rb') as pickleFile:
            data = pickle.load(pickleFile)
        self.samples, self.fluxBins, self.fluxAvgs, self.deltaFlux, self.beats = data

    def beatsDataExists(self):
        return os.path.isfile(self.getDataFileName())

    def drawWaveform(self, screen, data,):
        x1 = data.width/6
        x2 = data.width*5/6
        XRange = np.linspace(x1, x2, self.CHUNK)
        if 0 < data.curIndex < self.samples.shape[0]:
            scale = 500

            # Use Savitzky-Golay filter to smoothen values
            # wLen is the length of the window the filter uses
            # polyOrder is the order of the polynomial the filter uses
            numOfWindowsMinusOne = 15
            wLen = self.CHUNK//numOfWindowsMinusOne-1 # must be odd
            polyOrder = 3


            samples = -self.samples[data.curIndex]/scale
            samples *= self.window        
            samples = sig.savgol_filter(samples, wLen, polyOrder)
            samples = sig.savgol_filter(samples, wLen, polyOrder)
            samples += Player.Player.y
            pointList = [(XRange[i], samples[i]) for i in range(self.CHUNK)]
            
            pygame.draw.lines(screen, Colors.magenta, False, pointList, 2)
        else:
            pointList = [(XRange[i], Player.Player.y) for i in range(self.CHUNK)]
            pygame.draw.lines(screen, Colors.magenta, False, pointList, 2)
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