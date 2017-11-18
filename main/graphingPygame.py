import sys
import pygame
import wavStuff
import numpy as np
import scipy.signal as sig
import scipy.fftpack as fftpack

CHUNK = 1024
rate, audio = wavStuff.sciOpen(wavStuff.f)
# take log(audio + 1)
# The +1 handles the log(0) case
# maniuplate signs to avoid logs of negatve numbers
signs = np.sign(audio)
logAudio = np.fabs(audio)
logAudio = np.log1p(logAudio)/np.log(1.2)
logAudio *= signs
numOfChunks = audio.size/CHUNK

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

def drawPlot():
    pass

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

#play actual song, not cut up version
# woo = pygame.mixer.Sound(file="Music/beat.wav")
# woo.play()

index = 0
running = True
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
        fftData = -np.log1p(fftData)/np.log(1.03)
        fftData = sig.savgol_filter(fftData, 2*wLen+1, polyOrder)
        # fftData = sig.savgol_filter(fftData, wLen, polyOrder)
        fftData += height
        fftPointList = [(waveFormXRange[i], fftData[i]) for i in range(numPoints)]

        pygame.draw.lines(screen, teal, False, pointList, 2)
        pygame.draw.lines(screen, yellow, False, fftPointList[::2], 2)
        index += 1
    else: 
        pygame.draw.line(screen, teal, (waveFormX1, waveFormY), (waveFormX2, waveFormY))

    fpsActual = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fpsActual, (50, 50))

    pygame.display.flip()
