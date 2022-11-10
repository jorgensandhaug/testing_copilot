"""
An application that creates a game of tic-tac-toe using pygame and allows the user to play against the computer.
The computer will be using a minimax algorithm with alpha-beta pruning to determine the best move.
"""

import pygame
from pygame.locals import *
import sys
import math
import time

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


# Define some fonts
pygame.font.init()
FONT = pygame.font.SysFont("comicsansms", 72)
FONT_SMALL = pygame.font.SysFont("comicsansms", 48)



# Define the board
BOARD = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

# Define the window
WINDOW = pygame.display.set_mode((600, 600))
WINDOW.fill(WHITE)
pygame.display.set_caption("Tic-Tac-Toe")

# Define the game state
PLAYER = 1
COMPUTER = 2
GAME_OVER = False
WINNER = 0
TIE = False

def check_win(board):
    """
    Check if the game is over.
    """
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != 0:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != 0:
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != 0:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != 0:
        return board[0][2]
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                return -1
    return 0

# Define the minimax algorithm
def minimax(board, depth, is_maximizing):
    """
    The minimax algorithm with alpha-beta pruning.
    """
    result = check_win(board)
    if result == PLAYER:
        return -10
    elif result == COMPUTER:
        return 10
    elif result == 0:
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = COMPUTER
                    score = minimax(board, depth + 1, False)
                    board[i][j] = 0
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == 0:
                    board[i][j] = PLAYER
                    score = minimax(board, depth + 1, True)
                    board[i][j] = 0
                    best_score = min(score, best_score)
        return best_score

# Draw the board
def draw_board():
    """
    Draw the board.
    """
    pygame.draw.line(WINDOW, BLACK, (200, 0), (200, 600), 10)
    pygame.draw.line(WINDOW, BLACK, (400, 0), (400, 600), 10)
    pygame.draw.line(WINDOW, BLACK, (0, 200), (600, 200), 10)
    pygame.draw.line(WINDOW, BLACK, (0, 400), (600, 400), 10)
    pygame.display.update()

# Draw the X
def draw_x(x, y):
    """
    Draw an X on the board.
    """
    pygame.draw.line(WINDOW, RED, (x * 200 + 25, y * 200 + 25), (x * 200 + 175, y * 200 + 175), 10)
    pygame.draw.line(WINDOW, RED, (x * 200 + 175, y * 200 + 25), (x * 200 + 25, y * 200 + 175), 10)
    pygame.display.update()

# Draw the O
def draw_o(x, y):
    """
    Draw an O on the board.
    """
    pygame.draw.circle(WINDOW, BLUE, (x * 200 + 100, y * 200 + 100), 75, 10)
    pygame.display.update()

# Draw the winner
def draw_winner(winner):
    """
    Draw the winner.
    """
    if winner == PLAYER:
        text = FONT.render("X Wins!", True, RED)
    elif winner == COMPUTER:
        text = FONT.render("O Wins!", True, BLUE)
    else:
        text = FONT.render("Tie!", True, BLACK)
    WINDOW.blit(text, (150, 250))
    pygame.display.update()

# Draw the computer's move
def draw_computer_move():
    """
    Draw the computer's move.
    """
    best_score = -math.inf
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if BOARD[i][j] == 0:
                BOARD[i][j] = COMPUTER
                score = minimax(BOARD, 0, False)
                BOARD[i][j] = 0
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    BOARD[best_move[0]][best_move[1]] = COMPUTER
    draw_o(best_move[1], best_move[0])

# Draw the player's move
def draw_player_move(x, y):
    """
    Draw the player's move.
    """
    BOARD[y][x] = PLAYER
    draw_x(x, y)

# Main loop
def main():
    """
    The main loop.
    """
    global PLAYER, COMPUTER, GAME_OVER, WINNER, TIE
    draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN and not GAME_OVER:
                x = event.pos[0] // 200
                y = event.pos[1] // 200
                if BOARD[y][x] == 0:
                    draw_player_move(x, y)
                    WINNER = check_win(BOARD)
                    if WINNER != -1:
                        GAME_OVER = True
                        draw_winner(WINNER)
                    else:
                        draw_computer_move()
                        WINNER = check_win(BOARD)
                        if WINNER != -1:
                            GAME_OVER = True
                            draw_winner(WINNER)
        pygame.display.update()

if __name__ == "__main__": 
    main()

