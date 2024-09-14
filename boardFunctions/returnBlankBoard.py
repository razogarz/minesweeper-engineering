def return_blank_board(size: int) -> list:
		"""
		Return a blank board
		"""
		return [[-1 for _ in range(size)] for _ in range(size)]