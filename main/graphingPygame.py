import sys
import pygame
import wavStuff
import numpy as np
import scipy.signal as sig

CHUNK = 1024
rate, audio = wavStuff.sciOpen(wavStuff.f)
numOfChunks = audio.size/CHUNK

pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
size = width, height = 1000, 600
fps = 60

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
data = -audio[0]

# Use Savitzky-Golay filter to smoothen values
# wLen is the length of the window the filter uses
# polyOrder is the order of the polynomial the filter uses
numOfWindowsMinusOne = 5
wLen = data.size//numOfWindowsMinusOne-1 # must be odd
polyOrder = 3

data = sig.savgol_filter(data, wLen, polyOrder)
data = sig.savgol_filter(data, wLen, polyOrder)

data += waveFormY

pointList = [(waveFormX1, waveFormY), (waveFormX2, waveFormY)]

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
        data = -audio[index]
        data = sig.savgol_filter(data, wLen, polyOrder)
        data = sig.savgol_filter(data, wLen, polyOrder)
        data += waveFormY
        pointList = [(waveFormXRange[i], data[i]) for i in range(numPoints)]
        pygame.draw.lines(screen, teal, False, pointList, 2)
        index += 1
    else: 
        pygame.draw.line(screen, teal, (waveFormX1, waveFormY), (waveFormX2, waveFormY))

    fpsActual = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    screen.blit(fpsActual, (50, 50))

    pygame.display.flip()
