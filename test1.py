import pygame
from random import choice
from collections import deque

# Setting up the grid of the maze using pygame
RES = WIDTH, HEIGHT = 1200, 600
TILE = 60
cols, rows = WIDTH // TILE, HEIGHT // TILE
pygame.init()

screen = pygame.display.set_mode(RES)
clock = pygame.time.Clock()

class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'left': True, 'right': True, 'bottom': True}
        self.visited = False
        self.parent = None

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(screen, pygame.Color("white"), (x, y, TILE, TILE))
        if self.walls['top']:
            pygame.draw.line(screen, pygame.Color("darkorange"), (x, y), (x + TILE, y), 2)
        if self.walls['right']:
            pygame.draw.line(screen, pygame.Color("darkorange"), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls['bottom']:
            pygame.draw.line(screen, pygame.Color("darkorange"), (x, y + TILE), (x + TILE, y + TILE), 2)
        if self.walls['left']:
            pygame.draw.line(screen, pygame.Color("darkorange"), (x, y), (x, y + TILE), 2)

    def check_cell(self, x, y):
        if x < 0 or x >= cols or y < 0 or y >= rows:
            return None
        index = x + y * cols
        return grid_cells[index] if not grid_cells[index].visited else None

    def check_neighbours(self):
        neighbours = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top:
            neighbours.append(top)
        if right:
            neighbours.append(right)
        if bottom:
            neighbours.append(bottom)
        if left:
            neighbours.append(left)
        return choice(neighbours) if neighbours else None

def remove_walls(a, b):
    dx = a.x - b.x
    dy = a.y - b.y
    if dx == 1:
        a.walls['left'] = False
        b.walls['right'] = False
    elif dx == -1:
        a.walls['right'] = False
        b.walls['left'] = False
    if dy == 1:
        a.walls['top'] = False
        b.walls['bottom'] = False
    elif dy == -1:
        a.walls['bottom'] = False
        b.walls['top'] = False

grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current = grid_cells[0]
stack = []

def bfs_solve(start_cell):
    queue = deque([start_cell])
    path = []
    start_cell.visited = True
    while queue:
        current = queue.popleft()
        if current.x == cols - 1 and current.y == rows - 1:
            while current:
                path.append(current)
                current = current.parent
            return path
        for neighbor in [current.check_cell(current.x, current.y - 1), current.check_cell(current.x + 1, current.y),
                         current.check_cell(current.x, current.y + 1), current.check_cell(current.x - 1, current.y)]:
            if neighbor and not neighbor.visited and not current.walls['top'] if neighbor == current.check_cell(current.x, current.y - 1) else current.walls['right'] if neighbor == current.check_cell(current.x + 1, current.y) else current.walls['bottom'] if neighbor == current.check_cell(current.x, current.y + 1) else current.walls['left']:
                neighbor.visited = True
                neighbor.parent = current
                queue.append(neighbor)
    return path

while True:
    screen.fill(pygame.Color("darkslategrey"))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    if stack or not current.visited:
        current.visited = True
        next_cell = current.check_neighbours()
        if next_cell:
            next_cell.visited = True
            stack.append(current)
            remove_walls(current, next_cell)
            current = next_cell
        elif stack:
            current = stack.pop()
    else:
        solution_path = bfs_solve(grid_cells[0])
        for cell in solution_path:
            x, y = cell.x * TILE, cell.y * TILE
            pygame.draw.rect(screen, pygame.Color('green'), (x + 2, y + 2, TILE - 2, TILE - 2))

    for cell in grid_cells:
        cell.draw()

    pygame.display.flip()
    clock.tick(30)
