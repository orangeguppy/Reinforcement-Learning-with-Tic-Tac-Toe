import random
import itertools
import utils
import logging
import pickle

class HumanPlayer:
    def __init__(self, ui):
        self.ui = ui

    def move(self, possible_moves, state, char):
        return self.ui.mouseClick(char)

class RandomPlayer:
    def __init__(self):
        self.name = random.choice(['Alice', 'Bob', 'Cat'])
    
    def move(self, possible_moves, state=None, char=None):
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

    '''Step 2'''
    def __init__(self, epsilon=0.2, alpha=0.3, gamma=0.98, training=False):
        '''Step 1'''
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.training = training

        '''Step 2: Lazy-Loading the Q Table. I initially initialised all possible state-action combinations but it was really slow.'''
        self.Q_table = {}
        self.Q_last = 0.0
        self.state_action_last = None
        self.last_board = None
     
    '''
    Step 3: Greedy-Epsilon strategy to pick an action
    This method is called by the Game Logic class when its the AI's turn to move
    '''
    def move(self, possible_moves, state, char):
        if (self.training is False):
            most_optimal_action = self.get_most_optimal_action(state, char)
            return most_optimal_action

        # First choose between exploration and exploitation
        if (random.random() < self.epsilon): # Exploration
            (row, col) = random.choice(possible_moves)
            # Save the latest state-action pair
            self.state_action_last = (state, (row, col, char))
            # Save the old Q_value estimate which will be updated at the next iteration
            self.Q_last = self.getQ(state, (row, col, char))
            return (row, col, char)
        else: # Exploitation
            most_optimal_action = self.get_most_optimal_action(state, char)
            return most_optimal_action

    def get_most_optimal_action(self, state, char):
        Q_list = []
        valid_actions = utils.generate_possible_actions_per_state(state, char)
        for action in valid_actions:
            Q_list.append(self.getQ(state, action))

        if len(Q_list) == 0:
            return None
        maxQ = max(Q_list) # Get the best move out of all available moves that are recorded in the Q Table

        # If there is more than one best action, randomly pick one
        if Q_list.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(valid_actions)) if Q_list[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = Q_list.index(maxQ)
        self.state_action_last = (state, valid_actions[i])
        self.Q_last = self.getQ(state, valid_actions[i])
        return valid_actions[i]

    def getQ(self, state, action): # get Q states
        if(self.Q_table.get((state, action))) is None:
            self.Q_table[(state, action)] = 1.0
        return self.Q_table.get((state, action))

    '''Q(S, A) = Q(S, A) + alpha * (R + gamma * maxaQ(S', a) - Q(S, A))'''
    def calculate_Q_new(self, s_new, char):
        # Get the most optimal action for the new state
        action_maximising_new_state = self.get_most_optimal_action(s_new, char)

        # Q(S', A)
        if (action_maximising_new_state is not None):
            q_s_prime_a = self.getQ(s_new, action_maximising_new_state)
        else:
            q_s_prime_a = 0

        # Get reward of the new state
        reward = self.calculate_reward(s_new, char) # Pass in the current state of the board and the character being plotted
        self.Q_table[self.state_action_last] = self.getQ(self.state_action_last[0], self.state_action_last[1]) + self.alpha * (reward + self.gamma * (q_s_prime_a) - self.getQ(self.state_action_last[0], self.state_action_last[1]))

    def calculate_reward(self, s_new, char):
        if (utils.check_for_win_condition(s_new, char)):
            return 1
        elif (utils.check_for_win_condition(s_new, utils.get_opposing_char(char))):
            return -1
        elif (self.check_board_complete(s_new) is False):
            return 0
        else:
            return 0.5

    def check_board_complete(self, board):
        for row in board:
            for char in row:
                if char == ' ':
                    return False
        return True

    def saveQtable(self, file_name):  #save table
        with open(file_name, 'wb') as handle:
            pickle.dump(self.Q_table, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def loadQtable(self, file_name): # load table
        with open(file_name, 'rb') as handle:
            self.Q_table = pickle.load(handle)