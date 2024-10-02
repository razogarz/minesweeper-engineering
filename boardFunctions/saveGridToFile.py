def save_grid_to_file(grid, difficulty, row, col, named=False):
    """
    Safe the grid that has been proven to be solvable to a file
    """
    if named:
        name = input("Enter name of the board: ")
        file_string = f'./provenBoards/custom/{name}.csv'
    else:
        file_string = f'./provenBoards/{difficulty}/data_gen_r{row}_c{col}.csv'
    with open(file_string, "w") as f:
        for row in grid:
            for cell in row:
                f.write(str(cell) + ",")
            f.write("\n")
    return None