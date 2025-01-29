
import random
import numpy as np
import csv
import os.path

class LearningAgent:

    def __init__(self, env, agent_name, learning_rate = None, epsilon = None, discount_factor = None, parameters_line = 1 ):
        """
        Initialize the LearningAgent.

        :param learning_rate: Learning rate (alpha)
        :param epsilon: Exploration rate
        :param discount_factor: Discount factor (gamma)
        :param env: The checkers environment instance
        """
        self.learning_rate = learning_rate
        self.epsilon = epsilon
        self.discount_factor = discount_factor
        self.env = env
        self.q_table = {}  # Dictionary for Q-values
        self.agent_name = agent_name

        reward_weights = []

        with open("hyperparameters.csv", mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader) #skip names line
            for i in range(parameters_line):
                row = next(reader)
            if learning_rate is None:
                self.learning_rate = float(row[0])
            if epsilon is None:
                self.epsilon = float(row[1])
            if discount_factor is None:
                self.discount_factor = float(row[2])
            for i in range(3):
                reward_weights.append(float(row[3+i]))


        self.win_reward_weight = reward_weights[0]
        self.capturing_king_reward_weight = reward_weights[1]
        self.capturing_pieces_reward_weight = reward_weights[2]



    def evaluate_board(self, board, next_board, side, winner = None, moves = 0):

        # Assign rewards for piece differences
        pieces_player = np.count_nonzero((next_board == side) | (next_board == 2 * side))
        pieces_enemy = np.count_nonzero((next_board == -side) | (next_board == -2 * side))
        before_pieces_player = np.count_nonzero((board == side) | (board == 2 * side))
        before_pieces_enemy = np.count_nonzero((board == -side) | (board == -2 * side))

        #For capturing/ losing pieces
        capturing_pieces_reward = 0
        capturing_pieces_reward -= (before_pieces_player - pieces_player)

        # Additional rewards for kings
        before_kings_player = np.count_nonzero(board == 2 * side)
        before_kings_enemy = np.count_nonzero(board == -2 * side)
        kings_player = np.count_nonzero(next_board == 2 * side)
        kings_enemy = np.count_nonzero(next_board == -2 * side)

        #making, capturing or losing king
        capturing_king_reward = 0
        capturing_king_reward -= (before_kings_player - kings_player)

        win_reward = 0
        if winner == side:
            win_reward += 1
        elif winner == -side:
            win_reward -= 1
        elif winner == 0:
            win_reward -= 0.2

        reward = (win_reward * self.win_reward_weight +
                  capturing_king_reward * self.capturing_king_reward_weight +
                  capturing_pieces_reward * self.capturing_pieces_reward_weight)
        return reward

    def select_action(self, side, use_e_greedy = True):
        """
        Choose an action using an epsilon-greedy policy.

        :param use_e_greedy: determines if agent is greedy
        :param side: The current side the agent plays on
        :return: Selected action
        """

        valid_actions = self.env.valid_moves(side)
        if random.random() < self.epsilon and use_e_greedy:
            # Exploration: Random action
            return random.choice(valid_actions)

        # Exploitation: Best action based on Q-values
        board = tuple(self.env.get_board().flatten())
        state = (board, side)
        best_action = None
        max_q_value = float('-inf')

        for action in valid_actions:
            q_value = self.q_table.get((state, action), 0)
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
        state_action] = current_q + self.learning_rate * (
            reward + self.discount_factor * next_q - current_q
        )

    def save_QTable(self):
        with open("./Q_tables/" + self.agent_name + ".csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerows(self.q_table.items())
        print(self.agent_name + " Q-table saved")

    def load_QTable(self):
        if os.path.exists("./Q_tables/" + self.agent_name + ".csv"):
            print(self.agent_name + " loading Q-table ...")
            with open("./Q_tables/" + self.agent_name + ".csv", mode='r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    state_tuple = eval(row[0])
                    q_value = float(row[1])
                    self.q_table[state_tuple] = q_value
            print(self.agent_name + " Q-table loaded")
        else:
            print("There is no exising Q-table for the agent: " + self.agent_name)

    def set_reward_weights(self, win_reward_weight, capturing_king_reward_weight,
                          capturing_pieces_reward_weight):
        self.win_reward_weight = win_reward_weight
        self.capturing_king_reward_weight = capturing_king_reward_weight
        self.capturing_pieces_reward_weight = capturing_pieces_reward_weight
