'''
Module: UI (User Interface for Tic-Tac-Toe Game)

This module provides a user interface using the Pygame library for the Tic-Tac-Toe game.
It defines the `UI` class responsible for initializing the game window, rendering the game board,
capturing mouse clicks, drawing Xs and Os, displaying status messages, and handling UI-related actions.

Usage:
    The `UI` class can be instantiated to create a graphical user interface for the Tic-Tac-Toe game.
'''

import pygame

class UI:

    '''Initialize the Pygame window and UI elements'''
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")
        
        # Initialise pygame window, surface to draw on, and game font
        self.ttt = pygame.display.set_mode((225, 250))
        self.surface = pygame.Surface(self.ttt.get_size())
        self.surface = self.surface.convert()
        self.font = pygame.font.Font(None, 18)

        # Draw the board
        self.draw_lines()

        # Render the UI
        self.running = True
        self.render()

    '''Update the main Pygame display with the contents of the UI surface'''
    def render(self):
        # Update the main display with the contents of self.surface
        self.ttt.blit(self.surface, (0, 0))
        pygame.display.flip()

    '''Draw the grid lines for the Tic-Tac-Toe board'''
    def draw_lines(self):
        self.surface.fill((250, 250, 250))
        # Horizontal lines
        pygame.draw.line(self.surface, (0, 0, 0), (75, 0), (75, 225), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (150, 0), (150, 225), 2)
        
        # Vertical lines
        pygame.draw.line(self.surface, (0, 0, 0), (0,75), (225, 75), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,150), (225, 150), 2)

    '''Capture mouse clicks and return the row, column, and character selected'''
    def mouseClick(self, char):
        event = pygame.event.wait()
        while event.type != pygame.MOUSEBUTTONDOWN: # Wait for the human player to click on the square to place their character
            event = pygame.event.wait()
        
        (mouseX, mouseY) = pygame.mouse.get_pos() # Get the position of the mouse cursor
        row = int(mouseY / 225 * 3)
        col = int(mouseX / 225 * 3)

        # Check if the mouse position is within the bounds
        # Only render Xs and Os if the cursor is on the game board
        if self.checkWithinBound(mouseX, mouseY):
            self.drawMove(char, row, col)
        self.render()
        return (row, col, char)

    '''Draw Xs and Os on the game board'''
    def drawMove(self, char, row, col):
        # Get coordinates of the centre of the grid space
        centreX = ((col) * 75) + 32
        centreY = ((row) * 75) + 32
        text = self.font.render(char, 1, (10, 10, 10))
        self.surface.blit(text, (centreX, centreY))

    '''Display status messages on the UI'''
    def showStatus(self, statusMessage):
        text = self.font.render(statusMessage, 1, (10, 10, 10))
        text_width, text_height = self.font.size(statusMessage)  # Get the width and height of the rendered text

        # Fill the background rectangle with a light gray color
        self.surface.fill((250, 250, 250), (10, 230, 214, 24))

        # Blit the rendered text onto the surface
        self.surface.blit(text, (10 + 10, 230 + 5))  # Position the text with some padding within the background rectangle

        # Update the UI
        self.render()

    '''Check if the mouse click is within the bounds of the game board. Only allow the player to place characters within the bounds of the game board'''
    def checkWithinBound(self, posX, posY):
        if (posX < 0 or posX > 225 or posY < 0 or posY > 225):
            return False
        return True