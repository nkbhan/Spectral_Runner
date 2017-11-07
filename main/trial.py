import sys, pygame
import numpy as np

pygame.init()

clock = pygame.time.Clock()

size = width, height = 600, 240
speed = [1, 1]
black = 0, 0, 0
white = (255, 255, 255, 50)

screen = pygame.display.set_mode(size)

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill(black)

# ball = pygame.image.load("ball.bmp")
# ballrect = ball.get_rect()

n = 8
numOfRects = 2**n

margin = 10
w = (width-2*margin)/numOfRects

print(w)
rects = []
for i in range(numOfRects):
    h = np.random.randint(10, 200)
    rects.append(pygame.Rect(margin+ w*(i+1), height-10-h, w/2, h))

dy = 1
while 1:
    time = clock.tick(45)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # pygame.draw.rect(screen, (200, 200, 200, 50), rectangle)
    # ballrect = ballrect.move(speed)
    # if ballrect.left < 0 or ballrect.right > width:
    #     speed[0] = -speed[0]
    # if ballrect.top < 0 or ballrect.bottom > height:
    #     speed[1] = -speed[1]


    screen.blit(background, (0, 0))
    # screen.fill((200, 200, 200, 50), rectangle)
    for i in rects:
        screen.fill(white, i)
        i.inflate_ip(0, -dy)
        i.move_ip(0, dy)
    # screen.blit(ball, ballrect)
    pygame.display.flip()