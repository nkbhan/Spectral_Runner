import Colors
import pygame

class Player(pygame.sprite.Sprite):
    size = 50
    def __init__(self, screenWidth, screenHeight,
                 color=Colors.Colors.neonPink, lane=1):
        super().__init__()
        self.color = color
        self.size = Player.size
        self.x = screenWidth/2
        self.y = screenHeight - self.size
        
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(color)

        self.rect = self.get_rect()
        self.lane = lane
    
    def get_rect(self):
        left = self.x - self.size/2
        right = self.y - self.size/2
        return pygame.Rect(left, right, self.size, self.size)

    def update(self, dlane, data):
        if dlane == 1:
            self.lane = min(self.lane+dlane, 2)
        elif dlane == -1:
            self.lane = max(self.lane+dlane, 0)
        self.updateXPos(data)

    def updateXPos(self, data):
        self.x = data.width/4 + data.width/2 * (1/6 + 2*self.lane/6)
        self.rect = self.get_rect()
