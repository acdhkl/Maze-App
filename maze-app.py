##################################
# Maze Game and Visualizer
# Avinav Dhakal
# Last revised : Feb 2 2021
##################################

import pygame

# Set pygame window constants
WIDTH = 800
HEIGHT = 800

# Set color constants
PURPLE = (42,14,92)     # background colour
WHITE = (255,255,255)   # wall colour

# Initialise pygame window
pygame.init()
window =  pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game and Visualizer")
window.fill(PURPLE)

# Function to create square grid
def create_grid(x,y,cell_width,dim):
    for i in range(dim):
        x = cell_width
        y += cell_width
        for j in range(dim):
            pygame.draw.line(window,WHITE,[x,y],[x + cell_width, y])                           # top wall
            pygame.draw.line(window,WHITE,[x + cell_width,y],[x + cell_width, y + cell_width]) # right wall
            pygame.draw.line(window,WHITE,[x,y + cell_width],[x + cell_width, y + cell_width]) # bottom wall
            pygame.draw.line(window,WHITE,[x,y],[x, y + cell_width])                           # left wall
            pygame.display.flip()
            x += cell_width


create_grid(40,0,30,20)

# Ininite loop to keep pygame window open
running = True
while running:
    # Check if QUIT event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False