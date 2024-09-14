from gameConstants import *
import pygame

def draw_grid(grid, revealed, flagged, screen, font, flag_font, hint_cache_board, ROWS, COLS, GRID_SIZE):
    """
    Draw the minesweeper grid
    """

    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect((col + 1) * GRID_SIZE, (row + 1) * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            if revealed[row][col]:
                if grid[row][col] == -1:
                    pygame.draw.rect(screen, RED, rect)
                else:
                    pygame.draw.rect(screen, WHITE, rect)
                    pygame.draw.rect(screen, BLACK, rect, 1)
                    if grid[row][col] > 0:
                        text = font.render(str(grid[row][col]), True, BLACK)
                        screen.blit(text, ((col + 1) * GRID_SIZE + 10, (row + 1) * GRID_SIZE + 5))
            elif hint_cache_board[row][col] == -2:
                pygame.draw.rect(screen, GREEN, rect)
            else:
                pygame.draw.rect(screen, GRAY, rect)
                pygame.draw.rect(screen, BLACK, rect, 1)
                if flagged[row][col]:
                    flag_text = flag_font.render('F', True, BLUE)
                    screen.blit(flag_text, ((col + 1) * GRID_SIZE + 10, (row + 1) * GRID_SIZE + 5))

    # Draw row numbers
    for row in range(ROWS):
        row_text = font.render(str(row + 1), True, BLACK)
        screen.blit(row_text, (10, (row + 1) * GRID_SIZE + 10))

    # Draw column numbers
    for col in range(COLS):
        col_text = font.render(str(col + 1), True, BLACK)
        screen.blit(col_text, ((col + 1) * GRID_SIZE + 10, 10))
