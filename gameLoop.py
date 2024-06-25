import sys
from boardGenerator.boardFunctions import saveForMinizinc, draw_ascii_board
from pygameFunctions.minesweeper import *
from gameConstants import *

# ----------------- PYGAME SETUP -----------------
pygame.init()

screen = pygame.display.set_mode((WIDTH + GRID_SIZE, HEIGHT + GRID_SIZE))
pygame.display.set_caption("Minesweeper")

font = pygame.font.SysFont(None, 30)
flag_font = pygame.font.SysFont(None, 40)

def main():
    # ----------------- GAME VARIABLES -----------------
    first_click = True
    grid = None
    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    running = True
    game_over_flag = False


    while running:
        screen.fill(GRAY)
        for event in pygame.event.get():
            # ---------------- QUIT ----------------
            if event.type == pygame.QUIT:
                running = False
            # ------------- MOUSE CLICK ------------
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over_flag:
                x, y = event.pos
                row, col = (y // GRID_SIZE)-1, (x // GRID_SIZE)-1

                # ---------------- FIRST CLICK ----------------
                if first_click:
                    first_click = False
                    while True:
                        grid = create_grid(ROWS, NUM_MINES, (row, col))
                        if grid[row][col] == 0:
                            break

                # ---------------- LEFT CLICK ----------------
                if event.button == 1:  # Left click
                    if grid[row][col] == -1:
                        game_over_flag = True
                        game_over(grid, revealed)
                    else:
                        reveal_cell(grid, revealed, row, col, flagged)
                        if check_win(revealed, grid):
                            print("You win!")
                            running = False

                # ---------------- RIGHT CLICK ----------------
                if event.button == 3:
                    flagged[row][col] = not flagged[row][col]
                board_to_save = convert_to_save(grid, revealed, flagged)
                draw_ascii_board(board_to_save)
                saveForMinizinc(board_to_save, ROWS, NUM_MINES)

        # ----------------- DRAW GRID -----------------
        if grid:
            draw_grid(grid, revealed, flagged, screen, font, flag_font)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
