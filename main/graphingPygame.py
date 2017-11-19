import collections
import sys
import pygame
import wavStuff
import numpy as np
import scipy.signal as sig
import scipy.fftpack as fftpack


###############################################
# init song
###############################################

# constants
CHUNK = 1024
RATE = 44100
NUMCHUNKSPERSECOND = (RATE//CHUNK)//2
NUMFREQSUBBANDS = 32
BEATDETECTIONTHRESHOLD = 1.9
VARIANCELIMIT = 1.5e-4

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

bg = (44, 62, 80)
teal = (25, 148, 126)
yellow = (241, 196, 15)

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

waveFormX1 = width/6
waveFormX2 = width*5/6
waveFormXRange = np.linspace(waveFormX1, waveFormX2, numPoints)

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
# to get energy, take magnitude squared of fftData
# divide into NUMFREQSUBBANDS = 32

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
energySubBandsHistory = [collections.deque(maxlen=NUMCHUNKSPERSECOND)\
                         for i in range(NUMFREQSUBBANDS)]

# use history to calculate avg energy over the history
avgEnergySubBands = np.zeros(shape=(NUMFREQSUBBANDS))
for i in range(NUMFREQSUBBANDS):
    avgEnergySubBands[i] = sum(energySubBandsHistory[i])/NUMCHUNKSPERSECOND

beatsPerSubBand = np.zeros(shape=(NUMFREQSUBBANDS), dtype=int)

###############################################
# run pygame
###############################################

#play actual song, not cut up version
# woo = pygame.mixer.Sound(file="Music/beat.wav")
# woo.play()

index = 0
running = True
bassTextOn = False
bassTextCounter = 0
bassTextLimit = 15

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
        data = -logAudio[index]
        data = sig.savgol_filter(data, wLen, polyOrder)
        data = sig.savgol_filter(data, wLen, polyOrder)
        data += waveFormY
        pointList = [(waveFormXRange[i], data[i]) for i in range(numPoints)]

        # fft spectrum data
        # values are complex so take magnitude
        # take - log to scale and orient graph
        # move the graph down
        fftData = fftpack.rfft(audio[index], n=CHUNK)
        fftData = np.abs(fftData)
        fftEnergy = np.abs(fftData) # get energy values before data is modified
        fftData = -np.log1p(fftData)/np.log(1.03)
        # print((wLen//4))
        # fftData = sig.savgol_filter(fftData, int(wLen//16)+1, polyOrder+3)
        fftData = sig.savgol_filter(fftData, wLen, polyOrder)
        fftData = sig.savgol_filter(fftData, wLen, polyOrder)
        fftData += height
        fftPointList = [(waveFormXRange[i], fftData[i]) for i in range(numPoints)]

        # beat detection
        if np.max(fftEnergy) != 0:
            fftEnergy = fftEnergy/np.max(fftEnergy)
        fftEnergy.resize((NUMFREQSUBBANDS, CHUNK//NUMFREQSUBBANDS))
        for i in range(NUMFREQSUBBANDS):
            # get energy for each frequency subband
            energySubBands[i] = (NUMFREQSUBBANDS/CHUNK) * np.sum(fftEnergy[i])
            # put new energy into appropriate history buffer,
            # buffer is a queue, so first in, first out when we try
            # to add beyond the max length
            energySubBandsHistory[i].append(energySubBands[i])
            # get avg energy of past second
            avgEnergySubBands[i] = sum(energySubBandsHistory[i])/NUMCHUNKSPERSECOND

            # variance is a second check of whether there is a beat
            # if there is a high variance, then there is probably a beat
            var = 0
            for j in range(len(energySubBandsHistory[i])):
                var += (energySubBandsHistory[i][j]-avgEnergySubBands[i])**2
            energySubBandsVariance[i] = var/NUMCHUNKSPERSECOND

            # if current energy > threshold * avgEnergy,
            # we have beat in the subband
            if (energySubBands[i] > BEATDETECTIONTHRESHOLD*avgEnergySubBands[i]
                and energySubBandsVariance[i] > VARIANCELIMIT):
                beatsPerSubBand[i] += 1

        # if index%NUMCHUNKSPERSECOND == 0:
        #     print(index/NUMCHUNKSPERSECOND, beatsPerSubBand)

        # if (energySubBands[0] > BEATDETECTIONTHRESHOLD*avgEnergySubBands[0] and
        #     energySubBandsVariance[0] > VARIANCELIMIT):
        #     if index > 10:
        #         print('bass')

        # draw waveform
        pygame.draw.lines(screen, teal, False, pointList, 2)
        # draw spectrum
        pygame.draw.lines(screen, yellow, False, fftPointList[::2], 2)

        index += 1
    else: 
        pygame.draw.line(screen, teal, (waveFormX1, waveFormY), (waveFormX2, waveFormY))

    fpsActual = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fpsActual, (50, 50))

    bassText = font.render("bass", True, pygame.Color('white'))
    if (energySubBands[0] > BEATDETECTIONTHRESHOLD*avgEnergySubBands[0] and
        energySubBandsVariance[0] > VARIANCELIMIT):
        bassTextOn = True
    
    if bassTextOn:
        screen.blit(bassText, (width/2, height*3/4))
        bassTextCounter += 1
    
    if bassTextCounter >= bassTextLimit:
        bassTextOn = False
        bassTextCounter = 0

    pygame.display.flip()
