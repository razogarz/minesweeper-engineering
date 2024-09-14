def save_for_minizinc(board, rows, cols, number_of_mines, not_mines) -> None:
		"""
		Save the board to a data file for Minizinc to run
		"""
		with open("./minizincModels/data/data_gen.dzn", "w") as f:
				f.write("rows = {};\n".format(rows))
				f.write("cols = {};\n".format(cols))
				f.write("mines_count = {};\n".format(number_of_mines))
				f.write("not_mines = array2d(1..rows, 1..cols, [")
				for row in not_mines:
					for cell in row:
						f.write(str(cell) + ",")
				f.write("]);\n")
				f.write("fields = array2d(1..rows, 1..cols, [")
				for row in board:
						for cell in row:
								f.write(str(cell) + ",")
				f.write("]);\n")
		return None