import sys, pygame
import numpy as np
import audio_preprocessing as audio

pygame.init()
pygame.mixer.init()
song = "Music/05. Luna.mp3"
pygame.mixer.music.load(song)

clock = pygame.time.Clock()

size = width, height = 600, 240
speed = [1, 1]
black = 0, 0, 0
white = (255, 255, 255, 50)

screen = pygame.display.set_mode(size)


# ball = pygame.image.load("ball.bmp")
# ballrect = ball.get_rect()

n = 6
numOfRects = 2**n

margin = 10
w = (width-2*margin)/numOfRects

print(w)
rects = []
for i in range(numOfRects):
    h = np.random.randint(10, 200)
    rects.append(pygame.Rect(margin+ w*(i+1), height-10-h, w/2, h))

spectrum = audio.main()
numChunks = spectrum.shape[0]
numSamples = spectrum.shape[2]
ratio = numSamples/numOfRects

dy = 1
dt = 0
# pygame.mixer.music.play()
while 1:
    time = clock.tick(45)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    # screen.fill((200, 200, 200, 50), rectangle)
    screen.fill(black)
    if dt < numChunks:
        for i in range(numSamples):
            if i%(ratio) == ratio - 1:
                maxHeight = spectrum[dt, 0].max()
                localHeight = spectrum[dt, 0, i]
                if maxHeight != 0:
                    normalizedHeight = localHeight/maxHeight * (height-40)
                else:
                    normalizedHeight = 0
                index = int((i-3)//ratio)
                bottom = rects[index].bottom
                rects[index].height = normalizedHeight
                rects[index].height -= dy
                rects[index].bottom = bottom
                screen.fill(white, rects[index])
    else:
        for i in rects:
            screen.fill(white, i)
            # i.inflate_ip(0, -dy)
            # i.move_ip(0, dy)
    pygame.display.flip()
    dt += 1