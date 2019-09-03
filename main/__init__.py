# Naren Bhandari, nbhandar
# 15 112 Term Project
# MVC layout and modes based on lecture notes on event based animations

"""
__init__.py

runs the main game loop of pygame
"""

import os
import sys
import pygame
import numpy as np
import Obstacle
import Track
import time
import threading
from Data import *
from Colors import *
from Audio import *
from Player import *
from Explosion import *
from Score import *

# constants
CHUNK = 1024
RATE = 44100

###############################################
# init pygame
###############################################

pygame.mixer.pre_init(frequency=RATE, size=-16, channels=2, buffer=CHUNK)
pygame.init()
clock = pygame.time.Clock()
font = pygame.font.SysFont('moreperfectdosvga', 23)
bigFont = pygame.font.SysFont('moreperfectdosvga', 35)
biggerFont = pygame.font.SysFont('moreperfectdosvga', 50)
width, height = 960, 540

# init Data
data = Data()
def init(data):
    data.width = width
    data.height = height
    data.size = (data.width, data.height)
    data.screen = pygame.display.set_mode(data.size)
    data.fps = 60
    Obstacle.Obstacle.init()
    data.obstacles = pygame.sprite.Group()
    data.leftObstacles = pygame.sprite.Group()
    data.midObstacles = pygame.sprite.Group()
    data.rightObstacles = pygame.sprite.Group()
    Explosion.init()
    data.explosions = pygame.sprite.Group()
    data.bg = Colors.black
    data.bg = pygame.image.load("Images/background4.png").convert()
    data.bg = pygame.transform.scale(data.bg, (data.width, data.height)) 
    data.track = Track.Track(data)
    Player.init(data)
    data.players = pygame.sprite.GroupSingle()
    data.leftPlayers = pygame.sprite.GroupSingle()
    data.midPlayers = pygame.sprite.GroupSingle()
    data.rightPlayers = pygame.sprite.GroupSingle()
    data.scrollY = 0
    data.score = 0
    data.mode = "splashScreen"
    data.gameModes = ["Groove Mode", "Rhythm Mode"]
    data.title = pygame.image.load("Images/title.png")
    data.instructions = pygame.image.load("Images/instructions.png")
    data.running = True
    data.songsPath = "Music"
    data.songNames = [i for i in os.listdir(data.songsPath) \
                    if not os.path.isdir(data.songsPath + '/' + i)]
    data.songs = [font.render(i[:-4], False, Colors.white) for i in data.songNames]
    data.highlighted = 0
    data.lanes = 3
    data.delay = 3000 # in ms,  3 seconds
    data.songGameOffset = .75 # in seconds
    data.curIndex = -1
    data.lastLane = 0
    data.lastIndexObstacleAdded = 0
    data.indecesBetweenObstacles = 10

init(data)
##########################
# helper functions for all the game modes
##########################

def leftMouseClicked(x, y, data):
    pass

def rightMouseClicked(data):
    pass

def moveBackground(data):
    # moves the top position of the background image down
    data.bgRelativeY = data.scrollY % data.bg.get_rect().height
    data.scrollY += 1

def drawBackground(screen, data):
    # blits background at given height, and blits again above it if there
    # is empty space. 
    # This function when used with moveBackground, gives the effect of
    # an infinitely scrolling background.
    screen.blit(data.bg, (0, data.bgRelativeY))
    if data.bgRelativeY + data.bg.get_rect().height > data.height:
        screen.blit(data.bg, (0, data.bgRelativeY - data.height))

def drawImage(screen, image, cx, cy):
    # blits an surface to the screen centred at cx, cy
    rect = image.get_rect()
    width = rect[2]
    height = rect[3]
    screen.blit(image, (cx-width/2, cy-height/2))

########################
# Splash Screen Stuff
########################

def splashScreenTimerFired(time, data):
    moveBackground(data)

def splashScreenRedrawAll(screen, data):
    drawBackground(screen, data)
    drawImage(screen, data.title, data.width/2, data.height*2/5)
    drawImage(screen, data.instructions, data.width/2, data.height*4/5)
    # fpsActual = font.render(str(int(clock.get_fps())), True, Colors.white)
    # screen.blit(fpsActual, (50, 50))

def splashScreenEventHandler(data):
    # press space to continue
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                data.mode = "chooseGameMode"
        elif event.type == pygame.QUIT:
            data.running = False
            sys.exit()

########################
# Play Game Mode stuff for both drum and groove mode
#######################

