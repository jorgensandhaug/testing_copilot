"""
A snake game written in Python using the Pygame library using the arrows key to move the snake.
The snake is made up of a series of blue rectangles. The apple is a red rectangle.
"""

import sys
import random
import pygame
import time # To use time.sleep() function


# Global Variables to be used through our program
fps = 10
fps_clock = pygame.time.Clock()
# Play Surface
play_surface = pygame.display.set_mode((720, 460))
pygame.display.set_caption('Snake Game!')
# Colors
red = pygame.Color(255, 0, 0)  # gameover
green = pygame.Color(0, 255, 0)  # snake
black = pygame.Color(0, 0, 0)  # score
white = pygame.Color(255, 255, 255)  # background
brown = pygame.Color(165, 42, 42)  # food
# Game Variables
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
food_pos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
food_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0


def show_score(choice=1):
    s_font = pygame.font.SysFont('monaco', 24)
    s_surface = s_font.render('Score : {0}'.format(score), True, black)
    s_rect = s_surface.get_rect()
    if choice == 1:
        s_rect.midtop = (80, 10)
    else:
        s_rect.midtop = (360, 120)
    play_surface.blit(s_surface, s_rect)

# Game Over Function
def game_over():
    my_font = pygame.font.SysFont('monaco', 72)
    game_over_surface = my_font.render('Game Over!', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (360, 15)
    play_surface.blit(game_over_surface, game_over_rect)
    show_score(0)
    pygame.display.flip()
    time.sleep(5)
    sys.exit()  # console exit




def main():
    """
    This is the main function for our snake game.
    """
    global fps_clock, play_surface, fps, snake_pos, snake_body, food_pos, food_spawn, direction, change_to, score
    
    # initializing pygame

    pygame.init()

    while True:  # game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
        # Making sure the snake cannot move in the opposite direction instantaneously
        if change_to == 'RIGHT' and not direction == 'LEFT':
            direction = 'RIGHT'
        if change_to == 'LEFT' and not direction == 'RIGHT':
            direction = 'LEFT'
        if change_to == 'UP' and not direction == 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and not direction == 'UP':
            direction = 'DOWN'
        # Moving the snake
        if direction == 'RIGHT':
            snake_pos[0] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        # Snake body mechanism
        snake_body.insert(0, list(snake_pos))
        if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
            score += 1
            food_spawn = False
        else:
            snake_body.pop()
        # Spawning food on the screen
        if food_spawn == False:
            food_pos = [random.randrange(1, 72) * 10, random.randrange(1, 46) * 10]
        food_spawn = True
        # GFX
        play_surface.fill(white)
        for pos in snake_body:
            pygame.draw.rect(play_surface, green, pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(play_surface, brown, pygame.Rect(food_pos[0], food_pos[1], 10, 10))
        # Game Over conditions
        # Getting out of bounds
        if snake_pos[0] > 710 or snake_pos[0] < 0:
            game_over()
        if snake_pos[1] > 450 or snake_pos[1] < 0:
            game_over()
        # Touching the snake body
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over()
        show_score()
        pygame.display.flip()
        fps_clock.tick(fps)


# Calling the main function
main()
