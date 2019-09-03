"""
Explosion.py

contains explosion class that gets triggered when a player hits
an obstacle correctly.
"""

import pygame

class Explosion(pygame.sprite.Sprite):
    @staticmethod
    def init():
        # load frames of explosion animation into a list of frames from
        # the sprite sheet
        Explosion.frames = []
        image = pygame.image.load("Images/light_004[1].png").convert_alpha()
        width, height = image.get_size()
        rows, cols = 5, 5
        Explosion.frameWidth, Explosion.frameHeight = width/cols, height/rows
        for row in range(rows):
            for col in range(cols):
                # get frame contained in the rectangle
                rect = (col*Explosion.frameWidth, row*Explosion.frameHeight, 
                        Explosion.frameWidth, Explosion.frameHeight)
                frame = image.subsurface(rect)
                Explosion.frames.append(frame)
    
    def __init__(self, x, y):
        # initialize an explosion at position x, y and zeroth frame
        super().__init__()
        self.x = x
        self.y = y
        self.frame = 0
        self.updateFrame()
    
    def updateFrame(self):
        # change the fram being displayed
        self.image = self.frames[self.frame]
        self.rect = pygame.Rect(self.x-self.frameWidth/2,
                                self.y-self.frameHeight/2,
                                self.frameWidth, self.frameHeight)
    
    def update(self):
        # loop through frames of explosion and
        # kill the sprite if the explosion is over
        self.frame += 1
        if self.frame < len(self.frames):
            self.updateFrame()
        else:
            self.kill()