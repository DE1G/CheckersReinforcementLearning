import random

import pygame
import sys

import pygame_menu

from Checkers_template.Gym import train_agent_vs_random
from Checkers_template.WindowState import WindowState
from Checkers_template.game_controls import check_inputs, check_esc
from Checkers_template.gui import update_board
from checkers_env import checkers_env
from LearningAgent import LearningAgent

# Constants
WIDTH, HEIGHT = 600, 600  # Window dimensions
ROWS, COLS = 6, 6  # Board dimensions
SQUARE_SIZE = WIDTH // COLS

# Initialize pygame
pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Load Checkers Environment
env = checkers_env()

Q_agent = LearningAgent(0.4, 0.5, 0.5, env, "qTable")

window_state = WindowState.MENU
training_mode = 0

def start_game():
    global window_state
    window_state = WindowState.PLAY
    MENU.disable()

def start_training():
    global window_state
    window_state = WindowState.TRAINING
    MENU.disable()
def set_training_mode(value, mode):
    global training_mode
    training_mode = mode

def play_random():
    global window_state
    window_state = WindowState.TEST
    MENU.disable()
def start_testplay():
    global window_state
    window_state = WindowState.SELF
    MENU.disable()

def initMenu():
    menu = pygame_menu.Menu('Welcome', 400, 300,
                            theme=pygame_menu.themes.THEME_BLUE)
    menu.add.button('PlayRL', start_game)
    menu.add.button('Play', start_testplay)
    menu.add.button('Train RL', start_training)
    menu.add.button('Test RL', play_random)
    menu.add.button('Quit', pygame_menu.events.EXIT)
    return menu

MENU = initMenu()


def main():
    global window_state
    run = True

    while run:
        if window_state == WindowState.MENU:
            MENU.mainloop(WIN)
        elif window_state == WindowState.TRAINING:
            while run:
                train_agent_vs_random(env,1000, Q_agent)
                window_state = WindowState.MENU
                MENU.enable()
        elif window_state == WindowState.TEST:
            r_wins = 0
            a_wins = 0
            print("start testing")
            for game in range(100):
                env.reset()
                current_player = -1
                moves_played = 0
                while run:
                    update_board(env, WIN, env.get_board(), current_player)
                    if current_player == -1:
                        actions = env.valid_moves(current_player)
                        action = random.choice(actions)
                        env.move_piece(current_player, action)
                    elif current_player == 1:
                        Q_agent.select_action(current_player)
                        env.move_piece(current_player, Q_agent.select_action(current_player))
                    current_player = -current_player
                    moves_played += 1
                    winner = env.game_winner()

                    if moves_played >= 400:
                        print("to many moves")
                        break
                    if winner is not None:
                        if winner == -1:
                            a_wins += 1
                        elif winner == 1:
                            r_wins += 1
                        print("Player", winner, "wins!")
                        break
            print("agent:", a_wins)
            print("r:", r_wins)
            window_state = WindowState.MENU
            MENU.enable()
        elif window_state == WindowState.SELF:
            env.reset()
            selected_piece = None
            current_player = -1

            while run:
                update_board(env, WIN, env.get_board(), current_player, selected_piece)
                current_player, selected_piece = check_inputs(env, env.get_board(), current_player, selected_piece)
                winner = env.game_winner()

                if winner is not None:
                    print("Player", winner, "wins!")
                    window_state = WindowState.MENU
                    MENU.enable()
                    break

                if check_esc():
                    window_state = WindowState.MENU
                    MENU.enable()
                    break
        else:
            env.reset()
            selected_piece = None
            current_player = -1

            while run:
                update_board(env, WIN, env.get_board(), current_player, selected_piece)
                if current_player == -1:
                    current_player, selected_piece = check_inputs(env, env.get_board(), current_player, selected_piece)
                elif current_player == 1:
                    Q_agent.select_action(current_player)
                    env.move_piece(current_player, Q_agent.select_action(current_player))
                    current_player = -current_player
                winner = env.game_winner()

                if winner is not None:
                    print("Player", winner, "wins!")
                    window_state = WindowState.MENU
                    MENU.enable()
                    break

                if check_esc():
                    window_state = WindowState.MENU
                    MENU.enable()
                    break


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()



