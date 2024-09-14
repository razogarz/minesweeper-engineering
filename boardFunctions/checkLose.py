def check_lose(grid, revealed_cells, ROWS, COLS)->bool:
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == -1 and revealed_cells[row][col]:
                return True
    return False