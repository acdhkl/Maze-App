##################################
# Maze Game and Visualizer
# Avinav Dhakal
# Last revised : Feb 12 2021
##################################

import pygame
import time
import random

# Set pygame window constants
WIDTH = 800
HEIGHT = 800
FPS = 30

# Set color constants
PURPLE = (42, 14, 92)     # background colour
WHITE = (255, 255, 255)   # wall colour
GREEN = (0, 255, 0)       # current cell indicator colour
BLUE = (0, 0, 255)        # maze colour

# Initialise pygame window
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game and Visualizer")
window.fill(PURPLE)
pygame.display.flip()
clock = pygame.time.Clock()

# Function to create square grid with cell width: w, dimension: dim x dim


def create_grid(w, dim):
    y = 0
    for i in range(1, dim + 1):
        x = w
        y += w
        for j in range(1, dim + 1):
            pygame.draw.line(window, WHITE, [x, y], [
                x + w, y])           # top of cell
            # right of cell
            pygame.draw.line(window, WHITE, [x + w, y], [x + w, y + w])
            # bottom of cell
            pygame.draw.line(window, WHITE, [x + w, y + w], [x, y + w])
            # left of cell
            pygame.draw.line(window, WHITE, [x, y + w], [x, y])
            grid.append((x, y))
            x += w


# Function to generate a random maze starting at coordinates: (x,y), cell width: w

def generate_maze(x, y, w):
    stack.append((x, y))  # add starting cell to stack
    visited.add((x, y))  # add starting cell to visited set
    while len(stack) > 0:
        time.sleep(0.03)  # add brief pause to make animations slower
        cells = []       # create list to store unvisted neighbours of current cell

        if (x, y - w) not in visited and (x, y - w) in grid:  # ABOVE NEIGHBOUR
            cells.append("above")

        if (x+w, y) not in visited and (x + w, y) in grid:  # RIGHT NEIGHBOUR
            cells.append("right")

        if (x, y + w) not in visited and (x, y + w) in grid:  # BELOW NEIGHBOUR
            cells.append("below")

        if (x - w, y) not in visited and (x - w, y) in grid:  # LEFT NEIGHBOUR
            cells.append("left")

        if len(cells) > 0:
            chosen_cell = (random.choice(cells))

            # For randomly picked neighbour, colour it blue, add it to solution path, stack, and visted set
            if chosen_cell == "above":
                pygame.draw.rect(
                    window, BLUE, (x + 1, y - w + 1, w-1, 2*w-1), 0)
                pygame.display.update()
                solution_path[(x, y - w)] = x, y
                y -= w
                visited.add((x, y))
                stack.append((x, y))

            elif chosen_cell == "right":
                pygame.draw.rect(
                    window, BLUE, (x + 1, y + 1, 2*w-1, w-1), 0)
                pygame.display.update()
                solution_path[(x + w, y)] = x, y
                x += w
                visited.add((x, y))
                stack.append((x, y))

            elif chosen_cell == "below":
                pygame.draw.rect(
                    window, BLUE, (x + 1, y + 1, w-1, 2*w-1), 0)
                pygame.display.update()
                solution_path[(x, y + w)] = x, y
                y += w
                visited.add((x, y))
                stack.append((x, y))

            elif chosen_cell == "left":
                pygame.draw.rect(
                    window, BLUE, (x - w + 1, y + 1, 2*w-1, w-1), 0)
                pygame.display.update()
                solution_path[(x - w, y)] = x, y
                x -= w
                visited.add((x, y))
                stack.append((x, y))
        # If there are no viable neighbours, backtrack and pop a cell from the stack
        # Colour flash that cell green to indicate backtracking, then colour blue
        else:
            x, y = stack.pop()
            pygame.draw.rect(window, GREEN, (x + 1, y + 1, w-2, w-2), 0)
            pygame.display.update()
            time.sleep(0.01)
            # re-colour the path
            pygame.draw.rect(window, BLUE, (x + 1, y + 1, w-2, w-2), 0)
            pygame.display.update()


# Infinite loop to keep pygame window open
running = True
create_maze = True  # Check if first iteration
while running:
    clock.tick(FPS)
    # Check if QUIT event occurs, if so, window closes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # If first iteration of while loop:
        # 1) instantiate maze variables
        # 2) create grid
        # 3) generate maze

    if create_maze:
        grid = []
        stack = []
        visited = set()
        solution_path = {}

        # Set cell to start generating maze from
        ### MUST BE A MULTIPLE OF cell_width ###
        dimension = 20
        x = 40
        y = 40
        cell_width = 10

        create_grid(cell_width, dimension)
        pygame.display.update()
        generate_maze(x, y, cell_width)

        create_maze = False  # Indicate maze is done being created
