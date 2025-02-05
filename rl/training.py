import copy
import random
import time

import pandas as pd
from matplotlib import pyplot as plt

from gui.game_controls import check_esc


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
    print("current win %:", win_percentage[len(win_percentage) - 1])



def train_agent_vs_random(env, episodes, agent):
    """
    Train the agent using Q-learning.

    :param env: environment
    :param agent: The agent trained that shall be trained against random moves
    :param episodes: Number of games to play for training before plotting and saving
    """
    rl_agent_total_wins_history = [0] # for plotting progress
    side = 1 # side that agent will play on
    i = -1 # for keeping track of iterations
    back_to_menu = False

    games_played = 0
    moves_played = 0
    start_time = time.time()
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
            board = copy.copy(env.get_board())
            while True:
                # Select and perform an action
                action = agent.select_action(side)
                env.move_piece(side, action)
                moves_played += 1

                winner = env.game_winner()

                if winner is None:
                    next_state = get_next_state(env, side)
                    moves_played += 1
                    winner = env.game_winner()

                reward = agent.evaluate_board(board, env.get_board(), side, winner)

                agent.update_QTable((state, action), next_state, side, reward)

                # Move to the next state and switch players
                state = next_state
                board = copy.copy(env.get_board())

                back_to_menu = check_esc()
                if back_to_menu or winner is not None:
                    break

            # Update win history for plot
            if winner == side:
                rl_agent_total_wins_history.append(rl_agent_total_wins_history[len(rl_agent_total_wins_history) - 1] + 1)
            else:
                rl_agent_total_wins_history.append(rl_agent_total_wins_history[len(rl_agent_total_wins_history) - 1])

            # Decay epsilon after each episode
            agent.epsilon = max(0.01, agent.epsilon * 0.998)
            games_played += 1
            if back_to_menu:
                break
        print("--- %s seconds ---" % (time.time() - start_time))
        agent.save_QTable()
        print("--- %s seconds ---" % (time.time() - start_time))
        plot_game_history_percentage(rl_agent_total_wins_history)

        if back_to_menu:
            break

def train_agent_vs_agent(env, episodes, agent):
    """
    Train the agent using Q-learning.

    :param env: environment
    :param agent: The agent trained that shall be trained against random moves
    :param episodes: Number of games to play for training
    """
    side = 1 # side that agent will play on
    i = -1 # for keeping track of iterations
    back_to_menu = False
    moves_played = 0
    games_played = 0
    while True:
        i += 1
        for episode in range(episodes):
            #Print info
            if episode % 1000 == 0:
                print("learning...")
                print ("episode: ", i * episodes)

            #reset board switch side and set starting states
            env.reset()

            states = []
            boards = []
            actions = []

            states.append((tuple(env.get_board().flatten()), side))
            boards.append(copy.copy(env.get_board()))

            moves_since_capture = 0

            while True:

                # Select and perform an action
                action = agent.select_action(side)
                env.move_piece(side, action)
                moves_since_capture += 1
                if len(action[4]) > 0:
                    moves_since_capture = 0
                moves_played += 1

                winner = env.game_winner(moves_since_capture)

                side = -side
                # Move to the next state and switch players
                states.append((tuple(env.get_board().flatten()), side))
                boards.append(copy.copy(env.get_board()))
                actions.append(action)

                if winner is not None:
                    if winner == -side:
                        reward = agent.evaluate_board(boards[1], env.get_board(), -side, winner)

                        agent.update_QTable((states[0], actions[0]), states[2], -side, reward)
                    else:
                        reward = agent.evaluate_board(boards[0], env.get_board(), side, winner)

                        agent.update_QTable((states[0], actions[0]), states[2], side, reward)

                elif len(states) == 3:
                    reward = agent.evaluate_board(boards[0], env.get_board(), side, winner)

                    agent.update_QTable((states[0], actions[0]), states[2], side, reward)

                    states.pop(0)
                    boards.pop(0)
                    actions.pop(0)

                back_to_menu = check_esc()
                if back_to_menu or winner is not None:
                    break

            # Decay epsilon after each episode
            agent.epsilon = max(0.01, agent.epsilon * 0.998)
            games_played += 1

            if back_to_menu:
                break

        agent.save_QTable()
        print(moves_played/games_played)
        if back_to_menu:
            break

def train_agent_vs_random_until_converge_return_final_winrate(env, agent, convergence_value):
    wins = 0
    episodes = 0
    last_win_percentage = float("-inf")
    side = 1  # side that agent will play on
    while True:
        for episode in range(1000):
            # reset board switch side and set starting states
            env.reset()
            side = -side
            next_state = None
            state = (tuple(env.get_board().flatten()), side)
            board = copy.copy(env.get_board())
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
                board = copy.copy(env.get_board())
                if winner is not None:
                    if winner == side:
                        wins += 1
                    break
            # Decay epsilon after each episode
            agent.epsilon = max(0.01, agent.epsilon * 0.99)

        episodes += 1000
        if wins/episodes - last_win_percentage < convergence_value or wins/episodes >= 0.95:
            break
        last_win_percentage = wins/episodes
    print(episodes)
    return wins / episodes