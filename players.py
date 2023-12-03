import random
class HumanPlayer:
    pass

class RandomPlayer:
    def __init__(self):
        pass
    
    def move(self, possible_moves):
        return random.choice(possible_moves)