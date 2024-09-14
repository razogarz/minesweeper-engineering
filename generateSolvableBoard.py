from boardFunctions.checkLose import check_lose
from minizincFunctions.convertToSave import convert_to_save
from minizincFunctions.correctHintedBoard import correct_hinted_board
from minizincFunctions.hintMinedFields import hint_mined_fields
from minizincFunctions.hintSafeFields import hint_safe_fields
from minizincFunctions.saveForMinizinc import save_for_minizinc

from boardFunctions.handleFieldClick import handle_field_click
from boardFunctions.checkWin import check_win
from boardFunctions.drawAsciiBoard import draw_ascii_board
from boardFunctions.generateMineField import generate_mine_field
from boardFunctions.saveGridToFile import save_grid_to_file



def generate_solvable_board(ROWS, COLS, NUM_MINES, difficulty) -> bool:
    first_click = True
    grid = None
    running = True
    game_over_flag = False

    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    possible_moves = []

    '''
        hint_cache_board[x,y] = -3 - mine
        hint_cache_board[x,y] = -2 - not mine
        hint_cache_board[x,y] = -1 - possible mine
        hint_cache_board[x,y] = 0 - not revealed, not neighbour of revealed
        hint_cache_board[x,y] = 1 - not revealed, neighbour of revealed
        hint_cache_board[x,y] = 2 - revealed
    '''
    hint_cache_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    original_x = int(input("Enter x coordinate: "))
    original_y = int(input("Enter y coordinate: "))

    empty_fields = []

    while running:
        if not first_click and len(possible_moves) > 0:
            while len(possible_moves) > 0:
                x, y = possible_moves.pop(0)
                handle_field_click(grid, revealed, x, y, flagged, ROWS, COLS)
        elif first_click:
            first_click = False
            while True:
                grid = generate_mine_field(ROWS, COLS, NUM_MINES, (original_x, original_y))
                if grid[original_x][original_y] == 0:
                    break
            handle_field_click(grid, revealed, original_x, original_y, flagged, ROWS, COLS)

            # Save the empty fields
            for i in range(ROWS):
                for j in range(COLS):
                    if revealed[i][j] and grid[i][j] == 0:
                        empty_fields.append((i, j))
            print("Empty fields: ", empty_fields)
        else:
            game_over_flag = True

        if check_win(revealed, grid, ROWS, COLS):
            print("FOUND U")
            draw_ascii_board(grid)
            save_grid_to_file(grid, difficulty, original_x, original_y)
            return True
        elif not check_lose(grid, revealed, ROWS, COLS):
            board_to_save = convert_to_save(grid, revealed, flagged, ROWS, COLS)
            not_mines = [[0] * COLS for _ in range(ROWS)]
            for i in range(ROWS):
                for j in range(COLS):
                    if hint_cache_board[i][j] == -2:
                        not_mines[i][j] = 1
            save_for_minizinc(board_to_save, ROWS, COLS, NUM_MINES, not_mines)
            hint_cache_board = correct_hinted_board(board_to_save, hint_cache_board, flagged)
            hint_cache_board = hint_safe_fields(hint_cache_board, ROWS, COLS)

            for i in range(ROWS):
                for j in range(COLS):
                    if hint_cache_board[i][j] == -2 and not revealed[i][j]:
                        possible_moves.append((i, j))  # Use tuple instead of list for consistency

            print("Possible moves: ", possible_moves)
            if not possible_moves:
                print("No possible moves")
                # 2. HINT WHERE MINES HAVE TO BE
                hint_cache_board = hint_mined_fields(hint_cache_board, ROWS, COLS, flagged)
                # 3. FLAG THE MINES
                hint_cache_board = correct_hinted_board(board_to_save, hint_cache_board, flagged)
                # 4. LOOK FOR MOVES ONCE AGAIN
                hint_cache_board = hint_safe_fields(hint_cache_board, ROWS, COLS)

                for i in range(ROWS):
                    for j in range(COLS):
                        if hint_cache_board[i][j] == -2 and not revealed[i][j]:
                            possible_moves.append((i, j))
                if not possible_moves:
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

