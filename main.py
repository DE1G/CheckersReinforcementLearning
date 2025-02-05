import random

import pygame
import sys

from game.gamemodes import player_vs_player, test_agent_vs_random, player_vs_agent
from gui.Menu import Menu
from rl.training import train_agent_vs_random, train_agent_vs_agent
from gui.WindowState import WindowState
from game.CheckersEnv import CheckersEnv
from rl.LearningAgent import LearningAgent

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
Q_agent = None

def main():
    global Q_agent
    run = True

    while run:
        if MENU.window_state == WindowState.MENU:
            MENU.enable()
            MENU.run(WIN)
            continue

        if MENU.window_state == WindowState.SELF:
            player_vs_player(WIN, MENU, env)
            continue

        if Q_agent is None or  Q_agent.agent_name != MENU.agent_name:
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
            test_agent_vs_random(WIN, MENU, env, Q_agent, 200)
        else:
            player_vs_agent(WIN, MENU, env, Q_agent)


    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()



