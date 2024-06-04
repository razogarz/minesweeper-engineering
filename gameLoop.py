from functions import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 15  # Size of each cell
NUM_MINES = 40
ROWS = HEIGHT // GRID_SIZE
COLS = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DARK_GRAY = (128, 128, 128)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Fonts
font = pygame.font.SysFont(None, 30)
flag_font = pygame.font.SysFont(None, 40)

# Game loop
def main():
    # Initialize game variables
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    first_click = (0, 0)

    # Draw board to get first click
    draw_empty_board(ROWS, COLS, GRID_SIZE, GRAY, screen)

    # Generate a board with mines
    while True:
        full_board = naive_gen_board(GRID_SIZE, NUM_MINES, first_click)
        if full_board[first_click[0]][first_click[1]] == 0:
            break

    while True:
        # Draw the board
        draw_board(screen, full_board, revealed, flagged, font, flag_font, GRID_SIZE)

        # Check for game over
        if check_game_over(full_board, revealed):
            draw_game_over_screen(screen)
            break

        # Check for win
        if check_win(full_board, revealed):
            draw_win_screen(screen)
            break

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                row, col = y // GRID_SIZE, x // GRID_SIZE
                if event.button == 1:
                    if not flagged[row][col]:
                        if full_board[row][col] == 9:
                            revealed = [[True for _ in range(COLS)] for _ in range(ROWS)]
                        else:
                            revealed = uncover_fields(revealed, full_board, row, col)
                elif event.button == 3:
                    flagged[row][col] = not flagged[row][col]



if __name__ == "__main__":
    main()
