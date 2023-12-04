import players
class Game_Logic:
    def __init__(self, playerX, playerO, training=False):
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
        self.playerX = playerX
        self.playerO = playerO

        # Print assignments
        print("Player X is", self.playerX)
        print("Player O is", self.playerO)

        # Initialise turn
        self.playerX_turn = False

    def print_board(self):
        for row in self.board:
            print(row)
        print()

    def plot_char(self, char, row, col):
        if (self.board[row][col] == ' '):
            self.board[row][col] = char
            return True
        return False

    def evaluate_board(self):
        if (self.check_winner('X')):
            self.done = True
        elif (self.check_winner('O')):
            self.done = True

    def check_winner(self):
        # Boolean for evaluating the win condition
        if (self.check_for_win_condition('X')):
            self.winner = self.playerX
        elif (self.check_for_win_condition('O')):
            self.winner = self.playerO

    def check_for_win_condition(self, player):
        # Check rows, columns, and diagonals for a winning combination
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or all(self.board[j][i] == player for j in range(3)):
                return True
        if (all(self.board[i][i] == player for i in range(3)) or all(self.board[i][2 - i] == player for i in range(3))):
            return True
        return False

    def play_game(self):
        self.print_board()
        possible_moves = self.possible_moves()
        while (len(self.possible_moves()) > 0 and self.winner is None):
            if (self.playerX_turn):
                row, col = playerX.move(self.possible_moves())
                self.plot_char('X', row, col)
                self.playerX_turn = False
            else:
                row, col = playerO.move(self.possible_moves())
                self.plot_char('O', row, col)
                self.playerX_turn = True

            # Update the winner if any and print the board
            self.print_board()
            self.check_winner()
        
        # There are no more moves and the game has ended
        self.check_winner()
        if (self.winner == None):
            print("Draw!")
        else:
            print("Winner is", self.winner)
        return

    def end_game(self):
        print(self.winner)

    def possible_moves(self):
        moves = []
        for i in range(3):
            for j in range(3):
                if (self.board[i][j] == ' '):
                    moves.append((i, j))
        if (len(moves) == 0):
            self.done = True
        return moves

playerX = players.RandomPlayer()
playerO = players.RandomPlayer()

game_logic = Game_Logic(playerX, playerO)
game_logic.play_game()