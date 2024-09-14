def convert_to_save(grid, revealed_cells, flagged, ROWS, COLS):
    board = [[-1 for _ in range(COLS)] for _ in range(ROWS)]
    for row in range(ROWS):
        for col in range(COLS):
            if revealed_cells[row][col]:
                if grid[row][col] == -1:
                    board[row][col] = 9
                else:
                    board[row][col] = grid[row][col]
            else:
                board[row][col] = -1
    return board