"""
Minesweeper game using pygame. 
"""

import pygame
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Define some fonts
pygame.font.init()
FONT = pygame.font.SysFont("comicsansms", 72)
FONT_SMALL = pygame.font.SysFont("comicsansms", 48)



# Define the window
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Minesweeper")

# Define the board
BOARD = [[0 for i in range(10)] for j in range(10)]
BOMB = 9
BOMB_COUNT = 10
BOMB_LOCATIONS = []
for i in range(BOMB_COUNT):
    while True:
        row = random.randint(0, 9)
        col = random.randint(0, 9)
        if BOARD[row][col] != BOMB:
            BOARD[row][col] = BOMB
            BOMB_LOCATIONS.append((row, col))
            break
for row in range(10):
    for col in range(10):
        if BOARD[row][col] != BOMB:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if row + i >= 0 and row + i < 10 and col + j >= 0 and col + j < 10:
                        if BOARD[row + i][col + j] == BOMB:
                            BOARD[row][col] += 1

# Define the game state
GAME_OVER = False
WINNER = 0
TIE = False

def draw_board():
    """
    Draw the board. The bombs should be hidden.
    """
    for row in range(10):
        for col in range(10):
            pygame.draw.rect(WIN, BLACK, (row * 80, col * 80, 80, 80), 1)
            if BOARD[row][col] == -1:
                pygame.draw.rect(WIN, BLACK, (row * 80, col * 80, 80, 80), 0)
                text = FONT_SMALL.render(str(BOARD[row][col]), True, BLACK)
                WIN.blit(text, (row * 80 + 40 - text.get_width() / 2,
                                col * 80 + 40 - text.get_height() / 2))
            elif BOARD[row][col] == BOMB:
                pygame.draw.rect(WIN, BLACK, (row * 80, col * 80, 80, 80), 0)
                text = FONT_SMALL.render("X", True, BLACK)
                WIN.blit(text, (row * 80 + 40 - text.get_width() / 2,
                                col * 80 + 40 - text.get_height() / 2))
            elif BOARD[row][col] == 0:
                pygame.draw.rect(WIN, BLACK, (row * 80, col * 80, 80, 80), 0)
            else:
                pygame.draw.rect(WIN, BLACK, (row * 80, col * 80, 80, 80), 0)
                text = FONT_SMALL.render(str(BOARD[row][col]), True, BLACK)
                WIN.blit(text, (row * 80 + 40 - text.get_width() / 2,
                                col * 80 + 40 - text.get_height() / 2))

def check_win():
    """
    Check if the game is over.
    """
    for row in range(10):
        for col in range(10):
            if BOARD[row][col] != BOMB:
                return False
    return True


def main():
    """
    Main function.
    """
    global GAME_OVER
    global WINNER
    global TIE
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row = pos[0] // 80
                col = pos[1] // 80
                if BOARD[row][col] == BOMB:
                    GAME_OVER = True
                    WINNER = 1
                else:
                    BOARD[row][col] = -1
                    if check_win():
                        GAME_OVER = True
                        WINNER = 2
        if GAME_OVER:
            if WINNER == 1:
                text = FONT.render("You lose!", True, BLACK)
            else:
                text = FONT.render("You win!", True, BLACK)
            WIN.blit(text, (WIDTH / 2 - text.get_width() / 2, WIDTH / 2 - text.get_height() / 2))
        else:
            draw_board()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()
    