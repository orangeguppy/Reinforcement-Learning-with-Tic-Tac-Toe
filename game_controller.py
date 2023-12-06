import players
from game_logic import Game_Logic
import ui
import time
import utils

class Game_Controller:
    def __init__(self, ui, game_logic):
        self.ui = ui
        self.game_logic = game_logic

    def play_game(self):
        self.ui.showStatus("Game has started")
        # Print the status of the board
        self.game_logic.print_board()

        # Initialise all possible moves
        possible_moves = self.game_logic.possible_moves()

        # Continue alternating between players until there are no moves left or someone has won
        while (len(self.game_logic.possible_moves()) > 0 and self.game_logic.winner is None):
            # Current board state
            s_old = self.game_logic.board
            if (self.game_logic.playerX_turn):
                # Pick an action
                row, col = self.game_logic.playerX.move(self.game_logic.possible_moves(), self.game_logic.board)
                self.plot_char('X', row, col)
                # s_new = self.game_logic.board # New board state
                # self.playerX.calculate_Q_new(s_old, s_new, (row, col, 'X')) # Update the Q_table
                self.game_logic.playerX_turn = False
            else:
                row, col = self.game_logic.playerO.move(self.game_logic.possible_moves(), self.game_logic.board)
                self.plot_char('O', row, col)
                # s_new = self.game_logic.board # New board state
                # self.game_logic.playerO.calculate_Q_new(s_old, s_new, (row, col, 'O')) # Update the Q_table
                self.game_logic.playerX_turn = True

            # Update the winner if any and print the board
            self.game_logic.print_board()
            self.game_logic.update_winner()
            self.ui.render()
            time.sleep(2)

        # There are no more moves and the game has ended
        self.game_logic.print_board()
        self.game_logic.update_winner()
        if (self.game_logic.winner == None):
            print("Draw!")
            self.ui.showStatus("Draw!")
        else:
            print("Winner is", self.game_logic.winner)
            self.ui.showStatus(self.game_logic.get_winner_status_msg())
        time.sleep(1)
        return

    def plot_char(self, char, row, col):
        # Record the move in the backend game logic
        self.game_logic.plot_char(char, row, col)

        # Update the UI
        self.ui.drawMove(char, row, col)

playerX = players.RandomPlayer()
playerO = players.RandomPlayer()
ui = ui.UI()

game_logic = Game_Logic(playerX, playerO)

game_controller = Game_Controller(ui, game_logic)
game_controller.play_game()