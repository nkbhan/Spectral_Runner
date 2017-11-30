import pygame

class Explosion(pygame.sprite.Sprite):
    @staticmethod
    def init():
        Explosion.frames = []
        image = pygame.image.load("Images/light_004[1].png").convert_alpha()
        width, height = image.get_size()
        rows = cols = 5
        Explosion.frameWidth, Explosion.frameHeight = width/cols, height/rows
        for row in range(rows):
            for col in range(cols):
                rect = (col*Explosion.frameWidth, row*Explosion.frameHeight, 
                        Explosion.frameWidth, Explosion.frameHeight)
                frame = image.subsurface(rect)
                Explosion.frames.append(frame)
    
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.frame = 0
        self.updateFrame()
    
    def updateFrame(self):
        self.image = self.frames[self.frame]
        self.rect = pygame.Rect(self.x-self.frameWidth/2,
                                self.y-self.frameHeight/2,
                                self.frameWidth, self.frameHeight)
    
    def update(self):
        self.frame += 1
        if self.frame < len(self.frames):
            self.updateFrame()
        else:
            self.kill()