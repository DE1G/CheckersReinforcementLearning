#env = checkers_env.checkers_env(player = 1)
#env.render()

import pygame
import sys
import random

from Checkers_template.game_controls import check_inputs
from Checkers_template.gui import update_board
from checkers_env import checkers_env
from LearningAgent import LearningAgent

# Constants
WIDTH, HEIGHT = 600, 600  # Window dimensions
ROWS, COLS = 6, 6  # Board dimensions
SQUARE_SIZE = WIDTH // COLS

# Initialize pygame
pygame.init()

# Load Checkers Environment
env = checkers_env()
agent = LearningAgent(0.2, 0.5, 0.8, env)


def main():
    run = True
    selected_piece = None
    current_player = -1

    agent.learning(6000)

    print("finishedTraining")
    env.reset()
    '''
    randomPlayer = 0
    rlAgent = 0

    for testMatch in range(100):
        while True:
            update_board(env, WIN, env.get_board(), current_player, selected_piece)
            if current_player == -1:
                valid_actions = env.valid_moves(-1)
                action = random.choice(valid_actions)
                env.move_piece(current_player, action)
            elif current_player == 1:
                agent.select_action(current_player)
                env.move_piece(current_player, agent.select_action(current_player))
            current_player = -current_player
            winner = env.game_winner(env.get_board())

            if winner is not None:
                print("Player", winner, "wins!")
                if winner == 1:
                    rlAgent += 1
                elif winner == -1:
                    randomPlayer += 1
                env.reset()
                current_player = -1
                selected_piece = None
                break

    print("Random Player wins: ", randomPlayer)
    print("RL Agent wins: ", rlAgent)

    env.reset()
    '''
    while run:
        update_board(env, WIN, env.get_board(), current_player, selected_piece)
        if current_player == -1:
            current_player, selected_piece = check_inputs(env, env.get_board(), current_player, selected_piece)
        elif current_player == 1:
            agent.select_action(current_player)
            env.move_piece(current_player, agent.select_action(current_player))
            current_player = -current_player
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



