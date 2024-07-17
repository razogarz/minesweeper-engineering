import sys

import gameConstants
from boardGenerator.boardFunctions import saveForMinizinc
from pygameFunctions.minesweeper import *
from gameConstants import *

# ----------------- PYGAME SETUP -----------------
pygame.init()

def play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font):
    first_click = True
    grid = None
    running = True
    game_over_flag = False

    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]

    '''
        hint_cache_board[x,y] = -2 - mine
        hint_cache_board[x,y] = -1 - possible mine
        hint_cache_board[x,y] = 0 - not revealed, not neighbour of revealed
        hint_cache_board[x,y] = 1 - not revealed, neighbour of revealed
        hint_cache_board[x,y] = 2 - revealed
    '''
    hint_cache_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    while running:
        screen.fill(GRAY)
        for event in pygame.event.get():
            # ---------------- QUIT ----------------
            if event.type == pygame.QUIT:
                running = False

            # ------------- MOUSE CLICK ------------
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over_flag:
                x, y = event.pos
                if x < GRID_SIZE or y < GRID_SIZE:
                    continue

                row, col = (y // GRID_SIZE) - 1, (x // GRID_SIZE) - 1

                # ---------------- FIRST CLICK ----------------
                if first_click:
                    first_click = False
                    while True:
                        grid = create_grid(ROWS, NUM_MINES, (row, col))
                        if grid[row][col] == 0:
                            break

                # ---------------- LEFT CLICK ----------------
                if event.button == 1 or event.button == 2:  # left click or right click
                    if grid[row][col] == -1:
                        game_over_flag = True
                        game_over(grid, revealed, ROWS, COLS)
                    else:
                        reveal_cell(grid, revealed, row, col, flagged, ROWS, COLS)
                        if check_win(revealed, grid, ROWS, COLS):
                            print("You win!")
                            running = False
                        else:
                            board_to_save = convert_to_save(grid, revealed, flagged, ROWS, COLS)
                            # draw_ascii_board(board_to_save)
                            saveForMinizinc(board_to_save, ROWS, NUM_MINES)
                            hint_cache_board = correct_hinted(board_to_save, hint_cache_board, flagged)
                            if event.button == 2:
                                hint_cache_board = hint(hint_cache_board, ROWS, COLS)

                # ---------------- RIGHT CLICK ----------------
                if event.button == 3:
                    flagged[row][col] = not flagged[row][col]
                    hint_cache_board[row][col] = -1 if flagged[row][col] else 1

        # ----------------- DRAW GRID -----------------
        if grid:
            draw_grid(grid, revealed, flagged, screen, font, flag_font, hint_cache_board, ROWS, COLS, GRID_SIZE)
        pygame.display.flip()

    pygame.quit()
    sys.exit()




def main(args=None):
    if args is None:
        args = sys.argv[1:]  # Skip the script name

    # ----------------- GAME VARIABLES -----------------
    if args[0] == "easy":
        NUM_OF_CELLS = 8
        NUM_MINES = 10
    elif args[0] == "medium":
        NUM_OF_CELLS = 15
        NUM_MINES = 40
    elif args[0] == "hard":
        NUM_OF_CELLS = 20
        NUM_MINES = 99
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
        play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font)
    elif args[1] == "generate":
        print("Generating board...")
    else:
        print("Invalid mode")
        return




if __name__ == "__main__":
    main()
