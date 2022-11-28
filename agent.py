from layers_stable import Drop_Out_Layer, Activation_Layer, FC_Layer
from network_stable import Network
from functions_stable import pong_loss, sigmoid

class agent:
    def __init__(self, game, network):
        self.game = game
        self.network1 = Network(pong_loss)

        self.network1.add(FC_Layer((6,24)))
        self.network1.add(Activation_Layer())
        self.network2 = network(sigmoid)

    def main(self):
        game_over, state1, state2 = self.game.get_state()
        while not game_over:
            move1 = self.network1(state1)
            move2 = self.network2(state2)
            self.game.machine_play_frame(move1, move2)  # will update the game based on the move
            game_over, state1, state2 = self.game.get_state() # gets the new state based on the move
            self.network1.update(state1)  # should update based on the reward
            self.network2.update(state2)
              
