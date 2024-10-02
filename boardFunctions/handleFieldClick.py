def handle_field_click(grid, revealed_fields, row, col, flagged, ROWS, COLS):
    if revealed_fields[row][col] or flagged[row][col]:
        return

    revealed_fields[row][col] = True
    if grid[row][col] == 0:
        for r in range(max(0, row - 1), min(ROWS, row + 2)):
            for c in range(max(0, col - 1), min(COLS, col + 2)):
                if not revealed_fields[r][c]:
                    handle_field_click(grid, revealed_fields, r, c, flagged, ROWS, COLS)