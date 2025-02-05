import csv

from skopt import gp_minimize
from skopt.space import Real
from skopt.utils import use_named_args

from training import train_agent_vs_random_until_converge_return_final_winrate
from LearningAgent import LearningAgent
from CheckersEnv import CheckersEnv
import time

start_time = time.time()

# Define the parameter space for Bayesian Optimization
search_space = [
    Real(0.3, 0.62, name="learning_rate"),  # Range for learning rate
    Real(0.5, 1.0, name="epsilon"),  # Range for epsilon
    Real(0.5, 0.7, name="discount_factor"),  # Range for discount factor
    Real(0.75, 1.0, name="win_reward_weight"),
    Real(0.0, 1.0, name="capturing_king_reward_weight"),
    Real(0.0, 0.75, name="capturing_pieces_reward_weight"),
]

# Define the objective function
@use_named_args(search_space)
def objective(learning_rate, epsilon, discount_factor, win_reward_weight, capturing_king_reward_weight,
                          capturing_pieces_reward_weight):
    # Initialize the environment and agent
    env = CheckersEnv()
    env.initialize_board()
    agent = LearningAgent(
        env=env,
        agent_name="BayesianOptimizedAgent",
        learning_rate=learning_rate,
        epsilon=epsilon,
        discount_factor=discount_factor
    )

    agent.set_reward_weights(
        win_reward_weight=win_reward_weight,
        capturing_king_reward_weight=capturing_king_reward_weight,
        capturing_pieces_reward_weight=capturing_pieces_reward_weight,
    )

    # Train the agent and evaluate performance
    winrate = train_agent_vs_random_until_converge_return_final_winrate(env, agent, 0.01)  # Replace with your evaluation metric

    print("--- %s seconds ---" % (time.time() - start_time))
    # Negate the reward since Bayesian Optimization minimizes the objective
    return -winrate


# Run Bayesian Optimization
result = gp_minimize(
    func=objective,
    dimensions=search_space,
    n_calls=20,  # Number of evaluations
    random_state=42,  # For reproducibility
)


with open("hyperparameters" + ".csv", "a") as f:
    w = csv.writer(f)
    w.writerow(result.x)
print("Hyperparameters saved")

print(result.x)
print("--- %s seconds ---" % (time.time() - start_time))


'''
n_calls: 100
    Real(0.3, 0.62, name="learning_rate"),  # Range for learning rate
    Real(0.5, 1.0, name="epsilon"),  # Range for epsilon
    Real(0.5, 0.7, name="discount_factor"),  # Range for discount factor
    Real(0.75, 1.0, name="win_reward_weight"),
    Real(0.0, 1.0, name="capturing_king_reward_weight"),
    Real(0.0, 0.7, name="king_reward_weight"),
    Real(0.45, 0.75, name="capturing_pieces_reward_weight"),
    Real(0.5, 0.7, name="pieces_reward_weight"),
Hyperparameters saved
[0.32323811614749237, 0.5476741737937393, 0.6331140624572354, 0.9653299462498443, 0.9591391192114755, 0.6167831369434786, 0.707875146770339, 0.698302861463449]
--- 4362.927885055542 seconds ---
'''