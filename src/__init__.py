import itertools, random
from card import *
from player import *
from central_Area import *
from card_Game import *

# The main entry of the card game
if __name__ == '__main__':
    while True:
        # Ask user whether to start a new game
        playGame = raw_input("Do you want to play a new game ('y' or 'n') ? ")
        if playGame != 'Y' and playGame != 'y': break # Exit the game
        else:
            # Choose the type of the opponent
            opponentType = raw_input("Opponent type: aggressive ('a') or acquisative ('q'): ")
            aggressive = (opponentType == 'A' or opponentType == 'a')

            # Initialise the players and the central area
            central  = Central('central', [], 5, [], [])       
            player   = Player ('player',   30, [], [], 5, [], [], 0, 0) 
            computer = Player ('computer', 30, [], [], 5, [], [], 0, 0)

            # Initialise the game
            initialise_Game(player, computer, central) 

        # Starts the game turn by turn, every turn check whether anyone wins the game
        while True: 
            stopPlay = player_Turn(player, computer, central)
            if stopPlay == True: break # The player wins the game, end game turn
            stopPlay = computer_Turn(player, computer, central, aggressive)
            if stopPlay == True: break # The computer wins the game, end game turn

