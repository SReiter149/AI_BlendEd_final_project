from layers_stable import Drop_Out_Layer, Activation_Layer, FC_Layer
from network_stable import Network
from functions_stable import pong_loss, sigmoid
import numpy as np
from numpy import random


class agent:
    def __init__(self, game):
        self.game = game
        self.set_up()

        self.move1 = False #down
        self.move2 = True #up
    def set_up(self):
        self.agent1 = Network(pong_loss)
        self.agent1.add(FC_Layer((6,24), bias_true=True))
        self.agent1.add(Activation_Layer())
        self.agent1.add(FC_Layer((24,1), bias_true=True))

        #self.agent2 = Network(pong_loss)
        #self.agent2.add(FC_Layer((6,24), bias_true=True))
        #self.agent2.add(Activation_Layer())
        #self.agent2.add(FC_Layer((24,1), bias_true=True))

    def get_action(self, state1, state2):
        state1 = np.array(state1, dtype = float)
        prediction = self.agent1.forward_prop(state1)
        #print(prediction.shape)
        # I don't remember making it 3 dimensional
        self.move1 = bool(round(prediction[0][0][0]))
        
        #state2 = np.array(state1, dtype = float)
        #prediction = self.agent2.forward_prop(state2)
        #self.move2 = bool(round(prediction[0]))
        self.move2 = bool(round(prediction[0][0][0]))

    def main(self):
        game_over, state1, state2 = self.game.get_state()
        while True:
            self.get_action(state1, state2)
            self.game.machine_play_frame(self.move1, self.move2)  # will update the game based on the move
            game_over, state1, state2 = self.game.get_state() # gets the new state based on the move
            self.agent1.Qloss(state1)
            self.agent1.back_prop(state1) 
            
            self.agent2.Qloss(state2)
            self.agent2.back_prop(state2)  #should update based on the reward
            if game_over:
                self.game.reset()

