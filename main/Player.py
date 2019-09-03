"""
Player.py

contains player class for handling player sprites
"""

import Colors
import pygame

class Player(pygame.sprite.Sprite):
    @staticmethod
    def init(data):
        # initialize all the images and what not
        Player.size = 75
        Player.y = data.height - Player.size
        Player.pinkOn = pygame.image.load("Images/pinkDrumOn.png").convert_alpha()
        Player.pinkOff = pygame.image.load("Images/pinkDrumOff.png").convert_alpha()
        Player.tealOn = pygame.image.load("Images/tealDrumOn.png").convert_alpha()
        Player.tealOff = pygame.image.load("Images/tealDrumOff.png").convert_alpha()
        Player.yellowOn = pygame.image.load("Images/yellowDrumOn.png").convert_alpha()
        Player.yellowOff = pygame.image.load("Images/yellowDrumOff.png").convert_alpha()
        Player.OnImgs = [Player.pinkOn, Player.tealOn, Player.yellowOn]
        Player.OffImgs = [Player.pinkOff, Player.tealOff, Player.yellowOff]

    def __init__(self, data, lane=1):
        super().__init__()
        self.lane = lane
        self.x = data.width/4 + data.width/2 * (1/6 + 2*self.lane/6)
        self.imageOn = self.OnImgs[lane]
        self.imageOff = self.OffImgs[lane]
        self.image = self.imageOff
        self.rect = self.get_rect()
        self.maxLanes = 2
        self.isOn = False
        self.onTime = 5
        self.onTimer = self.onTime
    
    def get_rect(self):
        left = self.x - self.size/2
        right = self.y - self.size/2
        return pygame.Rect(left, right, self.size, self.size)

    def update(self, dlane, data):
        if dlane == 1:
            self.lane = min(self.lane+dlane, self.maxLanes)
        elif dlane == -1:
            self.lane = max(self.lane+dlane, 0)
        self.updateXPos(data)
        
    def updateTimer(self):
        # on image only last for limited time, 5 frames
        # switch off after that
        if self.isOn:
            self.onTimer -= 1
            if self.onTimer <= 0:
                self.image = self.imageOff
                self.isOn = False
                self.onTimer = self.onTime

    def updateXPos(self, data):
        self.x = data.width/4 + data.width/2 * (1/6 + 2*self.lane/6)
        self.rect = self.get_rect()

    def turnOn(self):
        # switch to on image
        self.isOn = True
        self.image = self.imageOn