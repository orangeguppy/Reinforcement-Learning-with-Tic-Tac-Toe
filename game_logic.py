'''
Module: Game Logic

This module defines the `Game_Logic` class that handles the game's core logic, including game setup, player moves, 
checking for a winner, managing the game board, and resetting the game state.

Class:
    Game_Logic: Manages game setup, player moves, and game state for a Tic-Tac-Toe-like game.

Usage:
    This class can be utilized within a larger application or game implementation requiring core game logic for a 
    Tic-Tac-Toe-like game.
'''
import random

import players
import utils

class Game_Logic:

    '''Initialise and setup a new game'''
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

    '''Get all possible moves given a configuration of the game board'''
    def possible_moves(self):
        moves = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ' ']
        if not moves:
            self.done = True
        return moves

    '''Plot a character on the board and save it'''
    def plot_char(self, char, row, col):
        board_list = list(list(row_tuple) for row_tuple in self.board)
        if board_list[row][col] == ' ':
            board_list[row][col] = char
            self.board = tuple(tuple(row_tuple) for row_tuple in board_list)
            return True
        return False

    '''Check if any player won, and save the player who won if any'''
    def update_winner(self):
        # Boolean for evaluating the win condition
        if utils.check_for_win_condition(self.board, 'X'):
            self.winner = self.playerX
        elif utils.check_for_win_condition(self.board, 'O'):
            self.winner = self.playerO

    '''Clear the game board'''
    def reset_board(self):
        self.board = (
            (' ', ' ', ' '),
            (' ', ' ', ' '),
            (' ', ' ', ' ')
        )
        self.winner = None

    '''Represent the game's result as a string'''
    def get_winner_status_msg(self):
        if self.winner is None:
            return "Draw"
        else:
            winner_str = str(self.winner) + " won the game!"
            return winner_str

    '''Print the status of the board'''
    def print_board(self):
        for row in self.board:
            print(row)
        print()
