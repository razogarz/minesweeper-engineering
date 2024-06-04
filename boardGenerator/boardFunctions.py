import random

def naive_gen_board(size: int, number_of_mines: int, first_click: tuple) -> list:
		"""
		Generate a naive board with mines
		"""
		# Initialize the board
		board = [[0 for _ in range(size)] for _ in range(size)]
		# Place mines
		mines = set()
		while len(mines) < number_of_mines:
				x = random.randint(0, size - 1)
				y = random.randint(0, size - 1)
				if (x, y) != first_click and (x, y) not in mines:
						mines.add((x, y))
						board[x][y] = 9
						for dx in [-1, 0, 1]:
								for dy in [-1, 0, 1]:
										if 0 <= x + dx < size and 0 <= y + dy < size and board[x + dx][y + dy] != -1 and board[x + dx][y + dy] != 9:
												board[x + dx][y + dy] += 1
		return board

def draw_ascii_board(board: list) -> None:
		"""
		Draw the board
		"""
		for row in board:
				for cell in row:
						print("|", end="")
						if cell == 9:
								print("X", end="")
						elif cell == -1:
								print("H", end="")
						else:
								print(cell, end="")
				print("|")

def returnBlankBoard(size: int) -> list:
		"""
		Return a blank board
		"""
		return [[-1 for _ in range(size)] for _ in range(size)]

def uncoverFields(current_board, full_board, x, y) -> list:
		"""
		Uncover the fields
		"""
		if full_board[x][y] == 9:
				current_board[x][y] = "X"
				return current_board
		elif full_board[x][y] != 0:
				current_board[x][y] = full_board[x][y]
				return current_board
		else:
				current_board[x][y] = full_board[x][y]
				for dx in [-1, 0, 1]:
						for dy in [-1, 0, 1]:
								if 0 <= x + dx < len(full_board) and 0 <= y + dy < len(full_board) and current_board[x + dx][y + dy] == -1:
										uncoverFields(current_board, full_board, x + dx, y + dy)
				return current_board

def saveForMinizinc(board, size, number_of_mines) -> None:
		"""
		Save the board to a data file for Minizinc to run
		"""
		with open("./superSaperSolver/data/data_gen.dzn", "w") as f:
				f.write("size = {};\n".format(size))
				f.write("mines_count = {};\n".format(number_of_mines))
				f.write("fields = array2d(1..size, 1..size, [")
				for row in board:
						for cell in row:
								f.write(str(cell) + ",")
				f.write("]);\n")
		return None