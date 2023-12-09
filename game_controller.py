import players
from game_logic import Game_Logic
import ui
import time
import utils
import logging

class Game_Controller:
    def __init__(self, game_logic, ui=None):
        self.ui = ui
        self.game_logic = game_logic

    def play_game(self):
        if (self.ui is not None):
            self.ui.showStatus("Game has started")

        # Initialise all possible moves
        possible_moves = self.game_logic.possible_moves()

        # Continue alternating between players until there are no moves left or someone has won
        while (len(self.game_logic.possible_moves()) > 0 and self.game_logic.winner is None):
            if (self.game_logic.playerX_turn):
                # Current board state
                s_old = self.game_logic.board
                # Pick an action
                (row, col, char) = self.game_logic.playerX.move(self.game_logic.possible_moves(), self.game_logic.board, 'X')
                self.plot_char('X', row, col)
                if (isinstance(self.game_logic.playerX, players.QLearner)):
                    s_new = self.game_logic.board # New board state
                    self.game_logic.playerX.calculate_Q_new(s_old, s_new, (row, col, 'X')) # Update the Q_table
                self.game_logic.playerX_turn = False
            else:
                # Current board state
                s_old = self.game_logic.board
                (row, col, char) = self.game_logic.playerO.move(self.game_logic.possible_moves(), self.game_logic.board, 'O')
                self.plot_char('O', row, col)
                if (isinstance(self.game_logic.playerO, players.QLearner)):
                    s_new = self.game_logic.board # New board state
                    self.game_logic.playerO.calculate_Q_new(s_old, s_new, (row, col, 'O')) # Update the Q_table
                self.game_logic.playerX_turn = True

            # Update the winner if any and print the board
            # self.game_logic.print_board()
            self.game_logic.update_winner()
            if (self.ui is not None):
                self.ui.render()
            # time.sleep(2)

        # There are no more moves and the game has ended
        # self.game_logic.print_board()

        if (isinstance(self.game_logic.playerO, players.QLearner)):
            self.game_logic.playerX.calculate_Q_new(s_old, s_new, (row, col, 'X')) # Update the Q_table
            self.game_logic.playerO.calculate_Q_new(s_old, s_new, (row, col, 'O')) # Update the Q_table
        self.game_logic.update_winner()
        if (self.game_logic.winner == None):
            print("Draw!")
            if (self.ui is not None):
                self.ui.showStatus("Draw!")
        else:
            print("Winner is", self.game_logic.winner)
            if (self.ui is not None):
                self.ui.showStatus(self.game_logic.get_winner_status_msg())
        # time.sleep(1)
        return

    def plot_char(self, char, row, col):
        # Record the move in the backend game logic
        self.game_logic.plot_char(char, row, col)

        # Update the UI
        if (self.ui is not None):
            self.ui.drawMove(char, row, col)

    def train(self, num_epochs):
        counter = 0
        while counter < num_epochs:
            self.play_game()
            counter += 1
            self.game_logic.reset_board()
            print(counter)
        logging.info("Final table")