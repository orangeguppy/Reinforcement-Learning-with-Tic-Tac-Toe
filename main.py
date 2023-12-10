import players
from ui import UI
from game_controller import Game_Controller
from game_logic import Game_Logic
import logging

def random_players():
    playerX = players.RandomPlayer()
    playerO = players.RandomPlayer()
    ui = ui.UI()

    game_logic = Game_Logic(playerX, playerO)

    game_controller = Game_Controller(game_logic, ui)
    game_controller.play_game()

# Training the QLearners
def train(num_epochs):
    playerX = players.QLearner()
    playerO = players.QLearner()

    game_logic = Game_Logic(playerX, playerO)

    game_controller = Game_Controller(game_logic, None)
    game_controller.train(num_epochs)

    # Save the Q tables
    playerX.saveQtable("playerXstates")
    playerO.saveQtable("playerOstates")

 # QLearner vs Human
def play_against_ai():
    ui = UI()
    playerX = players.QLearner()
    playerX.loadQtable("playerXstates")
    logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(playerX.Q_table)
    playerO = players.HumanPlayer(ui)
    game_logic = Game_Logic(playerX, playerO)
    game_controller = Game_Controller(game_logic, ui)
    game_controller.play_game()
    print(game_controller.game_logic.board)

# train(20000)
while(True):
    play_against_ai()