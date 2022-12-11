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
        while True:
            #each frame getting the state
            frames += 1            

            #getting and playing the move
            self.game_over, self.state, _ = self.game.get_state()
            self.get_action(self.state)
            self.game.machine_play_frame(self.move, 0) 
            
            #adding the state/move to back_prop at the end of the game
            training.append([self.state, self.move])

            #if the game goes long enough, we want to see
            if frames > 200:
                self.game.view = True
                
            if self.game_over:
                #back_prop loop
                for train in training:
                    self.agent1.Qloss(train[0],train[1])
                    losses.append(self.agent1.loss)
                    self.agent1.Qback_prop(self.agent1.loss) 
                

                self.num_frames.append(frames)
                self.avg_losses.append(sum(losses)/len(losses) * 100)

                #every 100th game displaying the plot
                if self.games % 100 == 0:
                    plt.close()
                    plt.title("Loss and # of Frames")
                    plt.xlabel("Game #")
                    plt.plot(self.num_frames, label="# of Frames")
                    plt.plot(self.avg_losses, label="Avg of Losses")
                    plt.show(block = False)
                    plt.legend()

                #resetting everything
                self.game.view = False
                losses = []
                training = []
                self.games += 1                
                frames = 0
                self.game.reset()
