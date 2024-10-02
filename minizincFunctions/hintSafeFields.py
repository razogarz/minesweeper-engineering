import numpy as np
from minizinc import Instance, Model, Solver
from gameConstants import FieldState

def hint_safe_fields(hint_cache_board, ROWS, COLS):
    """
    Send hint cache to minizinc
    """
    print("Hinting")
    temp_board = np.zeros((ROWS, COLS))
    hint = 0
    tree_depth = 0

    for i in range(ROWS):
        for j in range(COLS):
            if hint_cache_board[i][j] != FieldState.NOT_REVEALED_NEIGHBOUR.value or temp_board[i,j] == True:
                continue

            hint += 1
            minesweeper_model = Model("/mnt/c/Users/Razogarz/PycharmProjects/minesweeper-engineering/minizincModels/field_is_safe.mzn")
            gecode = Solver.lookup("gecode")

            minesweeper_model.add_file("/mnt/c/Users/Razogarz/PycharmProjects/minesweeper-engineering/minizincModels/data/data_gen.dzn", parse_data=True)
            instance = Instance(gecode,minesweeper_model)
            instance['x'] = i+1
            instance['y'] = j+1

            result = instance.solve()
            is_unsat = str(result.status) == "UNSATISFIABLE"

            if is_unsat:
                hint_cache_board[i][j] = FieldState.NOT_MINED.value
                print("Mine not possible at: ", i+1, j+1)
            else:
                temp_board = np.logical_or(temp_board, np.array(result['potential_mines']))

            tree_depth += result.statistics['peakDepth']

    return hint_cache_board, tree_depth, hint