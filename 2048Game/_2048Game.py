# Inspiration: https://rosettacode.org/wiki/2048

import pygame
import pygame.display as display
import game_board

# Window size

window_width = 720
window_height = 480

# Colors
background_color = pygame.color(232, 220, 202)
white = pygame.color(0, 0, 0)

# Initiate pygame
pygame.init()

# Initialize game window
display.set_caption('2048')
game_window = display.set_mode((window_width, window_height))
fps = pygame.time.Clock()

# Initialize the game state

game = game_board()

