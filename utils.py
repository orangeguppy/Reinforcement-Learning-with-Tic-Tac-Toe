'''Utility functions for the game board'''
import itertools

'''Generate all permutations of the Tic-Tac-Toe board, each permutation is a state S in Q(S, A)'''
def generate_possible_states():
    possible_symbols = ['X', 'O', ' ']
    all_possible_states = []
    for symbol_permutation in itertools.product(possible_symbols, repeat=9):
        temp_board = tuple(tuple(symbol_permutation[i * 3:(i + 1) * 3]) for i in range(3))
        all_possible_states.append(temp_board)
    return all_possible_states

'''Encode each state S and set of corresponding actions A in the form Q(S, A)'''
def generate_all_state_action_pairs(state):
    actions = generate_possible_actions_per_state(state)
    state_action_pairs = []
    for action in actions:
        state_action_pairs.append((state, action))
    return state_action_pairs

'''For a specific permutation (state S) of the Tic-Tac-Toe board, generate all available actions'''
def generate_possible_actions_per_state(state):
    moves = []
    for i, row in enumerate(state):
        for j, cell in enumerate(row):
            if cell == ' ':
                moves.extend([(i, j, 'X'), (i, j, 'O')])
    return moves

'''Check if a win condition has been fulfilled for any player'''
def check_for_win_condition(board, char):
    # Check rows, columns, and diagonals for a winning combination
    for i in range(3):
        if all(board[i][j] == char for j in range(3)) or all(board[j][i] == char for j in range(3)):
            return True
    if all(board[i][i] == char for i in range(3)) or all(board[i][2 - i] == char for i in range(3)):
        return True
    return False

'''Get the opposing character'''
def get_opposing_char(char):
    if (char == 'X'):
        return 'O'
    else:
        return 'X'