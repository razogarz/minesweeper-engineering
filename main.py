import sys

import gameConstants
from generateNoGuessingBoard import generate_no_guesser
from pygameMinesweeper import play_game
from pygameFunctions.minesweeper import *

# ----------------- PYGAME SETUP -----------------
pygame.init()

def main(args=None):
    if args is None:
        args = sys.argv[1:]  # Skip the script name

    # ----------------- GAME VARIABLES -----------------
    if args[0] == "easy":
        NUM_OF_CELLS = 8
        NUM_MINES = 15
    elif args[0] == "medium":
        NUM_OF_CELLS = 15
        NUM_MINES = 45
    elif args[0] == "hard":
        NUM_OF_CELLS = 20
        NUM_MINES = 85
    else:
        print("Invalid difficulty")
        return

    GRID_SIZE = 40  # Size of each cell
    WIDTH, HEIGHT = GRID_SIZE * NUM_OF_CELLS, GRID_SIZE * NUM_OF_CELLS
    ROWS = NUM_OF_CELLS
    COLS = NUM_OF_CELLS

    gameConstants.NUM_OF_CELLS = NUM_OF_CELLS
    gameConstants.GRID_SIZE = GRID_SIZE
    gameConstants.WIDTH = WIDTH
    gameConstants.HEIGHT = HEIGHT
    gameConstants.NUM_MINES = NUM_MINES
    gameConstants.ROWS = ROWS
    gameConstants.COLS = COLS

    screen = pygame.display.set_mode((WIDTH + GRID_SIZE, HEIGHT + GRID_SIZE))
    pygame.display.set_caption("Minesweeper")

    font = pygame.font.SysFont(None, 30)
    flag_font = pygame.font.SysFont(None, 40)

    if args[1] == "play":
        play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font, sys, pygame)
    elif args[1] == "generate":
        print("gen")
        pygame.quit()
        generate_no_guesser(ROWS, COLS, NUM_MINES, args[0])
    elif args[1] == "fromfile":
        play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font, sys, pygame, from_file = True, diff=args[0])
    else:
        print("Invalid mode")
        return

if __name__ == "__main__":
    main()
