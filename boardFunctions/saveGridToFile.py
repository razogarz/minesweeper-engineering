def save_grid_to_file(grid, difficulty, row, col):
    """
    Safe the grid that has been proven to be solvable to a file
    """
    with open(f'./provenBoards/{difficulty}/data_gen_r{row}_c{col}.csv', "w") as f:
        for row in grid:
            for cell in row:
                f.write(str(cell) + ",")
            f.write("\n")
    return None