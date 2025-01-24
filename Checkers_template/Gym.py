
import csv
import random

import pandas as pd
import pygame
from matplotlib import pyplot as plt

from Checkers_template.game_controls import check_esc


def get_next_state(env, side):

    if env.game_winner() is None:
        random_action = random.choice(env.valid_moves(-side))
        env.move_piece(-side, random_action)

    next_state = (tuple(env.get_board().flatten()), side)

    return next_state



def plot_game_history_percentage(game_history):
    win_percentage = []

    for game in range(len(game_history)):
        win_percentage.append(game_history[game] / (game + 1))

    pd.Series(win_percentage).plot()
    plt.ylim(0.4, 1)
    plt.show()



def train_agent_vs_random(env, episodes, agent):
    """
    Train the agent using Q-learning.

    :param env: environment
    :param agent: The agent trained that shall be trained against random moves
    :param episodes: Number of games to play for training
    """
    rl_agent_total_wins_history = [0] # for plotting progress
    side = 1 # side that agent will play on
    i = -1 # for keeping track of iterations
    back_to_menu = False
    while True:
        i += 1
        for episode in range(episodes):
            #Print info
            if episode % 1000 == 0:
                print("learning...")
                print ("episode: ", i * episodes)

            #reset board switch side and set starting states
            env.reset()
            side = -side
            next_state = None
            state = (tuple(env.get_board().flatten()), side)
            board = env.get_board()

            while True:
                # Select and perform an action
                action = agent.select_action(side)
                env.move_piece(side, action)

                winner = env.game_winner()

                if winner is None:
                    next_state = get_next_state(env, side)
                    winner = env.game_winner()


                reward = agent.evaluate_board(board, env.get_board(), side, winner)

                agent.update_QTable((state, action), next_state, side, reward)

                # Move to the next state and switch players
                state = next_state
                board = env.get_board()

                back_to_menu = check_esc()
                if back_to_menu or winner is not None:
                    break

            # Update win history for plot
            if winner == side:
                rl_agent_total_wins_history.append(rl_agent_total_wins_history[len(rl_agent_total_wins_history) - 1] + 1)
            else:
                rl_agent_total_wins_history.append(rl_agent_total_wins_history[len(rl_agent_total_wins_history) - 1])

            # Decay epsilon after each episode
            agent.epsilon = max(0.01, agent.epsilon * 0.99)

            if back_to_menu:
                break

        plot_game_history_percentage(rl_agent_total_wins_history)
        agent.save_QTable()

        if back_to_menu:
            break