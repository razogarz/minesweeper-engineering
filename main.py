import sys

import pygame

import gameConstants
from generateSolvableBoard import generate_solvable_board
from pygameMinesweeper import play_game
import time

# ----------------- PYGAME SETUP -----------------
pygame.init()

def main(args=None):
    if args is None:
        args = sys.argv[1:]  # Skip the script name

    # ----------------- GAME VARIABLES -----------------
    if args[0] == "easy":
        NUM_OF_ROWS = 10
        NUM_OF_COLS = 10
        NUM_MINES = 15
    elif args[0] == "medium":
        NUM_OF_ROWS = 16
        NUM_OF_COLS = 16
        NUM_MINES = 40
    elif args[0] == "hard":
        NUM_OF_ROWS = 16
        NUM_OF_COLS = 30
        NUM_MINES = 99
    elif args[0] == "custom":
        NUM_OF_ROWS = int(args[2])
        NUM_OF_COLS = int(args[3])
        NUM_MINES = int(args[4])
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

    if args[1] == "play":
        play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font, sys, pygame)
    elif args[1] == "generate":
        print("gen")
        pygame.quit()
        start = time.time()
        generate_solvable_board(ROWS, COLS, NUM_MINES, args[0])
        end = time.time()
        time_passed = end - start
        print(f'Time taken: {int(time_passed / 3600)}h {int(time_passed / 60)}m {int(time_passed % 60)}s')
    elif args[1] == "fromfile":
        play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font, sys, pygame, from_file = True, diff=args[0])
    else:
        print("Invalid mode")
        return

if __name__ == "__main__":
    main()
