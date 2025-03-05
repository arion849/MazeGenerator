'''
Generating a maze using the depth first search
algorithm.

1) Choose the starting cell, and we mark is as visited,
   so we don't get back to that one again, and we push the starting cell
   in an empty stack.

2) We set a while statement that runs if the stack is not empty
   we pop that cell from the stack and if that cell has
   neighbors that has not been visited we push that cell into
   the stack and choose one of the unvisited neighbors to visit.

3) We remove the wall(or the edge) form the current cell and the cell
   we chose.

4) Lastly we mark the chosen cell as visited and push it back into the
   stack.

5) Using pygame library we can display the generation of the maze.
'''



import pygame
from random import choice


# Setting up the grid of the maze using pygame
RES  = WIDTH, HEIGHT = 1200, 600
TILE = 60
cols, rows = WIDTH // TILE, HEIGHT // TILE
pygame.init()

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

# We define a Cell class that hold the cell coordinates, the walls of the cells and if it has been visited or not
class Cell:
    def __init__(self,x,y):
         self.x, self.y = x,y
         self.walls = {'top':True, 'left':True, 'right':True, 'bottom':True,}
         self.visited = False



    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(screen, pygame.Color('yellow'), (x + 2, y + 2, TILE - 2, TILE - 2))


    def draw(self):
         x, y = self.x * TILE, self.y * TILE
         if self.visited:
             pygame.draw.rect(screen, pygame.Color("black"),(x,y,TILE,TILE))

         if self.walls['top']:
            pygame.draw.line(screen, pygame.Color("darkorange"), (x, y), (x+TILE, y), 2)
         if self.walls['right']:
            pygame.draw.line(screen, pygame.Color("darkorange"), (x + TILE, y), (x + TILE, y + TILE), 2)
         if self.walls['bottom']:
             pygame.draw.line(screen, pygame.Color("darkorange"), (x, y + TILE), (x + TILE, y + TILE), 2)
         if self.walls['left']:
             pygame.draw.line(screen, pygame.Color("darkorange"), (x, y), (x, y + TILE), 2)


# Checking the cell by its coordinates
    def check_cell(self,x,y):
        find_index = lambda x, y : x + y * cols
        '''
         The cells contain the coordinates(x and y) that can be expressed as a 2D array
         but all the cell instances are going to be in a 1D array so by the above formula we can get the 
         elements of the 1D array by using the coordinates that are in the 2D array.
         
         
         '''
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]


    def check_neighbours(self):
         neighbours = []
         top = self.check_cell(self.x, self.y-1)
         right = self.check_cell(self.x+1 , self.y)
         bottom = self.check_cell(self.x, self.y+1)
         left = self.check_cell(self.x-1, self.y)
         if top and not top.visited:
             neighbours.append(top)
         if right and not right.visited:
             neighbours.append(right)
         if bottom and not bottom.visited:
             neighbours.append(bottom)
         if left and not left.visited:
            neighbours.append(left)
         return choice(neighbours) if neighbours else False


def remove_walls(current, next):
         dx =current.x - next.x
         if dx == 1:
             current.walls['left'] = False
         elif dx == -1:
             current.walls['right'] = False
             next.walls['left'] = False
         dy = current.y - next.y
         if dy == 1:
             current.walls['top'] = False
             next.walls['bottom'] = False
         elif dy == -1:
             current.walls['bottom'] = False
             next.walls['top'] = False


# Creating instances of the class, putting them in an array and creating a stack needed for the dps algorithm.

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []


while True:
    screen.fill(pygame.Color("darkslategrey"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw() for cell in grid_cells]
    current_cell.visited = True
    current_cell.draw_current_cell()

    next_cell = current_cell.check_neighbours()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)  # Push current cell onto the stack
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    pygame.display.flip()
    clock.tick(80)