def playSong(data):
    pygame.mixer.music.set_endevent(pygame.USEREVENT)
    pygame.mixer.music.load(data.song.file)
    time.sleep(data.delay/1000)
    pygame.mixer.music.play()

def playGameInit(data):
    # synchronize song and game
    dist = Player.y + Obstacle.Obstacle.size
    speed = data.fps * Obstacle.Obstacle.vy
    timeToGoDown = dist/speed
    Obstacle.Obstacle.vy = dist/(data.songGameOffset*data.fps)
    # play song
    data.song = Audio(data.song)
    data.song.getBeats()
    audioThread = threading.Thread(target=playSong, args=(data,))
    audioThread.start()
    data.playStartTime = time.time()
    if data.gameMode == "Rhythm Mode":
        rhythmModeInit(data)
    elif data.gameMode == "Groove Mode":
        grooveModeInit(data)

########################
# groove mode stuff
#######################

def grooveModeInit(data):
    # resest players and score
    data.players.empty()
    data.leftPlayers.empty()
    data.midPlayers.empty()
    data.rightPlayers.empty()
    player = Player(data, 0) # for pink color
    player.lane = 1 # move to middle
    player.updateXPos(data)
    data.players.add(player)
    data.score = Score()

def grooveModeEventHandler(data):
    player = data.players.sprite
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # move right and left based on arrow keys
            if event.key == pygame.K_RIGHT:
                if player:
                    player.update(1, data)
            elif event.key == pygame.K_LEFT:
                if player:
                    player.update(-1, data)
            # if player presses esc, go to home screen
            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                init(data)
                data.mode = "splashScreen"
        # if song ends go to score Screen
        elif event.type == pygame.USEREVENT:
            data.mode = "scoreScreen"
        elif event.type == pygame.QUIT:
            data.running = False
            sys.exit()

def grooveModeRedrawAll(screen, data):
    drawBackground(screen, data)
    data.song.drawWaveform(screen, data)
    data.track.draw(screen)
    data.obstacles.draw(screen)
    data.players.draw(screen)
    data.explosions.draw(screen)
    data.score.draw(screen, font)

def grooveModeTimerFired(dt, data):
    moveBackground(data)
    data.explosions.update()
    if time.time() - data.playStartTime > data.songGameOffset:
        # since there is some overlap between frames of video and chunks of
        # audio, only add a new obstacle if the chunk of audio has moved \
        # forward and there is a beat
        data.lastIndex = data.curIndex
        data.curIndex = data.song.getCurrentIndex(pygame.mixer.music.get_pos() + 
                                                data.songGameOffset*1000)
        if data.curIndex > data.lastIndex:
            beats = data.song.isBeat(data.curIndex)
            # add an obstacle to course
            # use mid range frequencies
            if beats[3] or beats[4] or beats[5]:
                if data.lastLane == 0:
                    lane = np.random.randint(0, data.lanes-1)
                elif data.lastLane == 1:
                    lane = np.random.randint(0, data.lanes)
                elif data.lastLane == 2:
                    lane = np.random.randint(1, data.lanes)
                data.obstacles.add(Obstacle.Obstacle(lane, data))
                data.lastLane = lane
        # check collisions
        for player in pygame.sprite.groupcollide(data.players, data.obstacles,
                                                 False, True):
            player.turnOn()
            data.explosions.add(Explosion(player.x, player.y))
            # data.score += 1
            data.score.update()

        #update sprites
        for player in data.players:
            player.updateTimer()
        data.obstacles.update(data)

##########################
# Rhythm Mode
##########################

def rhythmModeInit(data):
    data.players.empty()
    data.leftPlayers.empty()
    data.midPlayers.empty()
    data.rightPlayers.empty()
    data.leftPlayers.add(Player(data, 0))
    data.midPlayers.add(Player(data, 1))
    data.rightPlayers.add(Player(data, 2))
    data.score = Score()

def rhythmModeDrumHit(data, players, obstacles):
    collision = pygame.sprite.groupcollide(players, obstacles, False,
                                           True)
    for player in players:
        player.turnOn()
        if player not in collision:
            data.score.breakStreak()
    for player in collision:
        data.explosions.add(Explosion(player.x, player.y))
        data.score.update()

def rhythmModeEventHandler(data):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                rhythmModeDrumHit(data, data.rightPlayers, data.rightObstacles)
            elif event.key == pygame.K_LEFT:
                rhythmModeDrumHit(data, data.leftPlayers, data.leftObstacles)
            elif event.key == pygame.K_DOWN:
                rhythmModeDrumHit(data, data.midPlayers, data.midObstacles)
            # if user presses esc, go to splash screen
            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                init(data)
                data.mode = "splashScreen"
        elif event.type == pygame.USEREVENT:
            data.mode = "scoreScreen"
        elif event.type == pygame.QUIT:
            data.running = False
            sys.exit()

