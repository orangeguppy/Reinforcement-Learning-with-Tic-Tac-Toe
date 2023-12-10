'''
Module: Game Controller

This module defines the `Game_Controller` class, which orchestrates the gameplay logic, manages player moves,
and facilitates the interaction between the game logic, player strategies, and user interface (if provided).

The `Game_Controller` class controls the sequence of gameplay, training of Q-Learners, and updates the game's status.
It collaborates with the `Game_Logic` module for game-specific logic, player modules for strategies, and the `ui` module for the user interface.

Classes:
    - Game_Controller: Orchestrates the gameplay, training, and interaction between the game logic and UI.

Usage:
    This module can be used as part of a larger application implementing a game, providing a structured interface to control gameplay, training,
    and interfacing with the user interface.
'''

import time
import logging

from game_logic import Game_Logic
import players
import ui
import utils

class Game_Controller:
    '''This method initialises the Game_Controller Object'''
    def __init__(self, game_logic, ui=None):
        self.ui = ui
        self.game_logic = game_logic

    '''This method controls the sequence of gameplay'''
    def play_game(self):
        if (self.ui is not None):
            self.ui.showStatus("Game has started")

        # Initialise all possible moves
        possible_moves = self.game_logic.possible_moves()

        # Continue alternating between players until there are no moves left or someone has won
        while (len(self.game_logic.possible_moves()) > 0 and self.game_logic.winner is None):
            if (self.game_logic.playerX_turn): # Player X's turn
                # Current board state
                self.game_logic.playerX.last_board = self.game_logic.board
                
                # Pick an action
                (row, col, char) = self.game_logic.playerX.move(self.game_logic.possible_moves(), self.game_logic.board, 'X')

                # Execute the action
                self.plot_char('X', row, col)
            else: # Player O's turn
                # Current board state
                self.game_logic.playerO.last_board = self.game_logic.board
                
                # Pick an action
                (row, col, char) = self.game_logic.playerO.move(self.game_logic.possible_moves(), self.game_logic.board, 'O')

                # Execute the action
                self.plot_char('O', row, col)
                

            # Update the winner if any and update the UI
            self.game_logic.update_winner()
            if (self.ui is not None):
                self.ui.render()

            # Update the Q-Rewards after each turn
            if (isinstance(self.game_logic.playerX, players.QLearner) and isinstance(self.game_logic.playerO, players.QLearner)):
                s_new = self.game_logic.board # New board state

                # Possible moves for each player
                playerX_possible_moves = utils.generate_possible_actions_per_state(s_new, 'X')
                playerO_possible_moves = utils.generate_possible_actions_per_state(s_new, 'O')

                # Reward from Player X's POV
                reward = self.game_logic.playerX.calculate_reward(s_new, 'X')

                # Calculate the new Q table
                if (abs(reward) == 1 or abs(reward) == 0.5): # Game has ended
                    self.game_logic.playerX.calculate_Q_new(reward, s_new, playerX_possible_moves)
                    self.game_logic.playerO.calculate_Q_new(-1 * reward, s_new, playerO_possible_moves)
                elif (reward == 0 and self.game_logic.playerX_turn): # Game is ongoing
                    self.game_logic.playerO.calculate_Q_new(-1 * reward, s_new, playerO_possible_moves)
                elif (reward == 0 and not self.game_logic.playerX_turn): # Game is ongoing
                    self.game_logic.playerX.calculate_Q_new(reward, s_new, playerX_possible_moves)

            # End the current player's turn
            self.game_logic.playerX_turn = not self.game_logic.playerX_turn
        
        self.game_logic.update_winner()
        self.print_status()
        return

    '''Train the Q-Learners for a specified number of epochs, where each epoch is a game'''
    def train(self, num_epochs):
        counter = 0
        while counter < num_epochs:
            self.play_game()
            counter += 1
            self.game_logic.reset_board()
            print(counter)

    '''Update the board, and UI if applicable, after each move'''
    def plot_char(self, char, row, col):
        # Record the move in the backend game logic
        self.game_logic.plot_char(char, row, col)

        # Update the UI
        if (self.ui is not None):
            self.ui.drawMove(char, row, col)

    '''Print the game's result on the terminal, and on the UI if applicable'''
    def print_status(self):
        if (self.game_logic.winner == None):
            print("Draw!")
            if (self.ui is not None):
                self.ui.showStatus("Draw!")
        else:
            print("Winner is", self.game_logic.winner)
            if (self.ui is not None):
                self.ui.showStatus(self.game_logic.get_winner_status_msg())