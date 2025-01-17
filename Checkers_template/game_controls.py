import pygame

# Constants
WIDTH, HEIGHT = 600, 600  # Window dimensions
ROWS, COLS = 6, 6  # Board dimensions
SQUARE_SIZE = WIDTH // COLS

def check_inputs(env, board, current_player, selected_piece):
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            row, col = get_square_from_pos(pygame.mouse.get_pos())

            # Check if a move is available
            if selected_piece is not None:
                moves_for_piece = env.valid_moves_for_piece(current_player, selected_piece)

                for move in moves_for_piece:
                    if move[2] == row and move[3] == col:
                        env.move_piece(current_player, move)
                        selected_piece = None
                        current_player = -1 * current_player
                        return current_player, selected_piece

            # Check if there's a piece to select
            if board[row, col] == current_player or board[row, col] == 2 * current_player:
                selected_piece = (row, col)
                return current_player, selected_piece
    return current_player, selected_piece

def get_square_from_pos(pos):
    """Convert mouse position to board coordinates."""
    x, y = pos
    return y // SQUARE_SIZE, x // SQUARE_SIZE