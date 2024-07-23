from boardGenerator.boardFunctions import save_for_minizinc, draw_ascii_board
from pygameFunctions.minesweeper import create_grid, game_over, reveal_cell, check_win, save_grid, convert_to_save, \
    correct_hinted, hint, is_game_over


def generate_no_guesser(ROWS, COLS, NUM_MINES, difficulty) -> bool:
    first_click = True
    grid = None
    running = True
    game_over_flag = False

    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    possible_moves = []

    '''
        hint_cache_board[x,y] = -2 - mine
        hint_cache_board[x,y] = -1 - possible mine
        hint_cache_board[x,y] = 0 - not revealed, not neighbour of revealed
        hint_cache_board[x,y] = 1 - not revealed, neighbour of revealed
        hint_cache_board[x,y] = 2 - revealed
    '''
    hint_cache_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    original_x = int(input("Enter x coordinate: "))
    original_y = int(input("Enter y coordinate: "))

    x = int(original_x)
    y = int(original_y)

    while running:
        if not first_click and len(possible_moves) > 0:
            while len(possible_moves) > 0:
                x, y = possible_moves.pop(0)
                reveal_cell(grid, revealed, x, y, flagged, ROWS, COLS)
        elif first_click:
            first_click = False
            while True:
                grid = create_grid(ROWS, NUM_MINES, (original_x, original_y))
                if grid[original_x][original_y] == 0:
                    break
            reveal_cell(grid, revealed, original_x, original_y, flagged, ROWS, COLS)
        else:
            game_over_flag = True

        if check_win(revealed, grid, ROWS, COLS):
            print("FOUND U")
            draw_ascii_board(grid)
            save_grid(grid, difficulty, original_x, original_y)
            return True
        elif not is_game_over(grid, revealed, ROWS, COLS):
            board_to_save = convert_to_save(grid, revealed, flagged, ROWS, COLS)
            save_for_minizinc(board_to_save, ROWS, NUM_MINES)
            hint_cache_board = correct_hinted(board_to_save, hint_cache_board, flagged)
            hint_cache_board = hint(hint_cache_board, ROWS, COLS)

            for i in range(ROWS):
                for j in range(COLS):
                    if hint_cache_board[i][j] == -2 and not revealed[i][j]:
                        possible_moves.append((i, j))  # Use tuple instead of list for consistency

            print("Possible moves: ", possible_moves)
            if not possible_moves:
                print("No possible moves")
                game_over_flag = True

        if game_over_flag:
            print("Restarting")
            game_over_flag = False
            first_click = True
            grid = None
            revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
            flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
            possible_moves = []
            hint_cache_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            continue

    return False

