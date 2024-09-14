def check_win(revealed_fields, grid, ROWS, COLS) -> bool:
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] != -1 and not revealed_fields[row][col]:
                return False
    return True