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