import random
import sys
import wavStuff
import pygame
import numpy as np
import Data
import Obstacle
import Track
import Player
from Colors import *

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
size = width, height = 1200, 600
fps = round(RATE/CHUNK)
screen = pygame.display.set_mode(size)

data = Data.Data()
data.width = width
data.height = height
data.obstacles = pygame.sprite.Group()
data.bg = Colors.black
data.bg = pygame.image.load("Images/background.png").convert()
print(data.bg.get_rect())
data.bg = pygame.transform.scale(data.bg, (data.width, data.height)) 
print(data.bg.get_rect())
# Track.Track.init()
data.track = Track.Track(data)
data.player = None
data.players = pygame.sprite.Group()

def leftMouseClicked(x, y, data):
    print("Created obstacle ", end='')
    lane = np.random.randint(0, 3)
    o = Obstacle.Obstacle(lane, data)
    print(o.x, o.y, o.rect)
    data.obstacles.add(o)

def rightMouseClicked(data):
    if data.player == None:
        print("Created player ", end='')
        data.player = Player.Player(data.width, data.height)
        data.players.add(data.player)
        print(data.player)

def eventHandler(data):
    global running
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                leftMouseClicked(*(event.pos), data)
            elif event.button == 3:
                rightMouseClicked(data)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if data.player:
                    data.player.update(1, data)
            elif event.key == pygame.K_LEFT:
                if data.player:
                    data.player.update(-1, data)
        elif event.type == pygame.QUIT:
            running = False
            sys.exit()

running = True
while running:
    time = clock.tick(fps)
    eventHandler(data)

    screen.blit(data.bg, (0,0))
    data.track.draw(screen)
    data.obstacles.draw(screen)
    data.players.draw(screen)

    pygame.display.flip()
