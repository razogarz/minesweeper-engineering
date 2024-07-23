from boardGenerator.boardFunctions import *

def main():
		"""
		Generate a naive board with mines
		"""
		size = 15
		number_of_mines = 25
		first_click = (4, 5)

		while True:
			full_board = naive_gen_board(size, number_of_mines, first_click)
			if full_board[first_click[0]][first_click[1]] == 0:
				break
		
		covered_board = returnBlankBoard(size)
		draw_ascii_board(full_board)
		covered_board = uncoverFields(covered_board, full_board, first_click[0], first_click[1])
		print("\n")
		draw_ascii_board(covered_board)
		print(covered_board)
		save_for_minizinc(covered_board, size, number_of_mines)


if __name__ == "__main__":
		main()