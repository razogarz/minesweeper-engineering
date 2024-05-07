from pythonScripts.boardFunctions import *

def main():
		"""
		Generate a naive board with mines
		"""
		size = 10
		number_of_mines = 15
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

		saveForMinizinc(covered_board, size, first_click)
		
	
if __name__ == "__main__":
		main()