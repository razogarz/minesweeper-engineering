from gameConstants import FieldState

def correct_hinted_board(board, hint_cache_board, flagged_fields):
    """
        board: -1..9 where -1 is not revealed, 9 is mined
    """
    ROWS, COLS = len(board), len(board[0])  # Ensure ROWS and COLS are defined
    for i in range(ROWS):
        for j in range(COLS):
            # Skip revealed, mined and certain non-mined fields
            if hint_cache_board[i][j] not in [FieldState.POSSIBLE_MINE.value, FieldState.NOT_REVEALED_NOT_NEIGHBOUR.value, FieldState.NOT_REVEALED_NEIGHBOUR.value]:
                continue

            # If flagged, mark as possible mine
            if flagged_fields[i][j]:
                hint_cache_board[i][j] = FieldState.POSSIBLE_MINE.value
                continue

            # Check if the field is a neighbour of a revealed (or flagged) field
            for r in range(max(0, i - 1), min(ROWS, i + 2)):
                for c in range(max(0, j - 1), min(COLS, j + 2)):
                    if (board[r][c] != -1 or flagged_fields[r][c]) and (r != i or c != j):
                        hint_cache_board[i][j] = FieldState.NOT_REVEALED_NEIGHBOUR.value

            # board[i][j] == -1 means not revealed
            if board[i][j] != -1:
                hint_cache_board[i][j] = FieldState.REVEALED.value

    return hint_cache_board

