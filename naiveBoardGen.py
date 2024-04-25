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
						board[x][y] = -1
						for dx in [-1, 0, 1]:
								for dy in [-1, 0, 1]:
										if 0 <= x + dx < size and 0 <= y + dy < size and board[x + dx][y + dy] != -1:
												board[x + dx][y + dy] += 1
		return board

def draw_ascii_board(board: list) -> None:
		"""
		Draw the board
		"""
		for row in board:
				for cell in row:
						print("|", end="")
						if cell == -1:
								print("X", end="")
						else:
								print(cell, end="")
				print("|")

