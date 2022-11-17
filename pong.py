# http://www-classes.usc.edu/engr/ee-s/477p/s00/pong.html
# used above link for game specificaations
import pygame 
import sys
import time


WHITE = (255,255,255)
BLACK = (0,0,0)
SPEED = [2,2]
FPS = (1/60) * 10**9
PADDLE_SPEED = 2
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 512, 256


class Paddle():

    def __init__(self, screen, start_position, start_direction = [0,3], paddle_size = (2, 28)):
        self.screen = screen
        self.position = start_position
        self.direction = start_direction
        self.size = paddle_size
    
    def draw(self, color):
        pygame.draw.rect(self.screen, color, (self.position[0], self.position[1], self.size[0], self.size[1]))

    
    def move_up(self):
        if self.position[1] >= 0:
            self.position[1] -= PADDLE_SPEED

    def move_down(self):
        if self.position[1] + self.size[1] <= SCREEN_HEIGHT:
            self.position[1] += PADDLE_SPEED

class Ball():

    def __init__(self, screen, start_position, start_direction = [-2,2], size = 6):
        self.screen = screen
        self.size = size        
        self.position = start_position
        self.direction = start_direction 
    
    def move(self):
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]
    
    def draw(self, color):
        pygame.draw.circle(self.screen, color, (self.position[0], self.position[1]), self.size)
    
    def check_collision(self, paddles):
        width, height = self.screen.get_size()
        if self.position[0] - self.size <= 0 or self.position[0] + self.size >= width:
            self.direction[0]*=-1
        if self.position[1] - self.size <= 0 or self.position[1] + self.size >= height:
            self.direction[1]*=-1
        for paddle in paddles:
            if self.position[0] - self.size == paddle.position[0]:
                if (self.position[1] < paddle.position[1] + paddle.size[1]) and (self.position[1] > paddle.position[1]):
                    # if self.direction[0] < 0:
                    self.direction[0] *= -1

def main():
    pygame.init()

    WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    WINDOW.fill(BLACK)
    screen = pygame.display.set_mode(SCREEN_SIZE)

    pygame.key.set_repeat(1)

    ball_start = [SCREEN_WIDTH/2, SCREEN_HEIGHT/2]
    ball_size = 7
    ball = Ball(screen, start_position = ball_start, size=ball_size)
    paddle1 = Paddle(screen, start_position = [30,0], paddle_size = [4, 28])
    paddle2 = Paddle(screen, start_position = [SCREEN_WIDTH - 30,0], paddle_size = [4, 28])

    while True:
        start = time.time_ns()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        if keys[pygame.K_w]:
            paddle1.move_up()
        if keys[pygame.K_s]:
            paddle1.move_down()
        if keys[pygame.K_UP]:
            paddle2.move_up()
        if keys[pygame.K_DOWN]:
            paddle2.move_down()


        ball.check_collision([paddle1, paddle2])
        ball.move()

        screen.fill(BLACK)

        ball.draw(WHITE)
        paddle1.draw(WHITE)
        paddle2.draw(WHITE)
        pygame.display.flip()

        frame_time = time.time_ns() - start
        time.sleep((max(FPS - frame_time,0)) * 10**-9)
        
if __name__ == "__main__":
    main()
