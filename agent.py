#import all nessessary files
from layers import FC_Layer
from network import Network
from functions import pong_loss, tanh
import numpy as np
from matplotlib import pyplot as plt

class agent:
    #agent class to allow computer to interact with the game
    def __init__(self, game):
        #setting up initial variables
        self.game = game
        self.set_up()

        self.move = -1
        self.avg_losses = []
        self.num_frames = []
        self.frame_number = []
        self.games = 0
        self.game_over, self.state, _ = self.game.get_state()

        #setting up graph
        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.avg_losses)
        self.ax.set_xlabel("games")
        self.ax.set_ylabel("average loss")
        self.ax.set_title("Games VS Average Loss")

        
    def set_up(self):
        #creating the neural network to play the game
        self.agent1 = Network(pong_loss)
        self.agent1.add(FC_Layer((6,3), bias_true=False, activation = tanh))
        self.agent1.add(FC_Layer((3,1), bias_true=False, activation = tanh))


    def get_action(self, state):
        #gets a prediction by forward proping the neural net
        state = np.array(state, dtype = float)
        prediction = self.agent1.forward_prop(state)
        #setting the move to be the prediction
        self.move = prediction[0]
    
  

    def main(self):

        #setting up variables
        frames = 0
        training = []
        losses = []

        #we can run this for as long as we want
        random_move = 0.0
        # setup fps limiter
        limit_fps = False

        # we can run this for as long as we want
        while True:
            #each frame getting the state
            frames += 1            

            #getting and playing the move
            self.game_over, self.state, _ = self.game.get_state()
            self.get_action(self.state)
            if np.random.rand() > random_move:
                self.move = np.random.choice([-1,1])
            self.game.machine_play_frame(self.move, 0, limit_fps)
            self.agent1.Qloss(self.state, self.move)
            losses.append(self.agent1.loss)
            self.agent1.Qback_prop(self.agent1.loss)

            # adding the state/move to back_prop at the end of the game
            training.append([self.state, self.move])

            #if the game goes long enough, we want to see
            if frames > 200:
                self.game.view = True
                
            if self.game_over:
                random_move += 0.005
                # back_prop loop
                self.num_frames.append(frames)
                self.avg_losses.append(sum(losses)/len(losses) * 100)

                #every 100th game displaying the plot
                if self.games % 100 == 0:
                    plt.close()
                    plt.plot(self.avg_losses)

                    plt.plot(self.num_frames)
                    plt.show(block = False)

                    if self.games % 500 == 0:
                        self.game.view = True
                        limit_fps = True
                else:
                    self.game.view = False
                    limit_fps = False

                # resetting everything
                losses = []
                training = []
                self.games += 1                
                frames = 0

                self.game.reset()
