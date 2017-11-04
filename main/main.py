# Naren Bhandari
# 15-112 Term Project

import numpy as np
import matplotlib.pyplot as plt
# import scipy
# import pydub
from pydub import AudioSegment

def openMP3(path):
    song = AudioSegment.from_mp3(path)
    return song

def main():
    AudioSegment.converter = "C:\\libav-i686-w64-mingw32-11.7\\usr\\bin\\avconv"    
    song = openMP3("01 - Ties That Bind.mp3")
    print(song.channels, song.sample_width, song.frame_rate, song.frame_width)
    samples = song.get_array_of_samples()
    audio = np.array([samples[::2], samples[1::2]])
    audio = np.mean(audio, axis=0)
    print(audio.size)
    N = audio.shape[0]
    print(N)
    L = N/song.frame_rate
    print('Audio length: %.2f seconds'%L)

    f, ax = plt.subplots()
    ax.plot(np.arange(N) / song.frame_rate, audio)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Amplitude [unknown]')

main()
