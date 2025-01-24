
import random
import numpy as np
import csv
import os.path

class LearningAgent:

    def __init__(self, learning_rate, epsilon, discount_factor, env, agent_name):
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
        self.agent_name = agent_name
        if os.path.exists(agent_name + ".csv"):
            print(agent_name + " loading Q-table ...")
            with open(agent_name + ".csv", mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    key_tuple = eval(row[0])
                    value = float(row[1])
                    self.q_table[key_tuple] = value
            print(agent_name + " Q-table loaded")


    def evaluate_board(self, board, next_board, side, winner = None):

        reward = 0

        # Assign rewards for piece differences
        pieces_player = np.count_nonzero((next_board == side) | (next_board == 2 * side))
        pieces_enemy = np.count_nonzero((next_board == -side) | (next_board == -2 * side))
        before_pieces_player = np.count_nonzero((board == side) | (board == 2 * side))
        before_pieces_enemy = np.count_nonzero((board == -side) | (board == -2 * side))

        reward += (pieces_player - pieces_enemy) * 2
        reward -= (before_pieces_player - pieces_player) * 5
        reward += (before_pieces_enemy - pieces_enemy) * 5

        # Additional rewards for kings
        before_kings_player = np.count_nonzero(board == 2 * side)
        before_kings_enemy = np.count_nonzero(board == -2 * side)
        kings_player = np.count_nonzero(next_board == 2 * side)
        kings_enemy = np.count_nonzero(next_board == -2 * side)

        reward += kings_player
        reward -= (before_kings_player - kings_player) * 3
        reward += (before_kings_enemy - kings_enemy) * 3

        if winner == side:
            reward += 5
        elif winner == -side:
            reward -= 5
        elif winner == 0:
            reward -= 2

        return reward

    def select_action(self, side):
        """
        Choose an action using an epsilon-greedy policy.

        :param side: The current side the agent plays on
        :return: Selected action
        """

        valid_actions = self.env.valid_moves(side)
        if random.random() < self.epsilon:
            # Exploration: Random action
            return random.choice(valid_actions)

        # Exploitation: Best action based on Q-values
        board = tuple(self.env.get_board().flatten())
        state = (board, side)
        best_action = None
        max_q_value = float('-inf')

        for action in valid_actions:
            q_value = self.q_table.get((state, (action[0], action[1], action[2], action[3])), 0)
            if q_value > max_q_value:
                max_q_value = q_value
                best_action = action

        return best_action if best_action else random.choice(valid_actions)


    def update_QTable(self, state_action, next_state, side, reward):

        valid_actions = self.env.valid_moves(side)

        # Q-learning update
        next_q = max(
        [self.q_table.get((next_state, (a[0], a[1], a[2], a[3])), 0) for a in valid_actions],
        default=0
        )

        current_q = self.q_table.get(state_action, 0)
        self.q_table[
        state_action] = current_q + self.step_size * (
            reward + self.discount_factor * next_q - current_q
        )

    def save_QTable(self):
        with open(self.agent_name + ".csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerows(self.q_table.items())
        print(self.agent_name + " Q-table saved")