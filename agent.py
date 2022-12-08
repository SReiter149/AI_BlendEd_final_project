from layers_stable import Drop_Out_Layer, Activation_Layer, FC_Layer
from network_stable import Network
from functions_stable import pong_loss, sigmoid, tanh
import numpy as np
from numpy import random
from time import sleep
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation

class agent:
    def __init__(self, game):
        self.game = game
        self.set_up()

        self.move1 = False #down
        self.move2 = True #up
        self.avg_losses = []
        self.num_frames = []
        self.frame_number = []
        self.fig, self.ax = plt.subplots()
        self.games = 0
        self.ax.plot(self.avg_losses)
        self.ax.set_xlabel("games")
        self.ax.set_ylabel("average loss")
        self.ax.set_title("Games VS Average Loss")
        self.game_over, self.state1, self.state2 = self.game.get_state()
    def set_up(self):
        self.agent1 = Network(pong_loss)
        self.agent1.add(FC_Layer((6,64), bias_true=False))
        self.agent1.add(Activation_Layer(tanh))
        self.agent1.add(FC_Layer((64,32), bias_true=False))
        self.agent1.add(Activation_Layer(tanh))
        self.agent1.add(FC_Layer((32,10), bias_true=False))
        self.agent1.add(Activation_Layer(tanh))
        self.agent1.add(FC_Layer((10,1), bias_true=False))
        self.agent1.add(Activation_Layer(tanh))

        #self.agent2 = Network(pong_loss)
        #self.agent2.add(FC_Layer((6,24), bias_true=True))
        #self.agent2.add(Activation_Layer())
        #self.agent2.add(FC_Layer((24,1), bias_true=True))

    def get_action(self, state1, state2):
        state1 = np.array(state1, dtype = float)
        prediction = self.agent1.forward_prop(state1)
        #print(prediction.shape)
        # I don't remember making it 3 dimensional
        self.move1 = round(prediction[0])
        
        #state2 = np.array(state1, dtype = float)
        #prediction = self.agent2.forward_prop(state2)
        #self.move2 = bool(round(prediction[0]))
        self.move2 = round(sigmoid(round(prediction[0])))
    
  

    def main(self):
        frames = 0
        training = []
        while True:
            frames += 1
            losses = []
            self.get_action(self.state1, self.state2)
            self.game.machine_play_frame(self.move1, self.move2)  # will update the game based on the move
            self.game_over, self.state1, self.state2 = self.game.get_state() # gets the new state based on the move
            training.append([self.state1, self.move1])

            
            # self.agent2.Qloss(state2)
            # self.agent2.back_prop(state2)  #should update based on the reward
            if frames > 200:
                self.game.view = True
            if self.game_over:
                for train in training:
                    state = train[0].copy()
                    state.append(frames)
                    self.agent1.Qloss(state,train[1])
                    losses.append(abs(self.agent1.loss))
                    self.agent1.Qback_prop(self.agent1.loss) 
                training = []
                

                self.games += 1
                self.num_frames.append(frames)
                frames = 0
                self.avg_losses.append(sum(losses)/len(losses) * 1000)
                if self.games % 100 == 0:
                    temp =self.avg_losses[-100:]
                    plt.close()
                    plt.plot(self.avg_losses)

                    plt.plot(self.num_frames)
                    plt.show(block = False)

                    if self.games % 500 == 0:
                        self.game.view = True
                else:
                    self.game.view = False
                self.game.reset()
        


