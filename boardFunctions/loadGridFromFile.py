def load_grid_from_file(difficulty, row, col, named=False):
    """
    Load the grid that has been proven to be solvable from a file
    """
    if named:
        name = input("Enter name of the board: ")
        name_string = f'./provenBoards/custom/{name}.csv'
    else:
        name_string = f'./provenBoards/{difficulty}/data_gen_r{row}_c{col}.csv'

    with open(name_string, "r") as f:
        grid = []
        for line in f:
            grid.append([int(cell) for cell in line.split(",")[:-1]])

        print(grid)
    return grid