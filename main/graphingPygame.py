import collections
import sys
import pygame
import wavStuff
from Colors import Colors
import numpy as np
import scipy.signal as sig
import scipy.fftpack as fftpack


###############################################
# init song
###############################################

# constants
CHUNK = 1024
RATE = 44100
NUMCHUNKSPERSECOND = (RATE//CHUNK)
HISTORYBUFFERSIZE = NUMCHUNKSPERSECOND//4
NUMFREQSUBBANDS = 32
BEATDETECTIONTHRESHOLD = 1.5
VARIANCELIMIT = 1.5e-3

#open song
rate, audio = wavStuff.sciOpen(wavStuff.f, chunk=CHUNK)
# take log(audio + 1)
# The +1 handles the log(0) case
# maniuplate signs to avoid logs of negatve numbers
signs = np.sign(audio)
logAudio = np.fabs(audio)
logAudio = np.log1p(logAudio)/np.log(1.2)
logAudio *= signs
numOfChunks = audio.size/CHUNK

###############################################
# init pygame
###############################################

pygame.mixer.pre_init(frequency=rate, size=-16, channels=1, buffer=CHUNK)
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
size = width, height = 1000, 600
fps = round(rate/CHUNK)

bg = Colors.black
teal = Colors.blue
yellow = Colors.pink

screen = pygame.display.set_mode(size)

###############################################
# init waveform data
###############################################

def remap(n, oldMin, oldMax, newMin, newMax):
    # add test for dOld == 0
    dOld = oldMax - oldMin
    dNew = newMax - newMin
    return (((n - oldMin) * dNew) / dOld) + newMin

numPoints = len(audio[0])
print(numPoints)
waveFormX1 = width/6
waveFormX2 = width*5/6
waveFormXRange = np.linspace(waveFormX1, waveFormX2, numPoints)
spectrumXRange = np.linspace(waveFormX1, waveFormX2, numPoints//2)

barsXRANGE = np.linspace(waveFormX1, waveFormX2, CHUNK/NUMFREQSUBBANDS)

waveFormY = height/2
data = -logAudio[0]

# Use Savitzky-Golay filter to smoothen values
# wLen is the length of the window the filter uses
# polyOrder is the order of the polynomial the filter uses
numOfWindowsMinusOne = 5
wLen = data.size//numOfWindowsMinusOne-1 # must be odd
polyOrder = 3

data = sig.savgol_filter(data, wLen, polyOrder)
data = sig.savgol_filter(data, wLen, polyOrder)

# data += waveFormY

pointList = [(waveFormX1, waveFormY), (waveFormX2, waveFormY)]

###############################################
# init beat detection 
###############################################

# we have a fft spectrum of size CHUNK = 1024
# to get energy, take magnitude of fftData
# divide into NUMFREQSUBBANDS = 32

# since the rate is 44100 Hz,
# the frequency resolution f_res is rate/chunk = 43 roughly,
# so the max frequncy f_max = f_res*chunk/2 = 22050,
# which is what we expect since this is also rate/2,
# so each frequency subband will get f_max/NUMFREQBANDS = 690 Hz roughly
# worth of the frequncy space.

# TO DO: log scale frequency subband width to match hearing...

#initialize array of fft energy subbands
energySubBands = np.zeros(shape=(NUMFREQSUBBANDS))
energySubBandsVariance = np.zeros(shape=(NUMFREQSUBBANDS))

# initialize fft of zeroth chunk of samples
fftData = fftpack.rfft(audio[0], n=CHUNK)
fftData = np.abs(fftData)
fftEnergy = np.abs(fftData)
fftEnergy.resize((NUMFREQSUBBANDS, CHUNK//NUMFREQSUBBANDS))
for i in range(NUMFREQSUBBANDS):
    energySubBands[i] = (NUMFREQSUBBANDS/CHUNK) * np.sum(fftEnergy[i])


# each subband has a hostory buffer going back a second or roughly 43 chunks
# = list of 32 deques/queues of max length 43
energySubBandsHistory = [collections.deque(maxlen=HISTORYBUFFERSIZE)\
                         for i in range(NUMFREQSUBBANDS)]

# use history to calculate avg energy over the history
avgEnergySubBands = np.zeros(shape=(NUMFREQSUBBANDS))
for i in range(NUMFREQSUBBANDS):
    avgEnergySubBands[i] = sum(energySubBandsHistory[i])/HISTORYBUFFERSIZE

beatsPerSubBand = np.zeros(shape=(NUMFREQSUBBANDS), dtype=int)

###############################################
# run pygame
###############################################

#play actual song, not cut up version
# woo = pygame.mixer.Sound(file="Music/beat.wav")
# woo.play()

index = 0
running = True
bassText = font.render("bass", True, pygame.Color('white'))
bassTextOn = False
bassTextCounter = 0
bassTextLimit = 10

while running:
    time = clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    
    screen.fill(bg)

    if index < numOfChunks:

        # play song chunk
        audioToPlay = pygame.mixer.Sound(audio[index])
        audioToPlay.play()

        # waveform data
        # take log (and multiply by -1 so that up and down are match pygames)
        # filter and center
        data = -audio[index]/200
        data = sig.savgol_filter(data, wLen, polyOrder)
        data = sig.savgol_filter(data, wLen, polyOrder)
        data += waveFormY
        pointList = [(waveFormXRange[i], data[i]) for i in range(numPoints)]

        # fft spectrum data, using hamming window on each chunk of audio data
        # to lessen freuqncy spectrum ripples.
        # values are complex so take magnitude
        # move the graph down
        fftData = np.fft.rfft(audio[index]*np.hamming(len(audio[index])), n=CHUNK)

        # throw away first frequency since it does not correspond
        # to any particular frequency but is like the avg of all 
        # frequncies and will throw off beat detection due to size.
        fftData = np.abs(fftData)[1:] 

        fftEnergy = fftData # get energy values before data is modified
        # fftData = -np.log1p(fftData/1000)*50
        fftData = -fftData/6000
        # print((wLen//4))
        # fftData = sig.savgol_filter(fftData, int(wLen//16)+1, polyOrder+3)
        # fftData = sig.savgol_filter(fftData, wLen, polyOrder)
        # fftData = sig.savgol_filter(fftData, wLen, polyOrder)
        fftData += height*.9
        # print(fftData.shape)
        fftPointList = [(spectrumXRange[i], fftData[i]) for i in range(fftData.size-1)]

        # beat detection
        if np.max(fftEnergy) != 0:
            fftEnergy = fftEnergy/np.max(fftEnergy)
        fftEnergy.resize((NUMFREQSUBBANDS, (CHUNK//NUMFREQSUBBANDS)//2))
        for i in range(NUMFREQSUBBANDS):
            # get energy for each frequency subband
            energySubBands[i] = (NUMFREQSUBBANDS/CHUNK) * np.sum(fftEnergy[i])
            # get avg energy of past second
            avgEnergySubBands[i] = sum(energySubBandsHistory[i])/HISTORYBUFFERSIZE

            # variance is a second check of whether there is a beat
            # if there is a high variance, then there is probably a beat
            var = 0
            for j in range(len(energySubBandsHistory[i])):
                var += (energySubBandsHistory[i][j]-avgEnergySubBands[i])**2
            energySubBandsVariance[i] = var/HISTORYBUFFERSIZE

            # if current energy > threshold * avgEnergy,
            # we have beat in the subband
            if (energySubBands[i] > BEATDETECTIONTHRESHOLD*avgEnergySubBands[i]
                or energySubBandsVariance[i] > VARIANCELIMIT):
                beatsPerSubBand[i] += 1
            
            # put new energy into appropriate history buffer,
            # buffer is a queue, so first in, first out when we try
            # to add beyond the max length
            energySubBandsHistory[i].append(energySubBands[i])

        # was graphing twice as much frequency by including imaginary values
        # left most bar is avg energy, not energy of 0 frequency

        #plot energy bars
        barsBottomPoints = [(barsXRANGE[i], height*.9) for i in range(CHUNK//NUMFREQSUBBANDS)]
        barsTopPoints = [(barsXRANGE[i], height*.9-energySubBands[i]*1000) for i in range(CHUNK//NUMFREQSUBBANDS)]

        if index%NUMCHUNKSPERSECOND == 0:
        #     print(energySubBands)
            print(index/NUMCHUNKSPERSECOND, beatsPerSubBand[0],
                  energySubBands[0], avgEnergySubBands[0],
                  energySubBandsVariance[0], VARIANCELIMIT)

        # if (energySubBands[0] > BEATDETECTIONTHRESHOLD*avgEnergySubBands[0] and
        #     energySubBandsVariance[0] > VARIANCELIMIT):
        #     if index > 200:
        #         print(index/NUMCHUNKSPERSECOND, beatsPerSubBand[0],
        #           energySubBands[0], avgEnergySubBands[0],
        #           energySubBandsVariance[0], VARIANCELIMIT)

        # draw waveform
        pygame.draw.lines(screen, teal, False, pointList, 2)
        # draw spectrum
        pygame.draw.lines(screen, yellow, False, fftPointList, 2)
        # draw bars
        for i in range(CHUNK//NUMFREQSUBBANDS):
            pygame.draw.line(screen, Colors.green, barsBottomPoints[i],
                             barsTopPoints[i], 10)

        index += 1
    else: 
        pygame.draw.line(screen, teal, (waveFormX1, waveFormY), (waveFormX2, waveFormY))

    fpsActual = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fpsActual, (50, 50))

    if (energySubBands[0] > BEATDETECTIONTHRESHOLD*avgEnergySubBands[0] or
        energySubBandsVariance[0] > VARIANCELIMIT):
        bassTextOn = True
    
    if bassTextOn:
        screen.blit(bassText, (width/2, height/4))
        bassTextCounter += 1
    
    if bassTextCounter >= bassTextLimit:
        bassTextOn = False
        bassTextCounter = 0

    pygame.display.flip()
