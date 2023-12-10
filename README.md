# Reinforcement-Learning-with-Tic-Tac-Toe
Using model-free Q-Learning to play Tic-Tac-Toe.

# How to run
Clone the repository and run
`python3 main.py`
to train the Q-Learning agents and then play against the trained agent. Alternatively, you can comment out the line
`train(50000)`
to immediately play against a pre-trained Q-Learning agent

# Key lessons learnt
1. Using lazy-loading for initialising the Q-table is very important. I tried to initialise all possible permutations of states and actions at first, but it greatly slowed training time.
2. I initialised updated the Q-Table like this (pseudocode):
   
  a) Player's turn

  b) Record board state

  c) Update Q-Table for the playing player immediately.

But this was wrong. The agent only learned that it was supposed to try to place 3 characters in a row, but did not learn that it was supposed to try and block the opponent from winning at the same time.
I fixed this problem by only updating each player's state after the opponent has played (refer to the Game_Controller class to see the exact order)

# References
Class materials from CS420(Introduction to AI) at SMU
