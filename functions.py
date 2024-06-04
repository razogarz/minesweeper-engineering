import pygame
import random
import sys
from boardGenerator.boardFunctions import *

def draw_empty_board(rows, cols, grid_size, gray, screen):
    """
    Draw the empty board
    """
    for row in range(rows):
        for col in range(cols):
            pygame.draw.rect(screen, gray, (col * grid_size, row * grid_size, grid_size, grid_size))

def draw_board(screen, full_board, revealed, flagged, font, flag_font, grid_size):
    """
    Draw the board
    """
    for row in range(len(full_board)):
        for col in range(len(full_board[0])):
            if revealed[row][col]:
                pygame.draw.rect(screen, (255, 255, 255), (col * grid_size, row * grid_size, grid_size, grid_size))
                if full_board[row][col] != 0 and full_board[row][col] != 9:
                    text = font.render(str(full_board[row][col]), True, (0, 0, 0))
                    screen.blit(text, (col * grid_size + grid_size // 2 - text.get_width() // 2, row * grid_size + grid_size // 2 - text.get_height() // 2))
                elif full_board[row][col] == 9:
                    pygame.draw.circle(screen, (255, 0, 0), (col * grid_size + grid_size // 2, row * grid_size + grid_size // 2), grid_size // 4)
            elif flagged[row][col]:
                pygame.draw.rect(screen, (255, 0, 0), (col * grid_size, row * grid_size, grid_size, grid_size))
                text = flag_font.render("F", True, (0, 0, 0))
                screen.blit(text, (col * grid_size + grid_size // 2 - text.get_width() // 2, row * grid_size + grid_size // 2 - text.get_height() // 2))
            else:
                pygame.draw.rect(screen, (128, 128, 128), (col * grid_size, row * grid_size, grid_size, grid_size))

def check_game_over(full_board, revealed):
    """
    Check if the game is over
    """
    for row in range(len(full_board)):
        for col in range(len(full_board[0])):
            if full_board[row][col] == 9 and revealed[row][col]:
                return True
    return False

def check_win(full_board, revealed):
    """
    Check if the player has won
    """
    for row in range(len(full_board)):
        for col in range(len(full_board[0])):
            if full_board[row][col] != 9 and not revealed[row][col]:
                return False
    return True

def uncover_fields(revealed, full_board, row, col):
    """
    Uncover the fields
    """
    if full_board[row][col] == 9:
        revealed = [[True for _ in range(len(full_board[0]))] for _ in range(len(full_board))]
    elif full_board[row][col] != 0:
        revealed[row][col] = True
    else:
        revealed[row][col] = True
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= row + dx < len(full_board) and 0 <= col + dy < len(full_board[0]) and not revealed[row + dx][col + dy]:
                    uncover_fields(revealed, full_board, row + dx, col + dy)

    # save for minizinc
    saveForMinizinc(revealed, len(full_board), 0)

    return revealed
def draw_game_over_screen(screen):
    """
    Draw the game over screen
    """
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 50)
    text = font.render("Game Over!", True, (255, 0, 0))
    screen.blit(text, (100, 100))
    pygame.display.flip()

def draw_win_screen(screen):
    """
    Draw the win screen
    """
    screen.fill((255, 255, 255))
    font = pygame.font.SysFont(None, 50)
    text = font.render("You Win!", True, (0, 255, 0))
    screen.blit(text, (100, 100))
    pygame.display.flip()

