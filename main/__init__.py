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
font = pygame.font.SysFont('streamster', 20)
size = width, height = 960, 540
fps = 60
screen = pygame.display.set_mode(size)

data = Data.Data()
data.width = width
data.height = height
data.obstacles = pygame.sprite.Group()
data.bg = Colors.black
data.bg = pygame.image.load("Images/background.png").convert()
data.bg = pygame.transform.scale(data.bg, (data.width, data.height)) 
data.track = Track.Track(data)
data.players = pygame.sprite.Group()
data.player = Player.Player(data.width, data.height)
data.players.add(data.player)
data.scrollY = 0
data.score = 0

def leftMouseClicked(x, y, data):
    print("Created obstacle ", end='')
    lane = np.random.randint(0, 3)
    data.obstacles.add(Obstacle.Obstacle(lane, data))
    print(data.obstacles.sprites()[-1])

def rightMouseClicked(data):
    pass

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

def moveBackground(data):
    data.bgRelativeY = data.scrollY % data.bg.get_rect().height
    data.scrollY += 1

def drawBackground(screen, data):
    screen.blit(data.bg, (0, data.bgRelativeY))
    if data.bgRelativeY + data.bg.get_rect().height > data.height:
        screen.blit(data.bg, (0, data.bgRelativeY - data.height))

def redrawAll(screen, data):
    drawBackground(screen, data)
    data.track.draw(screen)
    data.obstacles.draw(screen)
    data.players.draw(screen)

    score = font.render(str(data.score), True, Colors.white)
    fpsActual = font.render(str(int(clock.get_fps())), True, Colors.white)

    screen.blit(fpsActual, (50, 50))
    screen.blit(score, (50, 70))

def timerFired(time, data):
    moveBackground(data)
    data.obstacles.update(data)
    for _ in pygame.sprite.groupcollide(data.players, data.obstacles,
                                        False, True):
        data.score += 1

running = True
while running:
    # controller
    time = clock.tick(fps)
    timerFired(time, data)
    eventHandler(data)
    redrawAll(screen, data)
    pygame.display.flip()
