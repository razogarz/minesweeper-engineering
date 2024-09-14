import random

def generate_mine_field(rows: int, cols: int, number_of_mines: int, first_click: tuple) -> list:
    """
    Generate a naive board with mines
    """
    # Initialize the board
    board = [[0 for _ in range(cols)] for _ in range(rows)]
    # Place mines
    mines = set()
    while len(mines) < number_of_mines:
        x = random.randint(0, rows - 1)
        y = random.randint(0, cols - 1)
        if (x, y) != first_click and (x, y) not in mines:
            mines.add((x, y))
            board[x][y] = -1
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if 0 <= x + dx < rows and 0 <= y + dy < cols and board[x + dx][y + dy] != -1:
                        board[x + dx][y + dy] += 1
    return board