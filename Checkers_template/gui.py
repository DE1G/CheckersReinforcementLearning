import pygame
import sys
from Checkers_template.checkers_env import checkers_env

# Constants
WIDTH, HEIGHT = 600, 600  # Window dimensions
ROWS, COLS = 6, 6  # Board dimensions
SQUARE_SIZE = WIDTH // COLS

# Initialize pygame
pygame.init()

# Load images
RED_PIECE_SURFACE = pygame.image.load("images/red_piece.png")
WHITE_PIECE_SURFACE = pygame.image.load("images/white_piece.png")
RED_KING_PIECE_SURFACE = pygame.image.load("images/red_king_piece.png")
WHITE_KING_PIECE_SURFACE = pygame.image.load("images/white_king_piece.png")
MOVE_MARK = pygame.image.load("images/marking.png")
BOARD = pygame.image.load("images/board.png")

# Scale images to match the board size
RED_PIECE_SURFACE = pygame.transform.scale(RED_PIECE_SURFACE, (SQUARE_SIZE, SQUARE_SIZE))
WHITE_PIECE_SURFACE = pygame.transform.scale(WHITE_PIECE_SURFACE, (SQUARE_SIZE, SQUARE_SIZE))
RED_KING_PIECE_SURFACE = pygame.transform.scale(RED_KING_PIECE_SURFACE, (SQUARE_SIZE, SQUARE_SIZE))
WHITE_KING_PIECE_SURFACE = pygame.transform.scale(WHITE_KING_PIECE_SURFACE, (SQUARE_SIZE, SQUARE_SIZE))
MOVE_MARK = pygame.transform.scale(MOVE_MARK, (SQUARE_SIZE, SQUARE_SIZE))
BOARD = pygame.transform.scale(BOARD, (WIDTH, HEIGHT))


# Helper Functions
def draw_board(env, win, board, player, selected_piece=None):
    """Draw the checkers board and pieces."""
    # Draw the board background
    win.blit(BOARD, (0, 0))

    # Draw pieces
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row, col]
            if piece == 1:  # White piece
                win.blit(WHITE_PIECE_SURFACE, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif piece == -1:  # Black piece
                win.blit(RED_PIECE_SURFACE, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif piece == 2:  # White king
                win.blit(WHITE_KING_PIECE_SURFACE, (col * SQUARE_SIZE, row * SQUARE_SIZE))
            elif piece == -2:  # red king
                win.blit(RED_KING_PIECE_SURFACE, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    if selected_piece is not None:
        moves_for_piece = env.valid_moves_for_piece(player, selected_piece)
        for move in moves_for_piece:
            win.blit(MOVE_MARK, (move[3] * SQUARE_SIZE, move[2] * SQUARE_SIZE))

def update_board(env, win, board, player, selected_piece=None):
    win.fill((0, 0, 0))  # Clear the screen
    draw_board(env, win, board, player, selected_piece)
    pygame.display.flip()