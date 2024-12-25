

import numpy as np


class checkers_env:

    def __init__(self, board=None, player=None):

        self.board = self.initialize_board()
        self.player = 1


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
        self.player = 1


    def valid_moves(self, player):
        '''
        A possible format could be [start_row, start_col, end_row, end_col], there are normal moves and moves with capture. Pieces could be king or normal.
        '''
        moves = []
        directions = [(-1, -1), (-1, 1)] if player == 1 else [(1, -1), (1, 1)]

        for row in range(6):
            for col in range(6):
                if self.board[row, col] == player or self.board[row, col] == 2 * player:  # Normal or king
                    piece_directions = directions
                    if self.board[row, col] == 2 * player:  # King moves in all directions
                        piece_directions += [(-d[0], -d[1]) for d in directions]

                    for dr, dc in piece_directions:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < 6 and 0 <= nc < 6 and self.board[nr, nc] == 0:
                            moves.append((row, col, nr, nc))  # Normal move

                        # Check for captures
                        capture_r, capture_c = row + 2 * dr, col + 2 * dc
                        if (
                                0 <= capture_r < 6 and 0 <= capture_c < 6
                                and self.board[nr, nc] == -player
                                and self.board[capture_r, capture_c] == 0
                        ):
                            moves.append((row, col, capture_r, capture_c))  # Capture move

        return moves



    def capture_piece(self, action):
        '''
        Assign 0 to the positions of captured pieces.
        '''
        start_r, start_c, end_r, end_c = action
        mid_r, mid_c = (start_r + end_r) // 2, (start_c + end_c) // 2
        self.board[mid_r, mid_c] = 0  # Remove captured piece



    def game_winner(self, board):
        '''
        return player 1 win or player -1 win or draw
        '''
        pieces_player1 = np.count_nonzero((board == 1) | (board == 2))
        pieces_player2 = np.count_nonzero((board == -1) | (board == -2))

        if pieces_player1 == 0:
            return -1  # Player 2 wins
        elif pieces_player2 == 0:
            return 1  # Player 1 wins
        elif not self.valid_moves(1) and not self.valid_moves(-1):
            return 0  # Draw
        else:
            return None  # Game ongoing


    def step(self, action, player):
        '''
        The transition of board and incurred reward after player performs an action. Be careful about King
        '''
        start_r, start_c, end_r, end_c = action
        self.board[start_r, start_c] = 0  # Remove piece from start
        self.board[end_r, end_c] = 2 * player if (
                    end_r == 0 or end_r == 5) else player  # Move to end and promote if needed

        # Check if it's a capture
        if abs(start_r - end_r) == 2:
            self.capture_piece(action)

        winner = self.game_winner(self.board)
        reward = 1 if winner == player else -1 if winner == -player else 0
        return [self.board, reward]


    def render(self):
        for row in self.board:
            for square in row:
                if square == 1:
                    piece = "|0"
                elif square == -1:
                    piece = "|X"
                elif square == 2:
                    piece = "|K"
                else:
                    piece = "| "
                print(piece, end='')
            print("|")