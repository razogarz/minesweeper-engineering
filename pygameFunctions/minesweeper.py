from minizinc import Instance, Model, Solver
from gameConstants import *
import pygame
import random

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


def draw_grid(grid, revealed, flagged, screen, font, flag_font):
    """
    Draw the minesweeper grid
    """

    # Info bar height
    info_bar_height = 40

    # Draw info bar with buttons
    pygame.draw.rect(screen, DARK_GRAY, (0, 0, WIDTH+GRID_SIZE, info_bar_height))

    text_mines = font.render("Mines: " + str(NUM_MINES), True, BLACK)
    screen.blit(text_mines, (10, 10))

    text_time = font.render("Time: 0", True, BLACK)
    screen.blit(text_time, (WIDTH - 100, 10))


    text_reset = font.render("Reset", True, BLACK)
    reset_rect = pygame.Rect(180, 5, 90, 30)
    pygame.draw.rect(screen, WHITE, reset_rect)
    pygame.draw.rect(screen, BLACK, reset_rect, 1)
    screen.blit(text_reset, (190, 10))

    text_hint = font.render("Hint", True, BLACK)
    hint_rect = pygame.Rect(280, 5, 90, 30)
    pygame.draw.rect(screen, WHITE, hint_rect)
    pygame.draw.rect(screen, BLACK, hint_rect, 1)
    screen.blit(text_hint, (290, 10))



    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect((col + 1) * GRID_SIZE, info_bar_height + (row + 1) * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if revealed[row][col]:
                if grid[row][col] == -1:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    if grid[row][col] > 0:
                        text = font.render(str(grid[row][col]), True, BLACK)
                        screen.blit(text, ((col + 1) * GRID_SIZE + 10, info_bar_height + (row + 1) * GRID_SIZE + 5))
            else:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if flagged[row][col]:
                    flag_text = flag_font.render('F', True, BLUE)
                    screen.blit(flag_text, ((col + 1) * GRID_SIZE + 10, info_bar_height + (row + 1) * GRID_SIZE + 5))

    # Draw row numbers
    for row in range(ROWS):
        row_text = font.render(str(row + 1), True, BLACK)
        screen.blit(row_text, (10, info_bar_height + (row + 1) * GRID_SIZE + 10))

    # Draw column numbers
    for col in range(COLS):
        col_text = font.render(str(col + 1), True, BLACK)
        screen.blit(col_text, ((col + 1) * GRID_SIZE + 10, info_bar_height + 10))




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

def correct_hinted(board, hint_cache_board):
    """
    0 not neighbouring
    1 neighbouring
    2 revealed
    """
    for i in range(ROWS):
        for j in range(COLS):
            if hint_cache_board[i][j] not in [0,1]:
                continue

            for r in range(max(0, i - 1), min(ROWS, i + 2)):
                for c in range(max(0, j - 1), min(COLS, j + 2)):
                    if board[r][c] != -1 and r != i and c != j:
                        hint_cache_board[i][j] = 1

            if board[i][j] != -1:
                hint_cache_board[i][j] = 2

    return hint_cache_board

def hint(hint_cache_board):
    """
    Send hint cache to minizinc
    """
    for i in range(len(hint_cache_board[0])):
        for j in range(len(hint_cache_board)):
            if hint_cache_board[i][j] != 1:
                continue
            minesweeper_model = Model("/mnt/c/Users/Razogarz/PycharmProjects/minesweeper-engineering/superMSSolver/mine_not_possible.mzn")
            gecode = Solver.lookup("gecode")

            minesweeper_model.add_file("/mnt/c/Users/Razogarz/PycharmProjects/minesweeper-engineering/superMSSolver/data/data_gen.dzn", parse_data=True)
            instance = Instance(gecode,minesweeper_model)
            instance['x'] = i+1
            instance['y'] = j+1

            result = instance.solve()
            print(i+1,j+1,result)
            # if not result["potential_mines"]:
            #     print(i,j)




