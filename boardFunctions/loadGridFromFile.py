def load_grid_from_file(difficulty, row, col):
    """
    Load the grid that has been proven to be solvable from a file
    """
    print(difficulty, row, col)
    with open(f'./provenBoards/{difficulty}/data_gen_r{row}_c{col}.csv', "r") as f:
        grid = []
        for line in f:
            grid.append([int(cell) for cell in line.split(",")[:-1]])

        print(grid)
    return grid