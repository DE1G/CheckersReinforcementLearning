#env = checkers_env.checkers_env(player = 1)
#env.render()

import pygame
import sys

from Checkers_template.game_controls import check_inputs
from Checkers_template.gui import update_board
from checkers_env import checkers_env

# Constants
WIDTH, HEIGHT = 600, 600  # Window dimensions
ROWS, COLS = 6, 6  # Board dimensions
SQUARE_SIZE = WIDTH // COLS

# Initialize pygame
pygame.init()

# Load Checkers Environment
env = checkers_env()



def main():
    run = True
    selected_piece = None
    current_player = -1

    while run:
        update_board(env, WIN, env.get_board(), current_player, selected_piece)
        current_player, selected_piece = check_inputs(env, env.get_board(), current_player, selected_piece)
        winner = env.game_winner(env.get_board())

        if winner is not None:
            print("Player", winner, "wins!")
            env.reset()
            current_player = -1
            selected_piece = None

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Checkers")
    main()



