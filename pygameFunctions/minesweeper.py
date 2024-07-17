import numpy as np
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


def draw_grid(grid, revealed, flagged, screen, font, flag_font, hint_cache_board, ROWS, COLS, GRID_SIZE):
    """
    Draw the minesweeper grid
    """

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect((col + 1) * GRID_SIZE, (row + 1) * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if revealed[row][col]:
                if grid[row][col] == -1:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    if grid[row][col] > 0:
                        text = font.render(str(grid[row][col]), True, BLACK)
                        screen.blit(text, ((col + 1) * GRID_SIZE + 10, (row + 1) * GRID_SIZE + 5))
            elif hint_cache_board[row][col] == -2:
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if flagged[row][col]:
                    flag_text = flag_font.render('F', True, BLUE)
                    screen.blit(flag_text, ((col + 1) * GRID_SIZE + 10, (row + 1) * GRID_SIZE + 5))

    # Draw row numbers
    for row in range(ROWS):
        row_text = font.render(str(row + 1), True, BLACK)
        screen.blit(row_text, (10, (row + 1) * GRID_SIZE + 10))

    # Draw column numbers
    for col in range(COLS):
        col_text = font.render(str(col + 1), True, BLACK)
        screen.blit(col_text, ((col + 1) * GRID_SIZE + 10, 10))




def reveal_cell(grid, revealed, row, col, flagged, ROWS, COLS):
    if revealed[row][col] or flagged[row][col]:
        return
    revealed[row][col] = True
    if grid[row][col] == 0:
        for r in range(max(0, row - 1), min(ROWS, row + 2)):
            for c in range(max(0, col - 1), min(COLS, col + 2)):
                if not revealed[r][c]:
                    reveal_cell(grid, revealed, r, c, flagged, ROWS, COLS)

def check_win(revealed, grid, ROWS, COLS):
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != -1 and not revealed[row][col]:
                return False
    return True

def game_over(grid, revealed, ROWS, COLS):
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == -1:
                revealed[row][col] = True

def convert_to_save(grid, revealed, flagged, ROWS, COLS):
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

def correct_hinted(board, hint_cache_board, flagged):
    """
    0 not neighbouring
    1 neighbouring
    2 revealed
    """
    ROWS, COLS = len(board), len(board[0])  # Ensure ROWS and COLS are defined

    for i in range(ROWS):
        for j in range(COLS):
            if hint_cache_board[i][j] not in [-1, 0, 1]:
                continue

            if flagged[i][j]:
                hint_cache_board[i][j] = -1
                continue

            for r in range(max(0, i - 1), min(ROWS, i + 2)):
                for c in range(max(0, j - 1), min(COLS, j + 2)):
                    if board[r][c] != -1 and (r != i or c != j):
                        hint_cache_board[i][j] = 1

            if board[i][j] != -1:
                hint_cache_board[i][j] = 2

    return hint_cache_board

def hint(hint_cache_board, ROWS, COLS):
    """
    Send hint cache to minizinc
    """
    temp_board = np.zeros((ROWS, COLS))

    for i in range(ROWS):
        for j in range(COLS):
            if hint_cache_board[i][j] != 1 or temp_board[i,j] == 1:
                continue

            minesweeper_model = Model("/mnt/c/Users/Razogarz/PycharmProjects/minesweeper-engineering/superMSSolver/mine_not_possible.mzn")
            gecode = Solver.lookup("gecode")

            minesweeper_model.add_file("/mnt/c/Users/Razogarz/PycharmProjects/minesweeper-engineering/superMSSolver/data/data_gen.dzn", parse_data=True)
            instance = Instance(gecode,minesweeper_model)
            instance['x'] = i+1
            instance['y'] = j+1

            result = instance.solve()
            is_unsat = str(result.status) == "UNSATISFIABLE"

            if is_unsat:
                hint_cache_board[i][j] = -2
                print("Mine not possible at: ", i+1, j+1)
            else:
                temp_board = np.logical_or(temp_board, np.array(result['potential_mines']))

    return hint_cache_board


