import Colors
import pygame

class Player(pygame.sprite.Sprite):
    size = 75
    def __init__(self, screenWidth, screenHeight,
                 color=Colors.Colors.neonPink, lane=1):
        super().__init__()
        self.color = color
        self.size = Player.size
        self.x = screenWidth/2
        self.y = screenHeight - self.size
        self.imageOn = pygame.image.load("Images/pinkDrumOn.png").convert_alpha()
        self.imageOff = pygame.image.load("Images/pinkDrumOff.png").convert_alpha()
        self.image = self.imageOff
        # self.image = pygame.Surface((self.size, self.size))
        # self.image.fill(color)

        self.rect = self.get_rect()
        self.lane = lane
        self.maxLanes = 2
        self.isOn = False
        self.onTime = 10
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
        self.isOn = True
        self.image = self.imageOn

    # def move(self, start, end, duration):
    #     newPos = start + (end - start) * n