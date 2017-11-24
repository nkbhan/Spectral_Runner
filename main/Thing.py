import pygame

class Thing(pygame.sprite.Sprite):
    def __init__(self, color, size, lane=1):
        super().__init__(self)
        
        self.image = pygame.Surface((size, size))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.lane = lane
