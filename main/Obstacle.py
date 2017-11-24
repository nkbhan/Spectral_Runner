import pygame
import Colors

class Obstacle(pygame.sprite.Sprite):
    size = 50
    def __init__(self, lane, data, color=Colors.Colors.neonBlue):
        super().__init__()

        self.lane = lane
        self.size = Obstacle.size
        self.updateXPos(self.lane, data)
        self.y = self.size

        self.image = pygame.Surface((Obstacle.size, Obstacle.size))
        self.image.fill(color)

        self.rect = self.get_rect()

    def get_rect(self):
        left = self.x - self.size/2
        right = self.y - self.size/2
        return pygame.Rect(left, right, self.size, self.size)

    def updateXPos(self, lane, data):
        self.x = data.width/4 + data.width/2 * (1/6 + 2*lane/6)
    
    def update(self):
        pass