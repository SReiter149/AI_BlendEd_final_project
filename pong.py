# http://www-classes.usc.edu/engr/ee-s/477p/s00/pong.html
# used above link for game specificaations
import pygame
import sys
import time


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEED = [2, 2]
FPS = (1 / 60) * 10**9
PADDLE_SPEED = 2
PADDLE_SIZE = [2, 56]
PADDLE_OFFSET = 30
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 512, 256


class Paddle:
    def __init__(
        self, screen, start_position, start_direction=[0, 3], paddle_size=(2, 28)
    ):
        self.screen = screen
        self.position = start_position
        self.direction = start_direction
        self.size = paddle_size

    def draw(self, color):
        pygame.draw.rect(
            self.screen,
            color,
            (self.position[0], self.position[1], self.size[0], self.size[1]),
        )

    def move_up(self):
        if self.position[1] >= 0:
            self.position[1] -= PADDLE_SPEED

    def move_down(self):
        if self.position[1] + self.size[1] <= SCREEN_HEIGHT:
            self.position[1] += PADDLE_SPEED


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


def main():
    pygame.init()

    WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pong")
    WINDOW.fill(BLACK)
    screen = pygame.display.set_mode(SCREEN_SIZE)
    FONT = pygame.font.SysFont(None, 24)

    pygame.key.set_repeat(1)

    ball_start = [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2]
    ball_size = 7
    ball = Ball(screen, start_position=ball_start, size=ball_size)
    paddle1 = Paddle(screen, start_position=[PADDLE_OFFSET, 0], paddle_size=PADDLE_SIZE)
    paddle2 = Paddle(
        screen,
        start_position=[SCREEN_WIDTH - PADDLE_OFFSET, 0],
        paddle_size=PADDLE_SIZE,
    )
    scores = [0, 0]  # player1, then player2
    while True:
        start = time.time_ns()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if keys[pygame.K_w]:
            paddle1.move_up()
        if keys[pygame.K_s]:
            paddle1.move_down()
        if keys[pygame.K_UP]:
            paddle2.move_up()
        if keys[pygame.K_DOWN]:
            paddle2.move_down()
        if ball.check_collision_wall():
            sys.exit()
        if ball.check_collision_paddle(paddle1):
            scores[0] += 1
        if ball.check_collision_paddle(paddle2):
            scores[1] += 1
        ball.move()
        score1_image = FONT.render(str(scores[0]), True, WHITE)
        score2_image = FONT.render(str(scores[1]), True, WHITE)

        screen.fill(BLACK)
        screen.blit(score1_image, (20, 20))
        screen.blit(score2_image, (SCREEN_WIDTH - 20, 20))
        ball.draw(WHITE)
        paddle1.draw(WHITE)
        paddle2.draw(WHITE)
        pygame.display.flip()

        frame_time = time.time_ns() - start
        time.sleep((max(FPS - frame_time, 0)) * 10**-9)


if __name__ == "__main__":
    main()
