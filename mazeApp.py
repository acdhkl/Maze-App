##################################
# Maze Game and Visualizer
# Avinav Dhakal
# Last revised : Feb 272021
# Known Bugs:
#             start_game function only works on first time clicking Start on menu
##################################

# Import Modules
import pygame
import pygame_menu
import time
import random


# Set pygame window constants
WIDTH = 800
HEIGHT = 800
FPS = 30
TIMEOUT = 0

# Set color constants
PURPLE = (42, 14, 92)    # background colour
RED = (250,0,0)
WHITE = (255, 255, 255)  # wall colour
GREEN = (0, 255, 0)      # backtracking cell indicator colour
BLUE = (0, 0, 255)       # maze colour
YELLOW = (255, 255, 0)   # solution dot colour
BLACK = (0, 0, 0)

font = "Retro.ttf"

# Maze specific variables
grid = []
stack = []
visited = set()
solution_path = {}

clock = pygame.time.Clock()

################### HELPER FUNCTIONS TO COLOUR IN MAZE PATH ####################

def colour_above(x, y, w):
    pygame.draw.rect(window, BLUE, (x + 1, y - w + 1, w - 1, 2 * w - 1), 0)
    pygame.display.update()


def colour_right(x, y, w):
    pygame.draw.rect(window, BLUE, (x + 1, y + 1, 2 * w - 1, w - 1), 0)
    pygame.display.update()


def colour_below(x, y, w):
    pygame.draw.rect(window, BLUE, (x + 1, y + 1, w - 1, 2 * w - 1), 0)
    pygame.display.update()


def colour_left(x, y, w):
    pygame.draw.rect(window, BLUE, (x - w + 1, y + 1, 2 * w - 1, w - 1), 0)
    pygame.display.update()

def add_dot(x, y,cell_width):
    pygame.draw.circle(
        window, YELLOW, (x + cell_width / 2, y + cell_width / 2), cell_width / 6
    )
    pygame.display.update()


def show_solution(x1, y1, x2, y2, cell_width):
    add_dot(x2, y2,cell_width)
    while (x2, y2) != (x1, y1):
        x2, y2 = solution_path[x2, y2]
        add_dot(x2, y2,cell_width)

# Function to create square grid with cell width: w, dimension: dim x dim
def create_grid(w, dim):
    y = 0
    for i in range(1, dim + 1):
        x = w
        y += w
        for j in range(1, dim + 1):
            # ABOVE CELL
            pygame.draw.line(window, WHITE, [x, y], [x + w, y])

            # RIGHT OF CELL
            pygame.draw.line(window, WHITE, [x + w, y], [x + w, y + w])

            # BELOW CELL
            pygame.draw.line(window, WHITE, [x + w, y + w], [x, y + w])

            # LEFT OF CELL
            pygame.draw.line(window, WHITE, [x, y + w], [x, y])

            # Add coordinate to grid list
            grid.append((x, y))

            x += w

# Main Menu

################################################################################
# Function to generate a random maze starting at coordinates: (x,y), cell width: w

def generate_maze(x, y, w):
    stack.append((x, y))  # add starting cell to stack
    visited.add((x, y))   # add starting cell to visited set

    while len(stack) > 0:
        time.sleep(TIMEOUT)  # add brief pause to make animations slower
        cells = []           # create list to store unvisted neighbours of current cell

        if (x, y - w) not in visited and (x, y - w) in grid:  # ABOVE NEIGHBOUR
            cells.append("above")

        if (x + w, y) not in visited and (x + w, y) in grid:  # RIGHT NEIGHBOUR
            cells.append("right")

        if (x, y + w) not in visited and (x, y + w) in grid:  # BELOW NEIGHBOUR
            cells.append("below")

        if (x - w, y) not in visited and (x - w, y) in grid:  # LEFT NEIGHBOUR
            cells.append("left")

        if len(cells) > 0:
            chosen_cell = random.choice(cells)

            # For randomly picked neighbour, colour it blue, add it to solution path, stack, and visted set
            if chosen_cell == "above":
                colour_above(x, y, w)
                solution_path[(x, y - w)] = x, y
                y -= w
                visited.add((x, y))
                stack.append((x, y))

            elif chosen_cell == "right":
                colour_right(x, y, w)
                solution_path[(x + w, y)] = x, y
                x += w
                visited.add((x, y))
                stack.append((x, y))

            elif chosen_cell == "below":
                colour_below(x, y, w)
                solution_path[(x, y + w)] = x, y
                y += w
                visited.add((x, y))
                stack.append((x, y))

            elif chosen_cell == "left":
                colour_left(x, y, w)
                solution_path[(x - w, y)] = x, y
                x -= w
                visited.add((x, y))
                stack.append((x, y))

        # If there are no viable neighbours, backtrack and pop a cell from the stack
        # Flash that cell green to indicate backtracking, then colour blue
        else:
            x, y = stack.pop()
            pygame.draw.rect(window, GREEN, (x + 1, y + 1, w - 2, w - 2), 0)
            pygame.display.update()
            time.sleep(TIMEOUT)
            # re-colour the path
            pygame.draw.rect(window, BLUE, (x + 1, y + 1, w - 2, w - 2), 0)
            pygame.display.update()

def start_game():

    # Infinite loop to keep pygame window open
    running = True
    create_maze = True  # True if first iteration
    print(running,create_maze)
    while running:
        clock.tick(FPS)
        # Check if QUIT event occurs, if so, window closes

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                grid = []
                stack = []
                visited = set()
                solution_path = {}
                running = False

        # If first iteration of while loop:
        # 1) instantiate maze variables
        # 2) create grid
        # 3) generate maze

        if create_maze:

            # Set cell to start generating maze from
            ### starting_x AND starting_y MUST BE A MULTIPLE OF cell_width ###
            dimension = 10
            cell_width = 40
            starting_x = 40
            starting_y = 40
            ending_x = dimension * cell_width  # BOTTOM RIGHT X COORDNIATE
            ending_y = dimension * cell_width  # BOTTOM RIGHT Y COORDINATE

            create_grid(cell_width, dimension)
            pygame.display.update()
            generate_maze(starting_x, starting_y, cell_width)

            # animate solution
            show_solution(starting_x, starting_y, ending_x, ending_y, cell_width)

            create_maze = False  # Indicate maze is done being created


# Initialise pygame window
pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT)) # Pygame surface
pygame.display.set_caption("Maze Generator and Visualizer") # Set title of window

# Create a new font to use
def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
 
    return newText

def main_menu():
 
    menu=True
    selected="start"
 
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        window.fill(PURPLE)
                        pygame.display.update()
                        start_game()
                    if selected=="quit":
                        pygame.quit()
                        quit()
        # Main Menu UI
        window.fill(BLUE)
        title=text_format("Maze Game",font, 90, YELLOW)
        if selected=="start":
            text_start=text_format("START", font, 75, RED)
        else:
            text_start = text_format("START", font, 75, BLACK)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 75, RED)
        else:
            text_quit = text_format("QUIT", font, 75, BLACK)
        
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()

        # Main Menu Text
        window.blit(title, (WIDTH/2 - (title_rect[2]/2), 80))
        window.blit(text_start, (WIDTH/2 - (start_rect[2]/2), 300))
        window.blit(text_quit, (WIDTH/2 - (quit_rect[2]/2), 360))
        pygame.display.update()
        clock.tick(FPS)
        pygame.display.set_caption("Python - Pygame Simple Main Menu Selection")
 


main_menu()









