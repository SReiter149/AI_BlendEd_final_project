# http://www-classes.usc.edu/engr/ee-s/477p/s00/pong.html
# used above link for game specificaations

#import all nessessary packages
import pygame
import sys
import time

class Paddle:
    #class for the paddle
    def __init__(self, screen, start_position, start_direction=[0, 3], paddle_size=(2, 28), paddle_speed = 2):
        #setting initial variables
        self.screen = screen 
        self.position = start_position 
        self.direction = start_direction
        self.size = paddle_size
        self.PADDLE_SPEED = paddle_speed

    def draw(self, color):
        #draws the paddle at its position
        pygame.draw.rect(self.screen,color,(self.position[0], self.position[1], self.size[0], self.size[1]))

    def move_up(self):
        #moves the paddle up by the paddle's speed
        if self.position[1] >= 0:
            self.position[1] -= self.PADDLE_SPEED

    def move_down(self):
        #moves the paddle down by the paddle's speed
        if self.position[1] + self.size[1] <= self.screen.get_size()[1]:
            self.position[1] += self.PADDLE_SPEED


class Ball:
    #class for the ball
    def __init__(self, screen, start_position, start_direction=[-2, 2], size=6):
        #setting up inital variables
        self.screen = screen
        self.size = size
        self.position = start_position
        self.direction = start_direction

    def move(self):
        #moves the ball based on its direction
        self.position[0] += self.direction[0]
        self.position[1] += self.direction[1]

    def draw(self, color):
        #draws the ball at its current position
        pygame.draw.circle(self.screen, color, (self.position[0], self.position[1]), self.size)

    def check_collision(self, paddles):
        """
        Possible outputs:
        0 means paddle 0 was touched
        1 means paddle 1 was touched
        False means game still going
        True means game is over
        """

        _, height = self.screen.get_size()

        #checks collision with each paddle
        for num, paddle in enumerate(paddles):

            #checks if the ball is within the paddle
            if self.position[0] - self.size <= paddle.position[0] and self.position[0] + self.size >= paddle.position[0]:
                if (self.position[1] - self.size <= paddle.position[1] + paddle.size[1] and self.position[1] + self.size >= paddle.position[1]):
                    #change the x direction of the ball
                    self.direction[0] *= -1
                    return num #returns the index of the paddle to give points

                #return game over bc the x coordinates are correct but he ys are not
                return True 

        #checks the collision with the roof 
        if (self.position[1] <= self.size or self.position[1] + self.size >= height):
            #changes the y direction of the ball
            self.direction[1] *= -1 
        #returns game over is false
        return False
    
