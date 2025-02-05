import numpy as np


class CheckersEnv:

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


    def get_board(self):
        return self.board

    def valid_moves(self, player):
        """
        Finds all valid moves for the given player, including multi-captures.
        Returns a list of moves. Each move is a tuple:
        (start_row, start_col, end_row, end_col, [captured_positions]).
        """
        moves = []
        for row in range(6):
            for col in range(6):
                if self.board[row, col] in [player, 2 * player]:
                    piece_directions = self.get_piece_directions(player, self.board[row, col])
                    self.find_moves(row, col, player, piece_directions, moves, [], multi_capture=True)

        #check if capture moves exist and convert list to tuple to be able to hash it
        capture_moves = [(move[0], move[1], move[2], move[3], tuple(move[4])) for move in moves if len(move[4])>0]
        moves = [(move[0], move[1], move[2], move[3], tuple(move[4])) for move in moves]

        return moves if len(capture_moves) == 0 else capture_moves

    def get_piece_directions(self, player, piece):
        """Returns movement directions based on piece type (normal or king)."""
        if piece == player:
            return [(1, 1), (1, -1)] if player == 1 else [(-1, 1), (-1, -1)]
        else:
            return [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    def find_moves(self, row, col, player, directions, moves, captured, multi_capture=True):
        """
        Recursively finds all valid moves for a piece, including multi-captures.
        """
        for dr, dc in directions:
            nr, nc = row + dr, col + dc

            # Check for simple moves
            if (nr, nc) not in captured and 0 <= nr < 6 and 0 <= nc < 6 and self.board[nr, nc] == 0:
                moves.append((row, col, nr, nc, []))

            # Check for captures
            capture_r, capture_c = row + 2 * dr, col + 2 * dc
            if (
                    0 <= capture_r < 6 and 0 <= capture_c < 6
                    and (self.board[nr, nc] == -player or -2 * player == self.board[nr,nc])  # Opponent's piece
                    and self.board[capture_r, capture_c] == 0  # Landing square is empty
                    and (nr, nc) not in captured  # Avoid re-capturing the same piece
            ):

                new_captured = captured + [(nr, nc)]
                for move in moves:
                    if move[2] == row and move[3] == col:
                        row = move[0]
                        col = move[1]
                moves.append((row, col, capture_r, capture_c, new_captured))

                # Explore further captures if multi_capture is enabled
                self.find_moves(capture_r, capture_c, player, directions, moves, new_captured,
                                multi_capture=True)

    def valid_moves_for_piece(self, player, selected_piece):
        """Returns valid moves for a specific piece on the board."""
        row, col = selected_piece
        piece = self.board[row, col]
        if piece not in [player, 2 * player]:
            return []

        moves = self.valid_moves(player)
        valid_moves = []
        for move in moves:
            if move[0] == row and move[1] == col:
                valid_moves.append(move)
        return valid_moves

    def move_piece(self, player, action):
        """
        Updates the board by performing the given action and handles captures.
        """
        start_r, start_c, end_r, end_c, captured_positions = action

        # Move the piece
        piece = self.board[start_r, start_c]
        self.board[start_r, start_c] = 0
        self.board[end_r, end_c] = 2 * player if (end_r == 0 or end_r == 5) else piece  # Promote if needed

        # Remove captured pieces
        for r, c in captured_positions:
            self.board[r, c] = 0

    def game_winner(self, moves_since_capture=0):
        """
        Determines the winner of the game.
        Returns 1 if Player 1 wins, -1 if Player -1 wins, 0 for a draw, and None if the game is ongoing.
        """
        if moves_since_capture >= 80:
            return 0
        pieces_player1 = np.count_nonzero((self.board == 1) | (self.board == 2))
        pieces_player2 = np.count_nonzero((self.board == -1) | (self.board == -2))

        if pieces_player1 == 0 or len(self.valid_moves(1)) == 0:
            return -1  # Player 2 wins
        elif pieces_player2 == 0 or len(self.valid_moves(-1)) == 0:
            return 1  # Player 1 wins
        elif len(self.valid_moves(1)) == 0 and len(self.valid_moves(-1)) == 0:
            return 0  # Draw
        else:
            return None  # Game ongoing
