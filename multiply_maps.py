'''
    USE SYMMETRY AND 0 FIELDS TO GENERATE MORE MAPS
'''
import numpy as np

from boardFunctions.saveGridToFile import save_grid_to_file


def main(diff, x, y):
    """
    Generate a naive board with mines
    """
    with open(f'./superMSSolver/generatedNoGuesser/{diff}/data_gen_r{x}_c{y}.csv', "r") as f:
        grid = []
        for line in f:
            grid.append([])
            for cell in line.split(","):
                if cell == "\n":
                    continue
                grid[-1].append(int(cell))
    rows = len(grid)
    cols = len(grid[0])
    symmetrical_click = [(x,y),(rows-1-x,y) , (x,cols-1-y), (rows-1-x,cols-1-y)]

    # SYMMETRY BY X
    grid_x = np.flip(grid, axis=0)

    # SYMMETRY BY Y
    grid_y = np.flip(grid, axis=1)

    # SYMMETRY BY X AND Y
    grid_xy = np.flip(grid_x, axis=1)


    # SAVE
    save_grid_to_file(grid_x, diff, symmetrical_click[1][0], symmetrical_click[1][1])
    save_grid_to_file(grid_y, diff, symmetrical_click[2][0], symmetrical_click[2][1])
    save_grid_to_file(grid_xy, diff, symmetrical_click[3][0], symmetrical_click[3][1])


if __name__ == "__main__":
    main("hard", 9, 9)
