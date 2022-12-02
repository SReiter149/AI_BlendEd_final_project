# http://www-classes.usc.edu/engr/ee-s/477p/s00/pong.html
# used above link for game specificaations
import pygame
import sys
import time

class Paddle:
    def __init__(
        self, screen, start_position, start_direction=[0, 3], paddle_size=(2, 28), paddle_speed = 2
    ):
        self.screen = screen
        self.position = start_position
        self.direction = start_direction
        self.size = paddle_size
        self.PADDLE_SPEED = paddle_speed

    def draw(self, color):
        pygame.draw.rect(
            self.screen,
            color,
            (self.position[0], self.position[1], self.size[0], self.size[1]),
        )

    def move_up(self):
        if self.position[1] >= 0:
            self.position[1] -= self.PADDLE_SPEED

    def move_down(self):
        if self.position[1] + self.size[1] <= self.screen.get_size()[1]:
            self.position[1] += self.PADDLE_SPEED


class Ball:
    def __init__(self, screen, start_position, start_direction=[-2, 2], size=6):
        self.screen = screen
        self.size = size
        self.position = start_position
        self.direction = start_direction

    def move(self):
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]

    def draw(self, color):
        pygame.draw.circle(
            self.screen, color, (self.position[0], self.position[1]), self.size
        )

    def check_collision_wall(self):
        width, height = self.screen.get_size()
        if (
            self.position[0] <= self.size or self.position[0] + self.size >= width
        ):  # collision with sides
            self.direction[0] *= -1
            return True
        if (
            self.position[1] <= self.size or self.position[1] + self.size >= height
        ):  # collision with top/bottom
            self.direction[1] *= -1
        return False

    def check_collision_paddle(self, paddle):
        if (
            self.position[1] - self.size <= paddle.position[1] + paddle.size[1]
            and self.position[1] + self.size >= paddle.position[1]
            and self.position[0] - self.size <= paddle.position[0] + paddle.size[0]
            and self.position[0] + self.size >= paddle.position[0]
        ):
            self.direction[0] *= -1
            return True
        return False

    
class game:

    def __init__(self, ):       
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.SPEED = [2, 2]
        self.FPS = (1 / 60) * 10**9
        self.PADDLE_SPEED = 2
        self.PADDLE_SIZE = [2, 56]
        self.PADDLE_OFFSET = 30
        self.SCREEN_SIZE = self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 512, 256
        self.GAME_OVER = False

        pygame.init()

        self.WINDOW = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.WINDOW.fill(self.BLACK)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.FONT = pygame.font.SysFont(None, 24)

        pygame.key.set_repeat(1)

        self.BALL_START = [self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2]
        self.BALL_SIZE = 7
        self.ball = Ball(self.screen, start_position=self.BALL_START, size=self.BALL_SIZE)
        self.paddle1 = Paddle(self.screen, start_position=[self.PADDLE_OFFSET, 0], paddle_size=self.PADDLE_SIZE)
        self.paddle2 = Paddle(
            self.screen,
            start_position=[self.SCREEN_WIDTH - self.PADDLE_OFFSET, 0],
            paddle_size=[self.PADDLE_SIZE[0], self.PADDLE_SIZE[1]*200],
        )
        self.scores = [0, 0]  # player1, then player2
        #self.score = 0

    def human_play_frame(self):
        start = time.time_ns()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if keys[pygame.K_w]:
            self.paddle1.move_up()
        if keys[pygame.K_s]:
            self.paddle1.move_down()
        if keys[pygame.K_UP]:
            self.paddle2.move_up()
        if keys[pygame.K_DOWN]:
            self.paddle2.move_down()
        if self.ball.check_collision_wall():
            self.GAME_OVER = True
        if self.ball.check_collision_paddle(self.paddle1):
            self.score += 1
        if self.ball.check_collision_paddle(self.paddle2):
            self.scores[1] += 1
        self.ball.move()
        score1_image = self.FONT.render(str(self.score), True, self.WHITE)
        #score2_image = self.FONT.render(str(self.scores[1]), True, self.WHITE)

        self.screen.fill(self.BLACK)
        self.screen.blit(score1_image, (20, 20))
        #self.screen.blit(score2_image, (self.SCREEN_WIDTH - 20, 20))
        self.ball.draw(self.WHITE)
        self.paddle1.draw(self.WHITE)
        self.paddle2.draw(self.WHITE)
        pygame.display.flip()

        frame_time = time.time_ns() - start
        time.sleep((max(self.FPS - frame_time, 0)) * 10**-9)        

    def machine_play_frame(self, 
                           p1_move, 
                           p2_move, 
                           view = True):
        #True = move up
        #False = move down
        start = time.time_ns()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if p1_move:
            self.paddle1.move_up()
        else:
            self.paddle1.move_down()
        if p2_move:
            self.paddle2.move_up()
        else:
            self.paddle2.move_down()

        if self.ball.check_collision_wall():
            self.GAME_OVER = True
        if self.ball.check_collision_paddle(self.paddle1):
            self.scores[0] += 1
        if self.ball.check_collision_paddle(self.paddle2):
            self.scores[1] += 1
        self.ball.move()
        if view:
            score1_image = self.FONT.render(str(self.scores[0]), True, self.WHITE)
            score2_image = self.FONT.render(str(self.scores[1]), True, self.WHITE)

            self.screen.fill(self.BLACK)
            self.screen.blit(score1_image, (20, 20))
            self.screen.blit(score2_image, (self.SCREEN_WIDTH - 20, 20))
            self.ball.draw(self.WHITE)
            self.paddle1.draw(self.WHITE)
            self.paddle2.draw(self.WHITE)
            pygame.display.flip()

            frame_time = time.time_ns() - start
            time.sleep((max(self.FPS - frame_time, 0)) * 10**-9)   
    def get_state(self):
        #please check these because there is a good chance I made a mistake
        #I want these numbers to be the same if the positions are the same but flipped for each paddle
        #[paddle y, paddle x, ball y, ball x, ball direction y, ball direction x]
        state1 = [self.paddle1.position[0] - self.PADDLE_SIZE[0] /2, self.paddle1.position[1] - self.PADDLE_SIZE[1]/ 2, self.ball.position[0] - self.BALL_SIZE/2, self.ball.position[1] - self.BALL_SIZE/2, self.ball.direction[0], self.ball.direction[1]]
        state2 = [self.paddle1.position[0], self.paddle1.position[1], self.SCREEN_WIDTH - self.ball.position[0], self.SCREEN_HEIGHT - self.ball.position[1], -1 * self.ball.direction[0], self.ball.direction[1]]      
        return self.GAME_OVER, state1, state2
    
    def reset(self):
        self.GAME_OVER = False
        self.BALL_START = [self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2]
        self.BALL_SIZE = 7
        self.ball = Ball(self.screen, start_position=self.BALL_START, size=self.BALL_SIZE)
        self.paddle1 = Paddle(self.screen, start_position=[self.PADDLE_OFFSET, 0], paddle_size=self.PADDLE_SIZE)
        #self.paddle2 = Paddle(
        #    self.screen,
        #    start_position=[self.SCREEN_WIDTH - self.PADDLE_OFFSET, 0],
        #    paddle_size=self.PADDLE_SIZE,
        #)
        self.scores = [0, 0]  # player1, then player2

def main():
    pong = game()
    while True:
        while not pong.GAME_OVER:
            pong.human_play_frame()
        pong.reset()



if __name__ == "__main__":
    main()
