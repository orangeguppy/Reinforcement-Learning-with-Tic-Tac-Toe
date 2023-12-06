import random
import itertools
import utils
import logging

# logging.basicConfig(
#     filename='output.log',  # File name where logs will be stored
#     level=logging.INFO,     # Set the logging level (e.g., INFO, DEBUG, ERROR)
#     format='%(asctime)s - %(levelname)s - %(message)s'  # Format of the log message
# )

class HumanPlayer:
    def move(self):
        pass

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
    # The keys would be encoded combinations of the state-action pairs
    Q_table = {}
    initialised = False

    def __init__(self, epsilon=0.2, alpha=0.3, gamma=0.9):
        '''Step 1'''
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma

        if (not QLearner.initialised):
            QLearner.initialise_Q_table()

    '''Step 2 Methods'''
    '''Initialise all Q(S, A) = 0'''
    @classmethod
    def initialise_Q_table(self):
        all_states = utils.generate_possible_states() # Generate all possible states (all possible configurations of the game board)
        all_state_action_pairs = itertools.chain.from_iterable(
            utils.generate_all_state_action_pairs(state) for state in all_states
        )
        
        # Initialise entries for each state-action pair and its corresponding reward
        QLearner.Q_table = {entry: 0 for entry in all_state_action_pairs}
        QLearner.initialised = True
        logging.info(QLearner.Q_table)
     
    '''
    Step 3: Greedy-Epsilon strategy to pick an action
    This method is called by the Game Logic class when its the AI's turn to move
    '''
    @profile
    def move(self, possible_moves, state, char):
        # First choose between exploration and exploitation
        if (random.random() < self.epsilon): # Exploration
            (row, col) = random.choice(possible_moves)
            return (row, col, char)
        else: # Exploitation
            most_optimal_action = self.get_most_optimal_action(state)
            return most_optimal_action

    @profile
    def get_most_optimal_action(self, state):
        valid_actions = utils.generate_possible_actions_per_state(state)

        valid_pairs = [(key, QLearner.Q_table[key]) for key in QLearner.Q_table.keys() if key[0] == state and key[1] in valid_actions]

        if not valid_pairs:
            return None

        max_reward = float('-inf')
        maximising_actions = []

        for key, q_value in valid_pairs:
            if q_value > max_reward:
                max_reward = q_value
                maximising_actions = [key]
            elif q_value == max_reward:
                maximising_actions.append(key)

        if len(maximising_actions) == 1:
            return maximising_actions[0]
        else:
            return random.choice(maximising_actions)[1]


    # @profile
    # def get_most_optimal_action(self, state):
    #     valid_actions = utils.generate_possible_actions_per_state(state)
    #     valid_pairs = [key for key in QLearner.Q_table.keys() if key[0] == state and key[1] in valid_actions]

    #     if not valid_pairs:
    #         return None

    #     max_reward = float('-inf')
    #     maximising_actions = []

    #     for key in valid_pairs:
    #         q_value = QLearner.Q_table[key]
    #         if q_value > max_reward:
    #             max_reward = q_value
    #             maximising_actions = [key]
    #         elif q_value == max_reward:
    #             maximising_actions.append(key)

    #     if len(maximising_actions) == 1:
    #         return maximising_actions[0]
    #     else:
    #         return random.choice(maximising_actions)[1]

    # def get_most_optimal_action(self, state):
    #     # Get all valid actions for that state
    #     valid_actions = utils.generate_possible_actions_per_state(state)

    #     # Retrieve all rewards for each valid action for the current state
    #     valid_pairs = [key for key in QLearner.Q_table.keys() if key[0] == state and key[1] in valid_actions]
        
    #     if (len(valid_pairs) == 0):
    #         return None

    #     # Get the maximum reward possible, out of all possible actions
    #     maximum_reward = max(QLearner.Q_table[key] for key in QLearner.Q_table if key in valid_pairs)

    #     # Get the state-action pairs that return this maximum value
    #     maximising_actions = [key for key in self.Q_table.keys() if key in valid_pairs and self.Q_table[key] == maximum_reward]

    #     if (len(maximising_actions) == 1): # If there is only one action with the maximum reward
    #         ret = maximising_actions[0]
    #         # print("here")
    #         # print(ret)
    #         return ret
    #     else: # If more than one action returns the maximum reward, randomly return one of them
    #         ret = random.choice(maximising_actions)[1]
    #         # print("there")
    #         # print(ret)
    #         return ret

    
    '''Q(S, A) = Q(S, A) + alpha * (R + gamma * maxaQ(S', a) - Q(S, A))'''
    @profile
    def calculate_Q_new(self, s_old, s_new, action):
        # Old reward
        Q_old_reward = QLearner.Q_table[(s_old, action)]
        # print("s_old")
        # print(s_old)

        # print("s_new")
        # print(s_new)

        # print("action")
        # print(action)

        # Getting the action which maximises the new state
        action_maximising_new_state = self.get_most_optimal_action(s_new)

        # print("Action maximising new state")
        # print(action_maximising_new_state)

        # Q(S', A)
        if (action_maximising_new_state is not None):
            q_s_prime_a = QLearner.Q_table[(s_new, action_maximising_new_state)]

            # Get reward of the new state
            reward = self.calculate_reward(s_new, action[2]) # Pass in the current state of the board and the character being plotted

            # print("action again")
            # print(action)
            # print("s_old again")
            # print(s_old)
            # Update the Q table
            QLearner.Q_table[(s_old, action)] = Q_old_reward + self.alpha * (reward + self.gamma * (q_s_prime_a) - Q_old_reward)

            # Print updated entry
            # print(QLearner.Q_table[(s_old, action)])

    @profile
    def calculate_reward(self, s_new, char):
        if (utils.check_for_win_condition(s_new, char)):
            return 1
        elif (utils.check_for_win_condition(s_new, utils.get_opposing_char(char))):
            return -1
        else:
            return 0

q = QLearner()