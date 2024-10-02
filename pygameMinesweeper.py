from minizincFunctions.convertToSave import convert_to_save
from minizincFunctions.correctHintedBoard import correct_hinted_board
from minizincFunctions.hintSafeFields import hint_safe_fields
from minizincFunctions.saveForMinizinc import save_for_minizinc
from gameConstants import GRAY
from pygameFunctions.drawGrid import draw_grid
from boardFunctions.generateMineField import generate_mine_field
from boardFunctions.loadGridFromFile import load_grid_from_file
from boardFunctions.handleFieldClick import handle_field_click
from boardFunctions.checkWin import check_win
from boardFunctions.gameOverRevealBombs import game_over_reveal_bombs


def play_game(COLS, ROWS, NUM_MINES, GRID_SIZE, screen, font, flag_font, sys, pygame, from_file=False, diff=None, grid_arg=None):
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
                    if from_file:
                        grid = load_grid_from_file(diff, row, col)
                    elif grid_arg:
                        grid = grid_arg
                    else:
                        while True:
                            grid = generate_mine_field(ROWS, COLS, NUM_MINES, (row, col))
                            if grid[row][col] == 0:
                                break


                # ---------------- LEFT CLICK ----------------
                if event.button == 1 or event.button == 2:  # left click or scroll click
                    if flagged[row][col]:
                        continue

                    if grid[row][col] == -1:
                        game_over_flag = True
                        game_over_reveal_bombs(grid, revealed, ROWS, COLS)
                    else:
                        handle_field_click(grid, revealed, row, col, flagged, ROWS, COLS)
                        if check_win(revealed, grid, ROWS, COLS):
                            print("You win!")
                            running = False
                        else:
                            board_to_save = convert_to_save(grid, revealed, flagged, ROWS, COLS)
                            # draw_ascii_board(board_to_save)
                            not_mines = [[0]*COLS for _ in range(ROWS)]
                            for i in range(ROWS):
                                for j in range(COLS):
                                    if hint_cache_board[i][j] == -2:
                                        not_mines[i][j] = 1
                            save_for_minizinc(board_to_save, ROWS, COLS, NUM_MINES, not_mines)
                            hint_cache_board = correct_hinted_board(board_to_save, hint_cache_board, flagged)
                            if event.button == 2:
                                hint_cache_board = hint_safe_fields(hint_cache_board, ROWS, COLS)[0]

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
