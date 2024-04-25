from naiveBoardGen import draw_ascii_board, naive_gen_board


def main():
		"""
		Generate a naive board with mines
		"""
		size = 10
		number_of_mines = 10
		first_click = (4, 5)
		board = naive_gen_board(size, number_of_mines, first_click)
		draw_ascii_board(board)
	
if __name__ == "__main__":
		main()