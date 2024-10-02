import random

from boardFunctions.drawAsciiBoard import draw_ascii_board


def add_outer_layer(grid: list, click: tuple, mines: int) -> list:
    mine_density = mines / (len(grid) * len(grid[0]))
    new_mine_count = int(mine_density * (len(grid) + 2) * (len(grid[0]) + 2))
    current_mine_count = mines

    new_grid = [[0 for _ in range(len(grid[0]) + 2)] for _ in range(len(grid) + 2)]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            new_grid[i + 1][j + 1] = grid[i][j]

    while current_mine_count < new_mine_count:
        x = random.randint(0, len(grid) + 1)
        y = random.randint(1, len(grid[0]) + 1)
        if (x,y) != click and new_grid[x][y] != -1 and (x == 0 or x == len(grid) + 1 or y == 0 or y == len(grid[0]) + 1):
            new_grid[x][y] = -1
            current_mine_count += 1

        for r in range(len(grid) + 2):
            for c in range(len(grid[0]) + 2):
                if new_grid[r][c] == -1:
                    continue
                num = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if 0 <= r + dx < len(grid) + 2 and 0 <= c + dy < len(grid[0]) + 2 and new_grid[r + dx][c + dy] == -1:
                            num += 1
                new_grid[r][c] = num
    draw_ascii_board(new_grid)
    return [new_grid, new_mine_count]
