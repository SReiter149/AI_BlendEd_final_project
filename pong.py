import pygame
import sys
import time
pygame.init()

size = width, height = 320, 240
sixty_fps = (1/60) * 10**9

speed = [2, 2]
black = 0, 0, 0
white = 255, 255, 255

screen = pygame.display.set_mode(size)

cp = [width/2, height/2]
cr = 20

while True:
    st = time.time_ns()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    if cp[0] - cr <= 0 or cp[0] + cr >= width:
        speed[0]*=-1
    if cp[1] - cr <= 0 or cp[1] + cr >= height:
        speed[1]*=-1
    cp[0] += speed[0]
    cp[1] += speed[1]

    screen.fill(black)
    pygame.draw.circle(screen, white, (cp[0], cp[1]), 20)
    pygame.display.flip()

    dt = time.time_ns() - st
    time.sleep((sixty_fps - dt) * 10**-9)
