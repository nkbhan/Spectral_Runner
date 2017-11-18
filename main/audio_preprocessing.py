# Naren Bhandari
# 15-112 Term Project

import numpy as np
import matplotlib.pyplot as plt
import scipy
# import pydub
from pydub import AudioSegment
from scipy.fftpack import rfft

def openMP3(path):
    # gets mp3 data from pydub
    # returns np array of samples averaged over the channels
    # and the frame rate
    song = AudioSegment.from_mp3(path)
    channels = song.split_to_mono()
    left = channels[0]
    right = channels[1]
    leftSamples = left.get_array_of_samples()
    rightSamples = right.get_array_of_samples()
    # split into two axes of np array
    audio = np.array([leftSamples, rightSamples])
    # take average of samples over the two channels
    audio = np.mean(audio, axis=0)
    numOfSecs = int(np.ceil(audio.size/song.frame_rate))
    numOfFramesIn16MS = song.frame_count(ms=16)
    print(numOfSecs, numOfFramesIn16MS)
    return audio, song.frame_rate

def plotWaveform(audio, rate):
    # chunk = 2*1024
    f, ax = plt.subplots()
    N = audio.shape[0]
    ax.plot(np.arange(N) / rate, audio)
    # ax.plot(np.arange(chunk), audio[:chunk])
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude')
    plt.show()

def plotSpectrum(audio, rate):
    N = 2
    chunk = N * 1024

    xfft = np.linspace(0, rate, chunk)
    # use real fast fourier transform since input is real
    # to improve effeicncy and return smaller array
    spectrum = rfft(audio, axis=0)
    # the spectrum is ordered like [0, 1,2,3,-4,-3,-2,-1]

    # no need to do this anymore, center specrtume like [-4,-3,-2,-1,0,1,2,3]
    # spectrum = scipy.fftpack.fftshift(spectrum)
    
    # plt.loglog(xfft, np.abs(spectrum)[0*chunk:1*chunk])
    plt.loglog(xfft, spectrum[0*chunk:1*chunk])
    plt.show()

def transformChunk(audio, chunk, index):
    # use real fast fourier transform since input is real
    # to improve effeicncy and return smaller array
    spectrum = rfft(audio[index*chunk:(index+1)*chunk], axis=0)
    # spectrums indeces correspond to the follwonig frequency values
    xfft = scipy.fftpack.rfftfreq(chunk)
    return xfft, spectrum

def plotSpectrumChunk(x, y):
    print(x)
    print(y)
    f, ax = plt.subplots()
    ax.set_xlabel("Frequency")
    ax.set_ylabel("Magnitude")
    plt.plot(x, np.abs(y))
    plt.show()

def plotSpectrumOverTime(audio, rate):
    chunk = 1024
    # http://bastibe.de/2013-05-30-speeding-up-matplotlib.html
    fig, ax = plt.subplots()
    x = np.linspace(0, rate, chunk)
    line, = ax.plot(x, np.random.randn(chunk))
    plt.ion()
    num_plots = 0
    for i in range(int(np.ceil(audio.size/chunk))):

        line.set_ydata(np.abs(rfft(audio[i*chunk:(i+1)*chunk], n=chunk)))
        fig.canvas.draw()
        fig.canvas.flush_events()
        num_plots += 1
    # plt.show()
    print(num_plots)

def main(songPath="Music/05. Luna.mp3"):
    # make sure pydub finds avconv - its finicky
    converterPath = "C:\\libav-i686-w64-mingw32-11.7\\usr\\bin\\avconv"
    AudioSegment.converter = converterPath
    # choose song
    audio, rate = openMP3(songPath)
    print(audio.size, audio.shape, rate)

    # resize to break up into chunks
    chunk = 1024
    numOfChunks = int(np.ceil(audio.size/chunk))
    shape = (numOfChunks, 1, chunk)
    audio.resize(shape)    
    # print(audio.size, audio.shape)
    # print(audio)

    spectrum = rfft(audio, n=1024)
    spectrum = np.abs(spectrum)
    # print(spectrum.size, spectrum.shape)
    return np.log1p(spectrum, where=True)
    # plotSpectrumOverTime(audio, rate)


    # index = 3
    # chunk = 1024
    # x, specChunk = transformChunk(audio, chunk, index)
    # print()
    # achunk = audio[index*chunk:chunk*(index+1)]
    # print(achunk, achunk.size)
    # plotSpectrumChunk(x, specChunk)


    # plotWaveform(audio, rate)
    # plotSpectrum(audio, rate)
    # plotSpectrum(np.sin(2*np.arange(0, 2*2*1024, 2)), 44100)
    # _, (ax1, ax2) = plt.subplots(2)

    # y1 = np.abs(scipy.fftpack.fftshift(fft(np.sin(2*np.arange(0, 2*2*1024, 2)))))
    # y2 = np.sin(np.linspace(0, 100,1000))

    # x1 = np.arange(-y1.shape[0]/2, y1.shape[0]/2)
    # x2 = 0

    # ax1.semilogy(x1, y1)
    # ax2.plot(y2)
    # plt.show()

if __name__ == "__main__":
    main()