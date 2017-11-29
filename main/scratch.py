import matplotlib.pyplot as plt
import scipy.signal as sig
import collections
import wave
import time
import pyaudio
import scipy.io.wavfile as sciwave
import numpy as np
from Audio import Audio


f = 'Music/beat.wav'
audio = Audio(f)
audio.getBeats()


data0 = audio.fluxBins[:,0]
hist0 = audio.fluxAvgs[:,0]
delta0 = audio.deltaFlux[:,0]
beats0 = audio.beats[:,0]
data1 = audio.fluxBins[:, 1]
data2 = audio.fluxBins[:, 2]
data3 = audio.fluxBins[:, 3]
data4 = audio.fluxBins[:, 4]

# Use Savitzky-Golay filter to smoothen values
# wLen is the length of the window the filter uses
# polyOrder is the order of the polynomial the filter uses
numOfWindowsMinusOne = 5
wLen = data0.size//numOfWindowsMinusOne-1 # must be odd
polyOrder = 3

# apply the filter for smoothness
#newData1 = sig.savgol_filter(data, wLen, polyOrder)

# apply the filter again for silky smoothness
#newData2 = sig.savgol_filter(newData1, wLen, polyOrder)

# Plot to compare 
fig, ax0 = plt.subplots()
#fig, (ax0, ax1, ax2, ax3, ax4) = plt.subplots(5)

ax0.plot(data0, '-')
ax0.plot(hist0, '-')
#ax0.plot(delta0, '-')
ax0.plot(beats0, '--')
#ax1.plot(data1, '-')
#ax2.plot(data2, '-')
#ax3.plot(data3, '-')
#ax4.plot(data4, '-')

plt.show()