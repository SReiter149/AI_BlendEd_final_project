# http://www-classes.usc.edu/engr/ee-s/477p/s00/pong.html
# used above link for game specificaations
import pygame 
import sys
import time




class Paddle():

    def __init__(self, start = [0,0]):
        pass

    def move(self):
        pass

class Ball():

    def __init__(self, start_position = [0,0], start_direction = [2,2], size = 7):
        self.position = start_position
        self.direction = start_direction 
    
    def move(self):
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
    


def main():
    pygame.init()

    WHITE = (255,255,255)
    BLACK = (0,0,0)
    SPEED = [2,2]
    FPS = (1/60) * 10**9

    SIZE = WIDTH, HEIGHT = 512, 256
    WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Pong")
    WINDOW.fill(BLACK)


    ball_start = [WIDTH/2, HEIGHT/2]
    ball_size = 7
    ball = Ball(start_position = ball_start)
    paddle = Paddle()

    screen = pygame.display.set_mode(SIZE)

    while True:
        start = time.time_ns()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        if ball.position[0] - ball_size <= 0 or ball.position[0] + ball_size >= WIDTH:
            ball.direction[0]*=-1
        if ball.position[1] - ball_size <= 0 or ball.position[1] + ball_size >= HEIGHT:
            ball.direction[1]*=-1
        ball.move()
        print(ball.direction, ball.position)

        screen.fill(BLACK)
        pygame.draw.circle(screen, WHITE, (ball.position[0], ball.position[1]), ball_size)
        pygame.display.flip()

        frame_time = time.time_ns() - start
        time.sleep((max(FPS - frame_time,0)) * 10**-9)
        

main()