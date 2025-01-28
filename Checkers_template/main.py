import random

import numpy as np
import pygame
import sys

from Checkers_template.Menu import Menu
from Checkers_template.training import train_agent_vs_random
from Checkers_template.WindowState import WindowState
from Checkers_template.game_controls import check_inputs, check_esc
from Checkers_template.gui import update_board
from CheckersEnv import CheckersEnv
from LearningAgent import LearningAgent

#for reproducibility
random.seed(42)

# Constants
WIDTH, HEIGHT = 600, 600  # Window dimensions
ROWS, COLS = 6, 6  # Board dimensions
SQUARE_SIZE = WIDTH // COLS

# Initialize pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Initialize Menu
MENU = Menu()

# Load Checkers Environment
env = CheckersEnv()

agent_name = "qTable"

def set_agent_name(name):
    global agent_name
    agent_name = name

def main():
    run = True

    while run:
        if MENU.window_state == WindowState.MENU:
            MENU.enable()
            MENU.run(WIN)
            continue
        if MENU.window_state == WindowState.SELF:
            env.reset()
            selected_piece = None
            current_player = -1

            while run:
                update_board(env, WIN, env.get_board(), current_player, selected_piece)
                current_player, selected_piece = check_inputs(env, env.get_board(), current_player, selected_piece)
                winner = env.game_winner()

                if winner is not None:
                    print("Player", winner, "wins!")
                    MENU.window_state = WindowState.MENU
                    break

                if check_esc():
                    MENU.window_state = WindowState.MENU
                    break

        Q_agent = LearningAgent(env, agent_name)
        if MENU.window_state == WindowState.TRAINING:
            train_agent_vs_random(env,1000, Q_agent)
            MENU.window_state = WindowState.MENU
        elif MENU.window_state == WindowState.TEST:
            r_wins = 0
            a_wins = 0
            print("start testing")
            won_games_move_count = []
            lost_games_move_count = []
            agent_side = random.choice([1,-1])
            for game in range(1000):
                env.reset()
                agent_side = -agent_side
                current_player = -1
                moves_played = 0
                while run:
                    update_board(env, WIN, env.get_board(), current_player)
                    if current_player == -agent_side:
                        actions = env.valid_moves(current_player)
                        action = random.choice(actions)
                        env.move_piece(current_player, action)
                    elif current_player == agent_side:
                        env.move_piece(current_player, Q_agent.select_action(current_player, False))
                    current_player = -current_player
                    moves_played += 1
                    winner = env.game_winner()

                    if winner is not None:
                        if winner == -agent_side:
                            lost_games_move_count.append(moves_played)
                            r_wins += 1
                        elif winner == agent_side:
                            won_games_move_count.append(moves_played)
                            a_wins += 1
                        print("Player", winner, "wins!")
                        break
            print("agent:", a_wins)
            print("r:", r_wins)
            print("games lost average moves played:", np.mean(lost_games_move_count))
            print("games won average moves played:", np.mean(won_games_move_count))
            MENU.window_state = WindowState.MENU
        else:
            env.reset()
            selected_piece = None
            current_player = -1

            while run:
                update_board(env, WIN, env.get_board(), current_player, selected_piece)
                if current_player == -1:
                    current_player, selected_piece = check_inputs(env, env.get_board(), current_player, selected_piece)
                elif current_player == 1:
                    env.move_piece(current_player, Q_agent.select_action(current_player, False))
                    current_player = -current_player
                winner = env.game_winner()

                if winner is not None:
                    print("Player", winner, "wins!")
                    MENU.window_state = WindowState.MENU
                    break

                if check_esc():
                    MENU.window_state = WindowState.MENU
                    break


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()



