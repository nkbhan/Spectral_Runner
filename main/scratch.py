import matplotlib.pyplot as plt
import scipy.signal as sig
import collections
import wave
import time
import pyaudio
import scipy.io.wavfile as sciwave
import numpy as np
from Audio import Audio


f = 'Music/Blank Banshee - Teen Pregnancy.wav'
audio = Audio(f)
audio.getBeats()

#data0 = audio.fluxBins[:,i]
#hist0 = audio.fluxAvgs[:,i]
#delta0 = audio.deltaFlux[:,i]
beats0 = audio.beats[:,0]
#data1 = audio.fluxBins[:, 1]
beats1 = audio.beats[:,1]
#data2 = audio.fluxBins[:, 2]
beats2 = audio.beats[:,2]
#data3 = audio.fluxBins[:, 3]
beats3 = audio.beats[:,3]
#data4 = audio.fluxBins[:, 4]
beats4 = audio.beats[:,4]

# Plot to compare 
f#ig, ax0 = plt.subplots()
fig, (ax0, ax2, ax4) = plt.subplots(3)

#ax0.plot(data0, '-')
#ax0.plot(hist0, '-')
#ax0.plot(delta0, '-')
ax0.plot(beats0, '-')
#ax1.plot(data1, '-')
#ax1.plot(beats1, '-')
ax2.plot(beats2, '-')
#ax2.plot(data2, '-')
#ax3.plot(beats3, '-')
#ax3.plot(data3, '-')
#ax4.plot(data4, '-')
ax4.plot(beats4, '-')

plt.show()