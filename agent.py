class agent():
    def __init__(self, game, network):
        self.game = game
        self.network = network
        pass

    def main(self):
        state, game_over = self.game.get_state()
        while not game_over:
            move = self.network(state)
            self.game.update(move) #will update the game based on the move
            reward = self.game.reward()
            self.network.update(reward) #should update based on the reward
            state, game_over = self.game.get_state() #gets the new state based on the move