def rhythmModeRedrawAll(screen, data):
    drawBackground(screen, data)
    data.song.drawWaveform(screen, data)
    data.track.draw(screen)
    data.leftObstacles.draw(screen)
    data.midObstacles.draw(screen)
    data.rightObstacles.draw(screen)
    data.leftPlayers.draw(screen)
    data.midPlayers.draw(screen)
    data.rightPlayers.draw(screen)
    data.explosions.draw(screen)
    data.score.draw(screen, font)

def rhythmModeTimerFired(dt, data):
    moveBackground(data)
    data.explosions.update()
    if time.time() - data.playStartTime > data.songGameOffset:
        data.lastIndex = data.curIndex
        data.curIndex = data.song.getCurrentIndex(pygame.mixer.music.get_pos() + 
                                                data.songGameOffset*1000)
        # only add an obstacle if index of song position has actually changed
        if data.curIndex > data.lastIndex:
            beats = data.song.isBeat(data.curIndex)
            #bass drum...
            if beats[0] and beats[1]:
                data.leftObstacles.add(Obstacle.Obstacle(0, data))
            #snare
            if beats[5]:
                data.midObstacles.add(Obstacle.Obstacle(1, data))
            # hi hats etc
            if beats[8]:
                data.rightObstacles.add(Obstacle.Obstacle(2, data))
        data.leftObstacles.update(data)
        data.midObstacles.update(data)
        data.rightObstacles.update(data)
        for players in [data.leftPlayers, data.midPlayers, data.rightPlayers]:
            for player in players:
                player.updateTimer()

############################
# Selection Screen Stuff
############################

def selectionScreenTimerFired(time, data):
    moveBackground(data)

def drawSongSelections(screen, data):
    chooseSongText = biggerFont.render("Choose a Song", True, Colors.white)
    screen.blit(chooseSongText, (data.width/10, data.height/10))
    numSongs = len(data.songs)
    if numSongs == 0:
        text = bigFont.render("Add wav files to the Music folder!!", False,
                           Colors.white)
        screen.blit(text, (data.width/7, data.width/4))
    for i, song in enumerate(data.songs):
        if i == data.highlighted:
            song = font.render(data.songNames[i][:-4], False, Colors.magenta)
        screen.blit(song, (data.width/4, 
                           data.height/5 + i*(data.height*8/10)/numSongs))

def selectionScreenRedrawAll(screen, data):
    drawBackground(screen, data)
    drawSongSelections(screen, data)
    # fpsActual = font.render(str(int(clock.get_fps())), True, Colors.white)
    # screen.blit(fpsActual, (50, 50))

def selectionScreenEventHandler(data):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # hit space to choose song and start the game
            if event.key == pygame.K_SPACE:
                if len(data.songs) > 0:
                    data.song = "Music" + '/' + data.songNames[data.highlighted]
                    data.mode = data.gameMode
                    data.highlighted = 0
                    playGameInit(data)
            elif event.key == pygame.K_DOWN:
                data.highlighted = min(len(data.songs)-1, data.highlighted+1)
            elif event.key == pygame.K_UP:
                data.highlighted = max(0, data.highlighted-1)
        elif event.type == pygame.QUIT:
            data.running = False
            sys.exit()


##########################
# chhose game mode screen
##########################

def chooseGameModeScreenTimerFired(time, data):
    moveBackground(data)

def drawGameModeChoice(screen, data):
    chooseModeText = biggerFont.render("Choose a Game Mode", True, Colors.white)
    screen.blit(chooseModeText, (data.width/10, data.height/10))
    for i in range(len(data.gameModes)):
        if i == data.highlighted:
            choice = bigFont.render(data.gameModes[i], True, Colors.magenta)
        else:
            choice = bigFont.render(data.gameModes[i], True, Colors.white)
        x = data.width/4
        y = data.height/3 + data.height/4*i
        screen.blit(choice, (x, y))

def chooseGameModeScreenRedrawAll(screen, data):
    drawBackground(screen, data)
    drawGameModeChoice(screen, data)
    # fpsActual = font.render(str(int(clock.get_fps())), True, Colors.white)
    # screen.blit(fpsActual, (50, 50))

