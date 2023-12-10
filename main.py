import logging

from game_controller import Game_Controller
from game_logic import Game_Logic
import players
from ui import UI

'''Method to train the Q-Learning agents'''
def train(num_epochs):
    # Create the Q-Learning agents
    playerX = players.QLearner()
    playerO = players.QLearner()

    # Create a Game Logic handler
    game_logic = Game_Logic(playerX, playerO)

    # Create a Game Controller object to orchestrate the various classes
    game_controller = Game_Controller(game_logic, None)
    game_controller.train(num_epochs)

    # Save the Q-tables
    playerX.saveQtable("playerXstates")
    playerO.saveQtable("playerOstates")

'''Method to play against trained AI Q-Learner'''
def play_against_ai():
    # Create a UI for players to interact with
    ui = UI()

    # Create the player objects
    playerO = players.HumanPlayer(ui) # Human
    playerX = players.QLearner() # Q_Learner
    playerX.loadQtable("playerXstates") # Load the Q-tables

    # For logging. Can be commented out if you want.
    logging.basicConfig(filename='output.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(playerX.Q_table)
    
    # Same as before in the train() method
    game_logic = Game_Logic(playerX, playerO)
    game_controller = Game_Controller(game_logic, ui)
    game_controller.play_game()

    # Print the initial board
    print(game_controller.game_logic.board)

# The code below trains the Q-Learners and then lets you play against them
train(50000)
while(True):
    play_against_ai()