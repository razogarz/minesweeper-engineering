def game_over_reveal_bombs(grid, revealed_cells, ROWS, COLS):
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col] == -1:
                revealed_cells[row][col] = True