class game:
    #class for pong
    def __init__(self, view = True):       
        #setting up constances
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.SPEED = [2, 2]
        self.FPS = (1 / 60) * 10**9
        self.PADDLE_SPEED = 2
        self.PADDLE_SIZE = [2, 56]
        self.PADDLE_OFFSET = 30
        self.SCREEN_SIZE = self.SCREEN_WIDTH, self.SCREEN_HEIGHT = 512, 256

        #setting up game variables
        self.GAME_OVER = False
        self.view = view

        #setting up game window
        pygame.init()
        self.WINDOW = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Pong")
        self.WINDOW.fill(self.BLACK)
        self.screen = pygame.display.set_mode(self.SCREEN_SIZE)
        self.FONT = pygame.font.SysFont(None, 24)
        pygame.key.set_repeat(1)

        #adding the ball
        self.BALL_START = [self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2]
        self.BALL_SIZE = 7
        self.ball = Ball(self.screen, start_position=self.BALL_START, size=self.BALL_SIZE)

        #adding the paddles
        self.paddle1 = Paddle(self.screen, start_position=[self.PADDLE_OFFSET, self.SCREEN_HEIGHT / 2], paddle_size=self.PADDLE_SIZE)
        self.paddle2 = Paddle(self.screen,start_position=[self.SCREEN_WIDTH - self.PADDLE_OFFSET, 0],paddle_size=[self.PADDLE_SIZE[0], self.PADDLE_SIZE[1]*200])

        #adding the scores, can be adapted for 2 players
        self.scores = [0, 0]


    def human_play_frame(self):
        #function for playing for a human

        #start time to allow for constant FPS
        start = time.time_ns()

        #getting human's actions
        keys = pygame.key.get_pressed()

        #allows for exiting of the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        
        #Get player move
        #W or up arrow to move up
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.paddle1.move_up()
        #S or down arrow to move down
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.paddle1.move_down()

        #get collision status
        collision = self.ball.check_collision([self.paddle1, self.paddle2])

        #update game based on collision output
        if type(collision) == bool:
            self.GAME_OVER = collision
        else:
            self.scores[collision] += 1

        #moves the ball based on its direction
        self.ball.move()

        #create scores images
        score1_image = self.FONT.render(str(self.scores[0]), True, self.WHITE)
        score2_image = self.FONT.render(str(self.scores[1]), True, self.WHITE)

        #draw screen 
        self.screen.fill(self.BLACK)
        self.screen.blit(score1_image, (20, 20))
        self.screen.blit(score2_image, (self.SCREEN_WIDTH - 20, 20))
        self.ball.draw(self.WHITE)
        self.paddle1.draw(self.WHITE)
        self.paddle2.draw(self.WHITE)
        pygame.display.flip()

        #Wait so allow for constant FPS
        frame_time = time.time_ns() - start
        time.sleep((max(self.FPS - frame_time, 0)) * 10**-9)        

    def machine_play_frame(self, p1_move, p2_move):
        """
        allow for the agent class to interact with the game

        move > 0 to move up
        move <= 0 to move down
        """

        #allow for human to exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        #update paddles based on the move
        if p1_move > 0:
            self.paddle1.move_up()
        else:
            self.paddle1.move_down()
        if p2_move > 0:
            self.paddle2.move_up()
        else:
            self.paddle2.move_down()

        #get collision status
        collision = self.ball.check_collision([self.paddle1, self.paddle2])

        #update game based on collision output
        if type(collision) == bool:
            self.GAME_OVER = collision
        else:
            self.scores[collision] += 1
        #move the ball
        self.ball.move()

        #display the game if self.view is true
        if self.view:

            #create score images
            score1_image = self.FONT.render(str(self.scores[0]), True, self.WHITE)
            score2_image = self.FONT.render(str(self.scores[1]), True, self.WHITE)
            
            #display game
            self.screen.fill(self.BLACK)
            self.screen.blit(score1_image, (20, 20))
            self.screen.blit(score2_image, (self.SCREEN_WIDTH - 20, 20))
            self.ball.draw(self.WHITE)
            self.paddle1.draw(self.WHITE)
            self.paddle2.draw(self.WHITE)
            pygame.display.flip()

    def get_state(self):
        """
        creates a state output to allow the agent to understand what is happening
        state is the same relative to the paddle


        state is of the form: [paddle y, paddle x, ball y, ball x, ball direction y, ball direction x]
        """

        #creates state
        state1 = [self.paddle1.position[0], self.paddle1.position[1], self.ball.position[0], self.ball.position[1], self.ball.direction[0], self.ball.direction[1]]
        state2 = [self.paddle1.position[0], self.paddle1.position[1], self.SCREEN_WIDTH - self.ball.position[0], self.SCREEN_HEIGHT - self.ball.position[1], -1 * self.ball.direction[0], self.ball.direction[1]] 

        #returns state and game over status     
        return self.GAME_OVER, state1, state2
    
    def reset(self):

        #resets the game to the beginning
        self.GAME_OVER = False
        self.BALL_START = [self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2]
        self.BALL_SIZE = 7
        self.SPEED = [2, 2]
        self.ball = Ball(self.screen, start_position=self.BALL_START, size=self.BALL_SIZE)
        self.paddle1 = Paddle(self.screen, start_position=[self.PADDLE_OFFSET, 0], paddle_size=self.PADDLE_SIZE)
        self.scores = [0, 0] 

def main():
    #main logic to allow the human to play the game

    #creates an instance of the game class
    pong = game()
    while True:
        #plays the step while not game over
        while not pong.GAME_OVER:
            pong.human_play_frame()

        #resets the game on game over 
        pong.reset()

if __name__ == "__main__":
    main()
