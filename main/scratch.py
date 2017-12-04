import matplotlib.pyplot as plt
import scipy.signal as sig
import collections
import wave
import time
import pyaudio
import scipy.io.wavfile as sciwave
import numpy as np
from Audio import Audio


# f = 'Music/MF DOOM feat RZA  - Books of War.wav'
f = 'Music/Blank Banshee - Teen Pregnancy.wav'
audio = Audio(f)
audio.getBeats()

data0 = audio.fluxBins[:,0]
hist0 = audio.fluxAvgs[:,0]
#delta0 = audio.deltaFlux[:,i]
beats0 = audio.beats[:,0]

data1 = audio.fluxBins[:, 1]
hist1 = audio.fluxAvgs[:,1]
beats1 = audio.beats[:,1]

data2 = audio.fluxBins[:, 2]
hist2 = audio.fluxAvgs[:,2]
beats2 = audio.beats[:,2]

data3 = audio.fluxBins[:, 3]
hist3 = audio.fluxAvgs[:, 3]
beats3 = audio.beats[:,3]

data4 = audio.fluxBins[:, 4]
hist4 = audio.fluxAvgs[:, 4]
beats4 = audio.beats[:,4]


data5 = audio.fluxBins[:, 5]
hist5 = audio.fluxAvgs[:, 5]
beats5 = audio.beats[:,5]

data6 = audio.fluxBins[:, 6]
hist6 = audio.fluxAvgs[:, 6]
beats6 = audio.beats[:,6]

data7 = audio.fluxBins[:, 7]
hist7 = audio.fluxAvgs[:, 7]
beats7 = audio.beats[:,7]

data8 = audio.fluxBins[:, 8]
hist8 = audio.fluxAvgs[:, 8]
beats8= audio.beats[:,8]

data9 = audio.fluxBins[:, 9]
hist9 = audio.fluxAvgs[:, 9]
beats9 = audio.beats[:,9]

# Plot to compare 
f#ig, ax0 = plt.subplots()
fig, (ax0, ax2, ax4) = plt.subplots(3)
fig2, (ax20, ax22, ax24) = plt.subplots(3)

ax0.plot(data1, '-')
ax0.plot(hist1, '-')
#ax0.plot(delta0, '-')
ax20.plot(beats1, '-')

ax2.plot(data5, '-')
ax2.plot(hist5, '-')
ax22.plot(beats5, '-'
)
#ax2.plot(data2, '-')
#ax3.plot(beats3, '-')
#ax3.plot(data3, '-')
ax4.plot(data9, '-')
ax4.plot(hist9, '-')
ax24.plot(beats9, '-')

plt.show()