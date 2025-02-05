# Inspiration: https://rosettacode.org/wiki/2048

import pygame
import pygame.display as display
import time
import random
from game_board import game_board

# Window size

window_width = 720
window_height = 480

# Colors
background_color = pygame.Color(232, 220, 202)
red = pygame.Color(255, 0, 0)
white = pygame.Color(255, 255, 255)
black = pygame.Color(0,0,0)

color_map = { 0:pygame.Color(211, 211, 211) }

# Initiate pygame
pygame.init()

# Initialize game window
display.set_caption('2048')
game_window = display.set_mode((window_width, window_height))
fps = pygame.time.Clock()

# Initialize the game state

grid_width, grid_height = 4, 4
win_condition, spawn_four_chance = 16384, 0.1

game = game_board(grid_width, grid_height, win_condition, spawn_four_chance)

def show_scores(color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(game.score), True, color)
    score_rect = score_surface.get_rect()
    game_window.blit(score_surface, score_rect)

def gameOver():
    game_over_font = pygame.font.SysFont('times new roman', 50)
    game_over_surface = game_over_font.render('Your Score is : ' + str(game.score), True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_width/2, window_width/4)
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(3)
    game.reset_game()
    pygame.display.update()
    #pygame.quit()
    #quit()

tile_size = 100

def GetScoreColor(val):

    if val not in color_map:
        R = random.randrange(0, 255)
        G = random.randrange(0, 255)
        B = random.randrange(0, 255)
        color_map[val] = pygame.Color(R, G, B)

    return color_map[val]

def drawBoard():
    game_window.fill(background_color)
    for col in range(grid_width):
        for row in range(grid_height):

            tile_val = game.grid[row][col]
            x = tile_size * (col - grid_width // 2) + window_width / 2
            y = tile_size * (row - grid_height // 2) + window_height / 2

            color = GetScoreColor(tile_val)

            pygame.draw.rect(game_window, color, pygame.Rect(x, y, tile_size, tile_size))

            if tile_val > 0:
                tile_font = pygame.font.SysFont('times new roman', 50)
                tile_surface = tile_font.render(str(tile_val), True, black)
                tile_rect = tile_surface.get_rect()
                tile_rect.midtop = (x + tile_size/2, y + tile_size/4)
                game_window.blit(tile_surface, tile_rect)
                pygame.display.flip()


drawBoard()

while True:

    next_action = None

    for event in pygame.event.get():
        if event.type == pygame.KEYUP:
            match event.key:
                case pygame.K_UP:
                    next_action = "UP"
                case pygame.K_DOWN:
                    next_action = "DOWN"
                case pygame.K_LEFT:
                    next_action = "LEFT"
                case pygame.K_RIGHT:
                    next_action = "RIGHT"

    # If player made a move and the game allowed the move
    if next_action is not None and game.move(next_action):
        
        # Change the display
        drawBoard()
        
        # Check if the player has lost
        if game.has_lost():
            gameOver()

    show_scores(white, 'times new roman', 20)

    pygame.display.update()
