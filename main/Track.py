import pygame
from Colors import Colors
import Obstacle

class Track(object):
    def __init__(self, data):
        self.topLeft = (data.width/6, 0)
        self.topRight = (data.width*5/6, 0)
        self.bottomLeft = (data.width/6, data.height)
        self.bottomRight = (data.width*5/6, data.height)
        self.width = self.topRight[0] - self.topLeft[0]
        self.height = data.height
        self.color = Colors.white
        self.lanes = 3
        self.linesPerLane = 3
        self.lineHeight = data.height/4
        self.image = pygame.Surface((self.width, self.height))
        self.image.set_alpha(100)

    def drawBorder(self, screen):
        pygame.draw.line(screen, self.color, self.topLeft, self.bottomLeft, 5)
        pygame.draw.line(screen, self.color, self.topRight, self.bottomRight, 5)

    def drawLane(self, screen, lane):
        for line in range(self.linesPerLane):
            pygame.draw.line(screen, self.color, self.topLeft)

    def drawLanes(self, screen):
        for lane in range(self.lanes - 1):
            self.drawLane(screen, lane)

    def draw(self, screen):
        screen.blit(self.image, self.topLeft)
        self.drawBorder(screen)
