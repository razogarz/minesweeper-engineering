def correct_hinted_board(board, hint_cache_board, flagged_fields):
    """
        hint_cache_board[x,y] = -2 - not mine
        hint_cache_board[x,y] = -1 - possible mine
        hint_cache_board[x,y] = 0 - not revealed, not neighbour of revealed
        hint_cache_board[x,y] = 1 - not revealed, neighbour of revealed
        hint_cache_board[x,y] = 2 - revealed
    """
    ROWS, COLS = len(board), len(board[0])  # Ensure ROWS and COLS are defined
    for i in range(ROWS):
        for j in range(COLS):
            if hint_cache_board[i][j] not in [-1, 0, 1]:
                continue

            if flagged_fields[i][j]:
                hint_cache_board[i][j] = -1
                continue

            for r in range(max(0, i - 1), min(ROWS, i + 2)):
                for c in range(max(0, j - 1), min(COLS, j + 2)):
                    if (board[r][c] != -1 or flagged_fields[r][c]) and (r != i or c != j):
                        hint_cache_board[i][j] = 1

            if board[i][j] != -1:
                hint_cache_board[i][j] = 2

    return hint_cache_board