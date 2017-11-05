# Naren Bhandari
# 15-112 Term Project

import numpy as np
import matplotlib.pyplot as plt
# import scipy
# import pydub
from pydub import AudioSegment

def openMP3(path):
    # gets mp3 data from pydub
    # returns np array of samples averaged over the channels
    # and the frame rate
    song = AudioSegment.from_mp3(path)
    samples = song.get_array_of_samples()
    # samples are serialized like [l0, r0, l1, r1, l2, r2, ...]
    # split into two axes of np array
    audio = np.array([samples[::2], samples[1::2]])
    # take average of samples over the two channels
    audio = np.mean(audio, axis=0)
    return audio, song.frame_rate

def plotWaveform(audio, rate):
    f, ax = plt.subplots()
    N = audio.shape[0]
    ax.plot(np.arange(N) / rate, audio)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude')
    plt.show()

def main():
    # make sure pydub finds avconv - its finicky
    converterPath = "C:\\libav-i686-w64-mingw32-11.7\\usr\\bin\\avconv"
    AudioSegment.converter = converterPath
    # choose song
    songPath = "01 - Ties That Bind.mp3"
    audio, rate = openMP3(songPath)
    plotWaveform(audio, rate)
    
main()
