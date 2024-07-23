from boardGenerator.boardFunctions import save_for_minizinc
from gameConstants import GRAY
from pygameFunctions.minesweeper import game_over, check_win, reveal_cell, convert_to_save, create_grid, correct_hinted, \
    hint, draw_grid, load_grid


def play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font, sys, pygame, from_file=False, diff=None):
    first_click = True
    grid = None
    running = True
    game_over_flag = False

    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]

    '''
        hint_cache_board[x,y] = -2 - not mine
        hint_cache_board[x,y] = -1 - possible mine
        hint_cache_board[x,y] = 0 - not revealed, not neighbour of revealed
        hint_cache_board[x,y] = 1 - not revealed, neighbour of revealed
        hint_cache_board[x,y] = 2 - revealed
    '''
    hint_cache_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    while running:
        screen.fill(GRAY)
        draw_grid(grid, revealed, flagged, screen, font, flag_font, hint_cache_board, ROWS, COLS, GRID_SIZE)
        pygame.display.flip()

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
                    if not from_file:
                        while True:
                            grid = create_grid(ROWS, NUM_MINES, (row, col))
                            if grid[row][col] == 0:
                                break
                    else:
                        grid = load_grid(diff, row, col)
                        # while True:
                        #     grid = create_grid(ROWS, NUM_MINES, (row, col))
                        #     if grid[row][col] == 0:
                        #         break

                # ---------------- LEFT CLICK ----------------
                if event.button == 1 or event.button == 2:  # left click or scroll click
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
                            save_for_minizinc(board_to_save, ROWS, NUM_MINES)
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
