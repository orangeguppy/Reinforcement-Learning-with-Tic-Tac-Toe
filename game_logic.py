class Game_Logic:
    def __init__(self, training=False):
        # Set training state
        self.training = training

        # Initialise game board
        self.board = [
            [' ', ' ', ' '],
            [' ', ' ', ' '],
            [' ', ' ', ' ']]
        
        # Initialise game states
        self.done = False
        self.winner = None
        
        # Set players
        self.playerX = None
        self.playerO = None

        # Initialise turn
        self.playerX_turn = None

    def print_board(self):
        print(self.board)

    def plot_char(self, char, row, col):
        if (self.board[row][col] is None):
            self.board[row][col] = char
            return True
        return False

    def evaluate_board(self):
        if (self.check_winner('X')):
            self.done = True
        elif (self.check_winner('O')):
            self.done = True

    def check_winner(self, player):
        # Check rows, columns, and diagonals for a winning combination
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or all(self.board[j][i] == player for j in range(3)):
                return True
        if (all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3))):
            return True
        return False

    def play_game(self):
        while (self.done is False):
            if (playerX_turn):
                playerX.move(self.possible_moves)
                self.plot_char('X', row, col)
            else:
                playerO.move(self.possible_moves)
                self.plot_char('O', row, col)
        self.end_game()

    def end_game(self):
        pass

    def possible_moves(self):
        moves = []
        for row in self.board:
            for col in row:
                if (self.board[row][col] == ' '):
                    moves.append((row, col))
        return moves