def chooseGameModeScreenEventHandler(data):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            # click space to choose a mode, go to song selection
            if event.key == pygame.K_SPACE:
                data.gameMode = data.gameModes[data.highlighted]
                data.highlighted = 0
                data.mode = "selectionScreen"
            elif event.key == pygame.K_DOWN:
                data.highlighted = 1
            elif event.key == pygame.K_UP:
                data.highlighted = 0
        elif event.type == pygame.QUIT:
            data.running = False
            sys.exit()

########################
# Score Screen Stuff
########################

def scoreScreenDrawTitle(screen, data):
    text = biggerFont.render("Results", True, Colors.white)
    screen.blit(text, (data.width/10, data.height/10))

def scoreScreenDrawScore(screen, data, font):
    text = font.render("Score: %d"%data.score.score, True, Colors.white)
    screen.blit(text, (data.width/5, data.height/4))

def scoreScreenDrawHits(screen, data, font):
    text = font.render("Hit: %.2f%%"%(data.score.getPercentHit()),
                       True, Colors.white)
    screen.blit(text, (data.width/5, data.height/4 + data.height/20))

def scoreScreenDrawMisses(screen, data, font):
    text = font.render("Missed: %.2f%%"%(data.score.getPercentMissed()),
                       True, Colors.white)
    screen.blit(text, (data.width/5, data.height/4 + 2*data.height/20))

def scoreScreenDrawStreak(screen, data, font):
    text = font.render("Longest Streak: %d"%(data.score.maxStreak), True,
                       Colors.white)
    screen.blit(text, (data.width/5, data.height/4 + 3*data.height/20))

def scoreScreenDrawMultiplier(screen, data, font):
    text = font.render("Largest Multiplier: x%d"%(data.score.biggestMultiplier),
                       True, Colors.white)
    screen.blit(text, (data.width/5, data.height/4 + 4*data.height/20))

def scoreScreenRedrawAll(screen, data):
    drawBackground(screen, data)
    scoreScreenDrawTitle(screen, data)
    scoreScreenDrawScore(screen, data, bigFont)
    scoreScreenDrawHits(screen, data, bigFont)
    scoreScreenDrawMisses(screen, data, bigFont)
    scoreScreenDrawStreak(screen, data, bigFont)
    scoreScreenDrawMultiplier(screen, data, bigFont)

def scoreScreenTimerFired(time, data):
    moveBackground(data)

def scoreScreenEventHandler(data):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                data.mode = "splashScreen"
        elif event.type == pygame.QUIT:
            data.running = False
            sys.exit()

#################
# mode pickers
################

def timerFired(time, data):
    if data.mode == "splashScreen":
        splashScreenTimerFired(time, data)
    elif  data.mode == "playGame":
        playGameTimerFired(time, data)
    elif data.mode == "selectionScreen":
        selectionScreenTimerFired(time, data)
    elif data.mode == "chooseGameMode":
        chooseGameModeScreenTimerFired(time, data)
    elif data.mode == "Rhythm Mode":
        rhythmModeTimerFired(time, data)
    elif data.mode == "Groove Mode":
        grooveModeTimerFired(time, data)
    elif data.mode == "scoreScreen":
        scoreScreenTimerFired(time, data)

def redrawAll(screen, data):
    if data.mode == "splashScreen":
        splashScreenRedrawAll(screen, data)
    elif  data.mode == "playGame":
        playGameRedrawAll(screen, data)
    elif data.mode == "selectionScreen":
        selectionScreenRedrawAll(screen, data)
    elif data.mode == "chooseGameMode":
        chooseGameModeScreenRedrawAll(screen, data)
    elif data.mode == "Rhythm Mode":
        rhythmModeRedrawAll(screen, data)
    elif data.mode == "Groove Mode":
        grooveModeRedrawAll(screen, data)
    elif data.mode == "scoreScreen":
        scoreScreenRedrawAll(screen, data)

def eventHandler(data):
    if data.mode == "splashScreen":
        splashScreenEventHandler(data)
    elif data.mode == "playGame":
        playGameEventHandler(data)
    elif data.mode == "selectionScreen":
        selectionScreenEventHandler(data)
    elif data.mode == "chooseGameMode":
        chooseGameModeScreenEventHandler(data)
    elif data.mode == "Rhythm Mode":
        rhythmModeEventHandler(data)
    elif data.mode == "Groove Mode":
        grooveModeEventHandler(data)
    elif data.mode == "scoreScreen":
        scoreScreenEventHandler(data)

# game loop
while data.running:
    dtime = clock.tick_busy_loop(data.fps)
    timerFired(dtime, data)
    eventHandler(data)
    redrawAll(data.screen, data)
    pygame.display.flip()
