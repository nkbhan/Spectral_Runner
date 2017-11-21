import sys
import wavStuff
import pygame
import numpy as numpy

# constants
CHUNK = 1024
RATE = 44100

f = 'Music/CutAndRun.wav'

###############################################
# init pygame
###############################################

pygame.mixer.pre_init(frequency=RATE, size=-16, channels=2, buffer=CHUNK)
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.Font(None, 30)
size = width, height = 1000, 600
fps = round(RATE/CHUNK)
screen = pygame.display.set_mode(size)

bg = (0, 0, 0)
teal = (25, 148, 126)
yellow = (241, 196, 15)

def mouseClicked(x, y):
    print("as")

running = True
while running:
    time = clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouseClicked(*(event.pos))
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    
    screen.fill(bg)

    pygame.display.flip()
