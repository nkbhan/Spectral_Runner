# Naren Bhandari, nbhandar
# 15 112 Term Project
# MVC layout and modes based on lecture notes on event based animations

import random
import os
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

###############################################
# init pygame
###############################################

pygame.mixer.pre_init(frequency=RATE, size=-16, channels=2, buffer=CHUNK)
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('streamster', 20)
titleFont = pygame.font.SysFont('streamster', 100)
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
data.mode = "splashScreen"
data.title = pygame.image.load("Images/title.png")
data.instructions = pygame.image.load("Images/instructions.png")
data.running = True
data.songsPath = "Music"
data.songNames = [i for i in os.listdir(data.songsPath) \
                  if not os.path.isdir(data.songsPath + '/' + i)]
data.songs = [font.render(i[:-4], True, Colors.white) for i in data.songNames]
data.highlighted = 0

def leftMouseClicked(x, y, data):
    print("Created obstacle ", end='')
    lane = np.random.randint(0, 3)
    data.obstacles.add(Obstacle.Obstacle(lane, data))
    print(data.obstacles.sprites()[-1])

def rightMouseClicked(data):
    pass

def moveBackground(data):
    data.bgRelativeY = data.scrollY % data.bg.get_rect().height
    data.scrollY += 1

def drawBackground(screen, data):
    screen.blit(data.bg, (0, data.bgRelativeY))
    if data.bgRelativeY + data.bg.get_rect().height > data.height:
        screen.blit(data.bg, (0, data.bgRelativeY - data.height))

def drawImage(screen, image, cx, cy):
    rect = image.get_rect()
    width = rect[2]
    height = rect[3]
    screen.blit(image, (cx-width/2, cy-height/2))

# Splash Screen Stuff

def splashScreenTimerFired(time, data):
    moveBackground(data)

def splashScreenRedrawAll(screen, data):
    drawBackground(screen, data)
    drawImage(screen, data.title, data.width/2, data.height*2/5)
    drawImage(screen, data.instructions, data.width/2, data.height*4/5)
    fpsActual = font.render(str(int(clock.get_fps())), True, Colors.white)
    screen.blit(fpsActual, (50, 50))

def splashScreenEventHandler(data):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                data.mode = "selectionScreen"
        elif event.type == pygame.QUIT:
            data.running = False
            sys.exit()

# Play Game Mode stuff

def playGameEventHandler(data):
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
            data.running = False
            sys.exit()

def playGameRedrawAll(screen, data):
    drawBackground(screen, data)
    data.track.draw(screen)
    data.obstacles.draw(screen)
    data.players.draw(screen)

    score = font.render(str(data.score), True, Colors.white)
    fpsActual = font.render(str(int(clock.get_fps())), True, Colors.white)

    screen.blit(fpsActual, (50, 50))
    screen.blit(score, (50, 70))

def playGameTimerFired(time, data):
    moveBackground(data)
    data.obstacles.update(data)
    for _ in pygame.sprite.groupcollide(data.players, data.obstacles,
                                        False, True):
        data.score += 1

# Selection Screen Stuff

def selectionScreenTimerFired(time, data):
    moveBackground(data)

def drawSongSelections(screen, data):
    numSongs = len(data.songs)
    for i, song in enumerate(data.songs):
        if i == data.highlighted:
            song = font.render(data.songNames[i][:-4], True, Colors.magenta)
        screen.blit(song, (data.width/3, i*data.height/numSongs))


def selectionScreenRedrawAll(screen, data):
    drawBackground(screen, data)
    drawSongSelections(screen, data)
    fpsActual = font.render(str(int(clock.get_fps())), True, Colors.white)
    screen.blit(fpsActual, (50, 50))

def selectionScreenEventHandler(data):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                data.song = "Music" + '/' + data.songNames[data.highlighted]
                data.mode = "playGame"
            elif event.key == pygame.K_DOWN:
                data.highlighted = min(len(data.songs)-1, data.highlighted+1)
            elif event.key == pygame.K_UP:
                data.highlighted = max(0, data.highlighted-1)
        elif event.type == pygame.QUIT:
            data.running = False
            sys.exit()

# mode pickers

def timerFired(time, data):
    if data.mode == "splashScreen":
        splashScreenTimerFired(time, data)
    elif  data.mode == "playGame":
        playGameTimerFired(time, data)
    elif data.mode == "selectionScreen":
        selectionScreenTimerFired(time, data)

def redrawAll(screen, data):
    if data.mode == "splashScreen":
        splashScreenRedrawAll(screen, data)
    elif  data.mode == "playGame":
        playGameRedrawAll(screen, data)
    elif data.mode == "selectionScreen":
        selectionScreenRedrawAll(screen, data)

def eventHandler(data):
    if data.mode == "splashScreen":
        splashScreenEventHandler(data)
    elif data.mode == "playGame":
        playGameEventHandler(data)
    elif data.mode == "selectionScreen":
        selectionScreenEventHandler(data)

while data.running:
    time = clock.tick(fps)
    timerFired(time, data)
    eventHandler(data)
    redrawAll(screen, data)
    pygame.display.flip()
