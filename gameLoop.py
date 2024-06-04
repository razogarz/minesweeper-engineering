import pygame
import random
import sys
from boardGenerator.boardFunctions import saveForMinizinc, draw_ascii_board

# Initialize Pygame
pygame.init()

# Constants
NUM_OF_CELLS = 20
GRID_SIZE = 40  # Size of each cell
WIDTH, HEIGHT = GRID_SIZE * NUM_OF_CELLS, GRID_SIZE * NUM_OF_CELLS
NUM_MINES = 100
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

def create_grid(size: int, number_of_mines: int, first_click: tuple) -> list:
    """
    Generate a naive board with mines
    """
    # Initialize the board
    board = [[0 for _ in range(size)] for _ in range(size)]
    # Place mines
    mines = set()
    while len(mines) < number_of_mines:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if (x, y) != first_click and (x, y) not in mines:
            mines.add((x, y))
            board[x][y] = -1
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < size and 0 <= y + dy < size and board[x + dx][y + dy] != -1:
                        board[x + dx][y + dy] += 1
    return board

def draw_grid(grid, revealed, flagged):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if revealed[row][col]:
                if grid[row][col] == -1:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    if grid[row][col] > 0:
                        text = font.render(str(grid[row][col]), True, BLACK)
                        screen.blit(text, (col * GRID_SIZE + 10, row * GRID_SIZE + 5))
            else:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if flagged[row][col]:
                    flag_text = flag_font.render('F', True, BLUE)
                    screen.blit(flag_text, (col * GRID_SIZE + 10, row * GRID_SIZE + 5))

def reveal_cell(grid, revealed, row, col, flagged):
    if revealed[row][col] or flagged[row][col]:
        return
    revealed[row][col] = True
    if grid[row][col] == 0:
        for r in range(max(0, row - 1), min(ROWS, row + 2)):
            for c in range(max(0, col - 1), min(COLS, col + 2)):
                if not revealed[r][c]:
                    reveal_cell(grid, revealed, r, c, flagged)

def check_win(revealed, grid):
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != -1 and not revealed[row][col]:
                return False
    return True

def game_over(grid, revealed):
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == -1:
                revealed[row][col] = True

def convert_to_save(grid, revealed, flagged):
    board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            if revealed[row][col]:
                if grid[row][col] == -1:
                    board[row][col] = 9
                else:
                    board[row][col] = grid[row][col]
            else:
                board[row][col] = -1
    return board

# Game loop
def main():
    first_click = True
    grid = None
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    running = True
    game_over_flag = False
    while running:
        screen.fill(GRAY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over_flag:
                x, y = event.pos
                row, col = y // GRID_SIZE, x // GRID_SIZE
                if first_click:
                    first_click = False
                    while True:
                        grid = create_grid(ROWS, NUM_MINES, (row, col))
                        if grid[row][col] == 0:
                            break
                if event.button == 1:  # Left click
                    if grid[row][col] == -1:
                        game_over_flag = True
                        game_over(grid, revealed)
                    else:
                        reveal_cell(grid, revealed, row, col, flagged)
                        if check_win(revealed, grid):
                            print("You win!")
                            running = False
                if event.button == 3:  # Right click
                    flagged[row][col] = not flagged[row][col]
                board_to_save = convert_to_save(grid, revealed, flagged)
                draw_ascii_board(board_to_save)
                saveForMinizinc(board_to_save, ROWS, NUM_MINES)
        if grid:
            draw_grid(grid, revealed, flagged)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
