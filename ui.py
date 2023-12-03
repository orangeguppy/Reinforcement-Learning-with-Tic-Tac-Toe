import pygame

class UI:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")
        
        # Initialise pygame window, surface to draw on, and game font
        self.ttt = pygame.display.set_mode((250, 250))
        self.surface = pygame.Surface(self.ttt.get_size())
        self.surface = self.surface.convert()
        self.font = pygame.font.Font(None, 18)

        # Draw the board
        self.draw_lines()

        # Render the UI
        self.running = True
        self.render()

    def render(self):
        while self.running:
            # Update the main display with the contents of self.surface
            self.ttt.blit(self.surface, (0, 0))
            pygame.display.flip()

            # Stop rendering the UI if the game is exited
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

    def draw_lines(self):
        self.surface.fill((250, 250, 250))
        # Horizontal lines
        pygame.draw.line(self.surface, (0, 0, 0), (75, 0), (75, 225), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (150, 0), (150, 225), 2)
        
        # Vertical lines
        pygame.draw.line(self.surface, (0, 0, 0), (0,75), (225, 75), 2)
        pygame.draw.line(self.surface, (0, 0, 0), (0,150), (225, 150), 2)

UI()