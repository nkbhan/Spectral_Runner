import pygame
import Colors

class Obstacle(pygame.sprite.Sprite):
    @staticmethod
    def init():
        Obstacle.size = 75
        Obstacle.vy = 7
        Obstacle.baseImage = pygame.image.load("Images/tealObstacle.png").convert_alpha()

    def __init__(self, lane, data, color=Colors.Colors.neonPurple):
        super().__init__()

        self.lane = lane
        self.size = Obstacle.size
        self.y = -self.size
        self.updateXPos(data)

        self.image = pygame.Surface((Obstacle.size, Obstacle.size))
        self.image = self.baseImage
        # self.image.fill(color)

        self.rect = self.get_rect()

    def get_rect(self):
        left = self.x - self.size/2
        top = self.y - self.size/2
        return pygame.Rect(left, top, self.size, self.size)

    def updateXPos(self, data):
        self.x = data.width/4 + data.width/2 * (1/6 + 2*self.lane/6)
        self.rect = self.get_rect()
    
    def updateYPos(self):
        self.y += self.vy
        self.rect = self.get_rect()

    def update(self, data):
        self.updateYPos()
        if self.y > data.height + self.size/2:
            self.kill()
