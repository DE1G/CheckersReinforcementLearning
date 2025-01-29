import random

import pygame
import sys

from Checkers_template.Menu import Menu
from Checkers_template.training import train_agent_vs_random, train_agent_vs_agent
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

#Intialize Learning Agent
Q_agent = LearningAgent(env, "QTable", parameters_line=2)

def main():
    global Q_agent
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
            continue
        if Q_agent.agent_name != MENU.agent_name:
            Q_agent = LearningAgent(env, MENU.agent_name, parameters_line=2)
        if len(Q_agent.q_table.items()) == 0:
            Q_agent.load_QTable()
        if MENU.window_state == WindowState.TRAINING:
            if MENU.training_mode == 1:
                print("Agent vs Random")
                train_agent_vs_random(env,1000, Q_agent)
            else:
                print("Agent vs Agent")
                train_agent_vs_agent(env,1000, Q_agent)
            MENU.window_state = WindowState.MENU
        elif MENU.window_state == WindowState.TEST:
            r_wins = 0
            a_wins = 0
            print("start testing")
            agent_side = random.choice([1,-1])
            for game in range(200):
                env.reset()
                agent_side = -agent_side
                current_player = -1
                moves_since_capture = 0
                while run:
                    update_board(env, WIN, env.get_board(), current_player)
                    if current_player == -agent_side:
                        actions = env.valid_moves(current_player)
                        action = random.choice(actions)
                    else:
                        action = Q_agent.select_action(current_player, False)
                    env.move_piece(current_player, action)

                    moves_since_capture += 1
                    if len(action[4]) > 1:
                        moves_since_capture = 0
                    current_player = -current_player

                    winner = env.game_winner(moves_since_capture)
                    if winner is not None:
                        if winner == -agent_side:
                            r_wins += 1
                        elif winner == agent_side:
                            a_wins += 1
                        break
            print("agent:", a_wins)
            print("r:", r_wins)
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



