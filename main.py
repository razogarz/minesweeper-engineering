import sys

import pygame

import gameConstants
from generateSolvableBoard import generate_solvable_board
from pygameMinesweeper import play_game
import time

from smartGen import smart_generate_board

# ----------------- PYGAME SETUP -----------------
pygame.init()

def main(args=None):
    global num_cols_arg, num_rows_arg, num_mines_arg, difficulty_arg, game_mode_arg
    if args is None:
        args = sys.argv[1:]  # Skip the script name

    difficulty_arg = args[0]
    game_mode_arg = args[1]

    if game_mode_arg == "custom":
        if len(args) != 5:
            print("Invalid number of arguments")
            return
        if not args[2].isdigit() or not args[3].isdigit() or not args[4].isdigit():
            print("Invalid arguments")
            return

        num_rows_arg = int(args[2])
        num_cols_arg = int(args[3])
        num_mines_arg = int(args[4])


    # ----------------- GAME VARIABLES -----------------
    if difficulty_arg == "easy":
        NUM_OF_ROWS = 10
        NUM_OF_COLS = 10
        NUM_MINES = 15
    elif difficulty_arg == "medium":
        NUM_OF_ROWS = 16
        NUM_OF_COLS = 16
        NUM_MINES = 40
    elif difficulty_arg == "hard":
        NUM_OF_ROWS = 16
        NUM_OF_COLS = 30
        NUM_MINES = 99
    elif difficulty_arg == "custom":
        NUM_OF_ROWS = num_rows_arg
        NUM_OF_COLS = num_cols_arg
        NUM_MINES = num_mines_arg
    else:
        print("Invalid difficulty")
        return

    GRID_SIZE = 40  # Size of each cell
    WIDTH, HEIGHT = GRID_SIZE * NUM_OF_COLS, GRID_SIZE * NUM_OF_ROWS
    ROWS = NUM_OF_ROWS
    COLS = NUM_OF_COLS

    gameConstants.NUM_OF_CELLS = NUM_OF_ROWS * NUM_OF_COLS
    gameConstants.GRID_SIZE = GRID_SIZE
    gameConstants.WIDTH = WIDTH
    gameConstants.HEIGHT = HEIGHT
    gameConstants.NUM_MINES = NUM_MINES
    gameConstants.ROWS = ROWS
    gameConstants.COLS = COLS

    screen = pygame.display.set_mode((WIDTH + GRID_SIZE, HEIGHT + GRID_SIZE))
    pygame.display.set_caption("Minesweeper")

    font = pygame.font.SysFont(None, 40)
    flag_font = pygame.font.SysFont(None, 40)

    if game_mode_arg == "play":
        play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font, sys, pygame)
    elif game_mode_arg == "generate":
        print("gen")
        pygame.quit()
        start = time.time()
        generate_solvable_board(ROWS, COLS, NUM_MINES, args[0])
        end = time.time()
        time_passed = end - start
        print(f'Time taken: {int(time_passed / 3600)}h {int(time_passed / 60)}m {int(time_passed % 60)}s')
    elif game_mode_arg == "fromfile":
        play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font, sys, pygame, from_file = True, diff=args[0])
    elif game_mode_arg == "smartgen":
        pygame.quit()
        start = time.time()
        smart_generate_board(ROWS, COLS, NUM_MINES, args[0])
        end = time.time()
        time_passed = end - start
        print(f'Time taken: {int(time_passed / 3600)}h {int(time_passed / 60)}m {int(time_passed % 60)}s')
    else:
        print("Invalid mode")
        return

if __name__ == "__main__":
    main()
