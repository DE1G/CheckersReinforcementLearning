

import numpy as np


class checkers_env:

    def __init__(self, board=None, player=None):

        self.board = self.initialize_board()


    def initialize_board(self):
        board = np.array([[1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [-1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1]])
        return board


    def reset(self):
        self.board = np.array([[1, 0, 1, 0, 1, 0],
                      [0, 1, 0, 1, 0, 1],
                      [0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0],
                      [-1, 0, -1, 0, -1, 0],
                      [0, -1, 0, -1, 0, -1]])


    def valid_moves(self, player):
        '''
        A possible format could be [start_row, start_col, end_row, end_col, prevMoves], there are normal moves and moves with capture. Pieces could be king or normal. The prevMoves is only introduced if there is a double jump involved.
        '''
        moves = []
        capture_moves = []

        for row in range(6):
            for col in range(6):
                if self.board[row, col] == 0 or -player == self.board[row, col] or -2 * player == self.board[row, col]:
                    continue

                if self.board[row, col] == player:
                    piece_directions = [(1, 1), (1, -1)] if player == 1 else [(-1, 1), (-1, -1)]
                else:
                    piece_directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

                capture_moves += self.find_capture_moves_for_piece(row, col, player, piece_directions)

                for i in range(len(capture_moves)):
                    next_captures = self.find_capture_moves_for_piece(capture_moves[i][2], capture_moves[i][3], player, piece_directions)
                    if len(next_captures) > 0:
                        capture_moves[i] = (capture_moves[i][0], capture_moves[i][1], next_captures[0][2], next_captures[0][3], [capture_moves[i], next_captures[0]])



                for dr, dc in piece_directions:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < 6 and 0 <= nc < 6 and self.board[nr, nc] == 0:
                        moves.append((row, col, nr, nc))  # Normal move
        return capture_moves if len(capture_moves) > 0 else moves


    def find_capture_moves_for_piece(self, row, col, player, piece_directions):
        '''
        Find all capture moves for a player
        '''
        capture_moves = []
        for dr, dc in piece_directions:
            nr, nc = row + dr, col + dc

            # Check for captures
            capture_r, capture_c = row + 2 * dr, col + 2 * dc
            if (
                    0 <= capture_r < 6 and 0 <= capture_c < 6
                    and (self.board[nr, nc] == -player or self.board[nr, nc] == -2 * player)
                    and self.board[capture_r, capture_c] == 0
            ):
                capture_moves.append((row, col, capture_r, capture_c))  # Capture move

        return capture_moves


    def valid_moves_for_piece(self, current_player, selected_piece):
        '''
        Will give the possible moves for a selected piece
        :param current_player:
        :param selected_piece:
        :return:
        '''
        row, col = selected_piece
        moves = self.valid_moves(current_player)
        moves_with_piece = []
        for move in moves:
            if move[0] == row and move[1] == col:
                moves_with_piece.append(move)
        return moves_with_piece


    def game_winner(self, board):
        '''
        return player 1 win or player -1 win or draw
        '''
        pieces_player1 = np.count_nonzero((board == 1) | (board == 2))
        pieces_player2 = np.count_nonzero((board == -1) | (board == -2))

        if pieces_player1 == 0 or not self.valid_moves(1):
            return -1  # Player 2 wins
        elif pieces_player2 == 0 or not self.valid_moves(-1):
            return 1  # Player 1 wins
        elif not self.valid_moves(1) and not self.valid_moves(-1):
            return 0  # Draw
        else:
            return None  # Game ongoing


    def move_piece(self, player ,action):
        '''
        The transition of board and incurred reward after player performs an action.
        '''
        move_action = (action[0], action[1], action[2], action[3])
        start_r, start_c, end_r, end_c = move_action
        piece = self.board[start_r, start_c]
        self.board[start_r, start_c] = 0  # Remove piece from start
        self.board[end_r, end_c] = 2 * player if (
                    end_r == 0 or end_r == 5) else piece  # Move to end and promote if needed
        # Check if it's a capture
        if abs(start_r - end_r) >= 2:
            self.capture_piece(action)

    def capture_piece(self, action):
        '''
        Assign 0 to the positions of captured pieces.
        '''
        if len(action) > 4:
            for action in action[4]:
                move_action = (action[0], action[1], action[2], action[3])
                start_r, start_c, end_r, end_c = move_action
                mid_r, mid_c = (start_r + end_r) // 2, (start_c + end_c) // 2
                self.board[mid_r, mid_c] = 0  # Remove captured piece
        else:
            start_r, start_c, end_r, end_c = action
            mid_r, mid_c = (start_r + end_r) // 2, (start_c + end_c) // 2
            self.board[mid_r, mid_c] = 0  # Remove captured piece

    def get_board(self):
        return self.board