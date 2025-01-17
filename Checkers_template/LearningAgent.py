import checkers_env
import math
import random
import matplotlib
import matplotlib.pyplot as plt
from collections import namedtuple, deque
from itertools import count
import numpy as np
import pandas as pd

class LearningAgent:

    def __init__(self, learning_rate, epsilon, discount_factor, env):
        """
        Initialize the LearningAgent.

        :param learning_rate: Learning rate (alpha)
        :param epsilon: Exploration rate (initial value)
        :param discount_factor: Discount factor (gamma)
        :param env: The checkers environment instance
        """
        self.step_size = learning_rate
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.env = env
        self.q_table = {}  # Dictionary for Q-values

    def evaluation(self, board_before, board, player):
        """
        Evaluate the board and return an intermediate reward.

        :param board: The current board state
        :param player: The current player
        :return: Reward for the board state
        """
        reward = 0

        # Assign rewards for piece differences
        pieces_player1 = np.count_nonzero((board == 1) | (board == 2))
        pieces_player2 = np.count_nonzero((board == -1) | (board == -2))
        before_pieces_player1 = np.count_nonzero((board_before == 1) | (board_before == 2))
        before_pieces_player2 = np.count_nonzero((board_before == -1) | (board_before == -2))
        reward += (pieces_player1 - pieces_player2)
        reward += ((pieces_player1 - pieces_player2) - (before_pieces_player1 - before_pieces_player2)) * 3

        # Additional rewards for kings
        before_kings_player1 = np.count_nonzero(board_before == 2)
        before_kings_player2 = np.count_nonzero(board_before == -2)
        kings_player1 = np.count_nonzero(board == 2)
        kings_player2 = np.count_nonzero(board == -2)
        reward += (kings_player1 - kings_player2) * 2 * player
        reward += ((kings_player1- kings_player2) - (before_kings_player1 - before_kings_player2)) * 2


        return reward

    def select_action(self, player):
        """
        Choose an action using an epsilon-greedy policy.

        :param player: The current player
        :return: Selected action
        """
        state = tuple(self.env.get_board().flatten())
        valid_actions = self.env.valid_moves(player)

        if random.random() < self.epsilon:
            # Exploration: Random action
            return random.choice(valid_actions)

        # Exploitation: Best action based on Q-values
        best_action = None
        max_q_value = float('-inf')

        for action in valid_actions:
            q_value = self.q_table.get((state, (action[0], action[1], action[2], action[3])), 0)
            if q_value > max_q_value:
                max_q_value = q_value
                best_action = action

        return best_action if best_action else random.choice(valid_actions)

    def learning(self, episodes):
        print("Hello")
        """
        Train the agent using Q-learning.

        :param episodes: Number of games to play for training
        """
        rl_agent_win_series = [0]

        for episode in range(episodes):
            self.env.reset()
            state = tuple(self.env.get_board().flatten())
            player = 1  # Start with Player 1

            while True:
                # Select and perform an action
                action = self.select_action(player)
                self.env.move_piece(player, action)

                winner = self.env.game_winner(self.env.get_board())

                if winner is None:
                    #Make other player makes random move
                    random_valid_actions = self.env.valid_moves(-1)
                    random_action = random.choice(random_valid_actions)
                    self.env.move_piece(-1, random_action)

                # Get the next state and reward
                next_state = tuple(self.env.get_board().flatten())
                reward = self.evaluation(state, self.env.get_board(), player)

                # Check if the game is over
                winner = self.env.game_winner(self.env.get_board())
                if winner is not None:
                    if winner == player:
                        reward += 15  # Reward for winning
                    elif winner == -player:
                        reward -= 15  # Penalty for losing
                    else:
                        reward += 0  # Neutral reward for draw

                valid_actions = self.env.valid_moves(player)

                # Q-learning update
                best_next_q = max(
                    [self.q_table.get((next_state, (a[0], a[1], a[2], a[3])), 0) for a in valid_actions],
                    default=0
                )

                current_q = self.q_table.get((state, (action[0], action[1], action[2], action[3])), 0)
                self.q_table[(state, (action[0], action[1], action[2], action[3]))] = current_q + self.step_size * (
                    reward + self.discount_factor * best_next_q - current_q
                )

                # Break if the game is over
                if winner is not None:
                    break

                # Move to the next state and switch players
                state = next_state
            if winner == 1:
                rl_agent_win_series.append(rl_agent_win_series[len(rl_agent_win_series) - 1] + 1)
            else:
                rl_agent_win_series.append(rl_agent_win_series[len(rl_agent_win_series) - 1])
            # Decay epsilon after each episode
            self.epsilon = max(0.01, self.epsilon * 0.995)

        for game in range(len(rl_agent_win_series)):
            rl_agent_win_series[game] = rl_agent_win_series[game] / (game + 1)
        pd.Series(rl_agent_win_series).plot()
        plt.ylim(0.4, 1)
        plt.show()