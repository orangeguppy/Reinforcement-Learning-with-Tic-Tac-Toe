import random
import itertools

class HumanPlayer:
    pass
    def move(self):
        pass

class RandomPlayer:
    def __init__(self):
        self.name = random.choice(['Alice', 'Bob', 'Cat'])
    
    def move(self, possible_moves):
        return random.choice(possible_moves)
    
    def __str__(self):
        return self.name

class QLearner:

    '''
    OVERVIEW
        Steps of the epsilon algorithm
        1. Initialise alpha = (0, 1], small epsilon > 0, gamma
        2. Initialise all Q(s, a), except terminal, = 0, and initialise the first state S (this is done in game_logic)
        3. For each Episode:
                Choose A from S using policy derived from Q
                Take action A, observe R, S'
                Q(S, A) = Q(S, A) + alpha * (R + gamma * maxaQ(S', a) - Q(S, A))
                S = S'
            until S is terminal

        In the context of this Tic-Tac-Toe game,
        State: The positions of all characters currently on the board
        Action: Picking the coordinates of the location to plot a character
        Reward:
            -1 -- Loss
             0 -- Draw
             1 -- Win
    '''

    def __init__(self, epsilon=0.2, alpha=0.1, gamma=0.5):
        '''Step 1'''
        self.episilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        # self.last_action

        '''Step 2'''
        # The key would be an encoded combination of the state-action pairs
        self.Q_table = {}
        self.initialise_Q_table()

    '''Step 2 Methods'''
    def initialise_Q_table(self):
        all_states = self.generate_possible_states() # Generate all possible states
        all_state_action_pairs = []
        for state in all_states:
            all_pairs_per_state = self.generate_all_state_action_pairs(state)
            all_state_action_pairs.extend(all_pairs_per_state)
        print(all_state_action_pairs[0])


    def generate_possible_states(self):
        possible_symbols = ['X', 'O', ' ']
        all_possible_states = []
        for symbol_permutation in itertools.product(possible_symbols, repeat=9):
            temp_board = tuple(tuple(symbol_permutation[i * 3:(i + 1) * 3]) for i in range(3))
            all_possible_states.append(temp_board)
        return all_possible_states

    def generate_possible_actions_per_state(self, state):
        moves = []
        for i in range(3):
            for j in range(3):
                if state[i][j] == ' ':
                    moves.append((i, j))
        if len(moves) == 0:
            self.done = True
        return moves

    def generate_all_state_action_pairs(self, state):
        actions = self.generate_possible_actions_per_state(state)
        state_action_pairs = []
        for action in actions:
            state_action_pairs.append((state, action))
        return state_action_pairs
     
    def move(self, possible_moves, state):
        # First choose between exploration and exploitation
        if (random.random() < self.epsilon): # Exploration
            return random.choice(possible_moves)
        else: # Exploitation
            most_optimal_action = self.get_most_optimal_action(state)
            return 
            pass

    def get_most_optimal_action(self, state):
        # First get all actions which can be taken in the current state
        pass

QLearner()