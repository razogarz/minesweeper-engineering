import random
import time

from boardFunctions.checkLose import check_lose
from gameConstants import FieldState
from minizincFunctions.convertToSave import convert_to_save
from minizincFunctions.correctHintedBoard import correct_hinted_board
from minizincFunctions.hintMinedFields import hint_mined_fields
from minizincFunctions.hintSafeFields import hint_safe_fields
from minizincFunctions.saveForMinizinc import save_for_minizinc

from boardFunctions.handleFieldClick import handle_field_click
from boardFunctions.checkWin import check_win
from boardFunctions.drawAsciiBoard import draw_ascii_board
from boardFunctions.generateMineField import generate_mine_field



def smart_generate_board(ROWS, COLS, NUM_MINES, difficulty) -> bool:
    '''
            hint_cache_board[x,y] = -3 - mine
            hint_cache_board[x,y] = -2 - not mine
            hint_cache_board[x,y] = -1 - possible mine
            hint_cache_board[x,y] = 0 - not revealed, not neighbour of revealed
            hint_cache_board[x,y] = 1 - not revealed, neighbour of revealed
            hint_cache_board[x,y] = 2 - revealed
    '''

    first_click = True
    running = True
    game_over_flag = False

    revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
    flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
    hint_cache_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    possible_moves = []
    empty_fields = []
    prev_grid = None
    grid = None

    sum_of_hints = 0
    sum_of_tree_depth = 0
    time_start = time.time()

    original_x = int(input("Enter x coordinate: "))
    original_y = int(input("Enter y coordinate: "))

    while running:
        #-----------------------HANDLE CLICKS-------------------------
        if first_click:
            first_click = False
            grid, NUM_MINES = handle_first_click(
                ROWS, COLS, NUM_MINES, original_x, original_y, revealed, flagged, empty_fields, prev_grid, grid
            )
        elif not first_click and len(possible_moves) > 0:
            # Normal click
            while len(possible_moves) > 0:
                x, y = possible_moves.pop(0)
                handle_field_click(grid, revealed, x, y, flagged, ROWS, COLS)
        else:
            # No possible moves
            game_over_flag = True

        #-----------------------CHECK GAME OVER------------------------
        if check_win(revealed, grid, ROWS, COLS):
            print("FOUND U")
            print("Average tree depth: ", sum_of_tree_depth / sum_of_hints)
            time_end = time.time()
            time_passed = time_end - time_start
            print(f'Time taken: {int(time_passed / 3600)}h {int(time_passed / 60)}m {int(time_passed % 60)}s')
            draw_ascii_board(grid)
            # save_grid_to_file(grid, difficulty, original_x, original_y)
            con = input("Continue? (y/n): ")
            if con == "n":
                return True

            prev_grid = grid
            ROWS += 2
            COLS += 2
            original_x += 1
            original_y += 1
            game_over_flag = True
            time_start = time.time()
        else:
            print("LETS ROLL")
            board_to_save = convert_to_save(grid, revealed, flagged, ROWS, COLS)
            not_mines = [[0] * COLS for _ in range(ROWS)]
            for i in range(ROWS):
                for j in range(COLS):
                    if hint_cache_board[i][j] == FieldState.NOT_MINED.value:
                        not_mines[i][j] = 1
            save_for_minizinc(board_to_save, ROWS, COLS, NUM_MINES, not_mines)
            hint_cache_board = correct_hinted_board(board_to_save, hint_cache_board, flagged)
            hint_cache_board, tree_depth, num_of_hints = hint_safe_fields(hint_cache_board, ROWS, COLS)
            sum_of_hints += num_of_hints
            sum_of_tree_depth += tree_depth

            for i in range(ROWS):
                for j in range(COLS):
                    if hint_cache_board[i][j] == FieldState.NOT_MINED.value and not revealed[i][j]:
                        possible_moves.append((i, j))

            print("Possible moves HERE: ", possible_moves)
            if not possible_moves:
                print("No possible moves")
                # 2. HINT WHERE MINES HAVE TO BE
                hint_cache_board = hint_mined_fields(hint_cache_board, ROWS, COLS, flagged)
                # 3. FLAG THE MINES
                hint_cache_board = correct_hinted_board(board_to_save, hint_cache_board, flagged)
                # 4. LOOK FOR MOVES ONCE AGAIN
                hint_cache_board, tree_depth, num_of_hints = hint_safe_fields(hint_cache_board, ROWS, COLS)

                for i in range(ROWS):
                    for j in range(COLS):
                        if hint_cache_board[i][j] == FieldState.NOT_MINED.value and not revealed[i][j]:
                            possible_moves.append((i, j))
                            sum_of_tree_depth += tree_depth
                            sum_of_hints += num_of_hints
                if not possible_moves:
                    game_over_flag = True


        #-----------------------RESTART GAME-------------------------
        if game_over_flag:
            print("Restarting")
            game_over_flag = False
            first_click = True
            grid = None
            revealed = [[False for _ in range(COLS)] for _ in range(ROWS)]
            flagged = [[False for _ in range(COLS)] for _ in range(ROWS)]
            possible_moves = []
            hint_cache_board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
            sum_of_tree_depth = 0
            sum_of_hints = 0
            continue

    return False

def add_outer_layer(grid: list, click: tuple, mines: int) -> list:
    mine_density = mines / (len(grid) * len(grid[0]))
    new_mine_count = int(mine_density * (len(grid) + 2) * (len(grid[0]) + 2))
    current_mine_count = mines

    new_grid = [[0 for _ in range(len(grid[0]) + 2)] for _ in range(len(grid) + 2)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            new_grid[i + 1][j + 1] = grid[i][j]

    while current_mine_count < new_mine_count:
        x = random.randint(0, len(grid) + 1)
        y = random.randint(1, len(grid[0]) + 1)
        if (x,y) != click and new_grid[x][y] != -1 and (x == 0 or x == len(grid) + 1 or y == 0 or y == len(grid[0]) + 1):
            new_grid[x][y] = -1
            current_mine_count += 1

        for r in range(len(grid) + 2):
            for c in range(len(grid[0]) + 2):
                if new_grid[r][c] == -1:
                    continue
                num = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= r + dx < len(grid) + 2 and 0 <= c + dy < len(grid[0]) + 2 and new_grid[r + dx][c + dy] == -1:
                            num += 1
                new_grid[r][c] = num
    draw_ascii_board(new_grid)
    return [new_grid, new_mine_count]

def handle_first_click(
        ROWS: int, COLS: int, NUM_MINES: int, original_x: int, original_y: int, revealed: list, flagged: list,
        empty_fields: list, prev_grid: list, grid: list
):
    new_mines_count = NUM_MINES
    while True:
        if not prev_grid:
            grid = generate_mine_field(ROWS, COLS, NUM_MINES, (original_x, original_y))
            if grid[original_x][original_y] == 0:
                break
        else:
            grid, new_mines_count = add_outer_layer(prev_grid, (original_x, original_y), NUM_MINES)
            break
    handle_field_click(grid, revealed, original_x, original_y, flagged, ROWS, COLS)
    for row in range(ROWS):
        for col in range(COLS):
            if revealed[row][col] and grid[row][col] == -1:
                print(row, col)
    # Save the empty fields
    for i in range(ROWS):
        for j in range(COLS):
            if revealed[i][j] and grid[i][j] == 0:
                empty_fields.append((i, j))

    return [grid, new_mines_count]