import matplotlib.pyplot as plt
import wavStuff
import scipy.signal as sig
import numpy as np

rate, audio = wavStuff.sciOpen(wavStuff.f)

data = audio[int(audio.size/2048)] #first chunk of data

# Use Savitzky-Golay filter to smoothen values
# wLen is the length of the window the filter uses
# polyOrder is the order of the polynomial the filter uses
numOfWindowsMinusOne = 5
wLen = data.size//numOfWindowsMinusOne-1 # must be odd
polyOrder = 3

# apply the filter for smoothness
newData1 = sig.savgol_filter(data, wLen, polyOrder)

# apply the filter again for silky smoothness
newData2 = sig.savgol_filter(newData1, wLen, polyOrder)

# Plot to compare 
fig, (ax1, ax2, ax3) = plt.subplots(3)

ax1.plot(data, '-')
ax2.plot(newData1, '-')
ax3.plot(newData2, '-')

plt.show()