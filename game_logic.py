import players
import utils
import random

class Game_Logic:
    def __init__(self, playerX, playerO, training=False):
        # Set training state
        self.training = training

        # Initialise game board as a tuple of tuples
        self.board = (
            (' ', ' ', ' '),
            (' ', ' ', ' '),
            (' ', ' ', ' ')
        )
        
        # Initialise game states
        self.done = False
        self.winner = None
        
        # Set players
        self.playerX = playerX
        self.playerO = playerO

        # Initialise turn
        self.playerX_turn = random.choice([True, False])

    def print_board(self):
        for row in self.board:
            print(row)
        print()

    def plot_char(self, char, row, col):
        board_list = list(list(row_tuple) for row_tuple in self.board)
        if board_list[row][col] == ' ':
            board_list[row][col] = char
            self.board = tuple(tuple(row_tuple) for row_tuple in board_list)
            return True
        return False

    def update_winner(self):
        # Boolean for evaluating the win condition
        if utils.check_for_win_condition(self.board, 'X'):
            self.winner = self.playerX
        elif utils.check_for_win_condition(self.board, 'O'):
            self.winner = self.playerO

    def end_game(self):
        print(self.winner)

    def possible_moves(self):
        moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
        if not moves:
            self.done = True
        return moves

    def get_winner_status_msg(self):
        if self.winner is None:
            return "Draw"
        else:
            winner_str = str(self.winner) + " won the game!"
            return winner_str

    def reset_board(self):
        self.board = (
            (' ', ' ', ' '),
            (' ', ' ', ' '),
            (' ', ' ', ' ')
        )
        self.winner = None
