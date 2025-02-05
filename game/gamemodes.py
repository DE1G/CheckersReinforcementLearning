import random

from gui.WindowState import WindowState
from gui.game_controls import check_inputs, check_esc
from gui.gui import update_board


def player_vs_agent(win, menu, env, Q_agent):
    env.reset()
    selected_piece = None
    current_player = -1

    while True:
        update_board(env, win, env.get_board(), current_player, selected_piece)
        if current_player == -1:
            current_player, selected_piece = check_inputs(env, env.get_board(), current_player, selected_piece)
        elif current_player == 1:
            env.move_piece(current_player, Q_agent.select_action(current_player, False))
            current_player = -current_player
        winner = env.game_winner()

        if winner is not None:
            print("Player", winner, "wins!")
            menu.window_state = WindowState.MENU
            break

        if check_esc():
            menu.window_state = WindowState.MENU
            break

def player_vs_player(win, menu, env):
    env.reset()
    selected_piece = None
    current_player = -1

    while True:
        update_board(env, win, env.get_board(), current_player, selected_piece)
        current_player, selected_piece = check_inputs(env, env.get_board(), current_player, selected_piece)
        winner = env.game_winner()

        if winner is not None:
            print("Player", winner, "wins!")
            menu.window_state = WindowState.MENU
            break

        if check_esc():
            menu.window_state = WindowState.MENU
            break

def test_agent_vs_random(win, menu, env, Q_agent, games):
    r_wins = 0
    a_wins = 0
    print("start testing")
    agent_side = random.choice([1, -1])
    for game in range(games):
        env.reset()
        agent_side = -agent_side
        current_player = -1
        moves_since_capture = 0
        while True:
            update_board(env, win, env.get_board(), current_player)
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
    menu.window_state = WindowState.MENU