from enum import Enum
import time
import pygame
import sys
import copy
import random  


CELL_SIZE = 20
CELL_SEPARATION = 1
GRID_LINE_COLOR = (50, 50, 50)
ALIVE_COLOR = (255, 255, 255)
DEAD_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (30, 30, 30)
FPS = 10
simulation_active = True

class CellState(Enum):
    ALIVE = 1
    DEAD = 0

class Cell:
    def __init__(self, state=CellState.DEAD, row=None, col=None):
        self.state = state
        self.row = row
        self.col = col
        self.rect = None

    def __str__(self):
        return '⬛' if self.state == CellState.ALIVE else '⬜'

    def count_neighbors(self, grid):
        directions = [(-1,-1), (-1,0), (-1,1),
                      (0,-1),           (0,1),
                      (1,-1),  (1,0),  (1,1)]
        livecount = 0
        height = len(grid)
        width = len(grid[0])
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < height and 0 <= c < width:
                if grid[r][c].state == CellState.ALIVE:
                    livecount += 1
        return livecount

    def apply_conway_rules(self, grid):
        neighbors = self.count_neighbors(grid)
        if self.state == CellState.ALIVE:
            if neighbors < 2 or neighbors > 3:
                return CellState.DEAD
            else:
                return CellState.ALIVE
        elif self.state == CellState.DEAD:
            if neighbors == 3:
                return CellState.ALIVE
            else:
                return CellState.DEAD

def evolve_grid(grid):
    height = len(grid)
    width = len(grid[0])
    next_grid = copy.deepcopy(grid)

    for r in range(height):
        for c in range(width):
            current_cell = grid[r][c]
            next_state = current_cell.apply_conway_rules(grid)
            next_grid[r][c].state = next_state

    return next_grid

def print_grid(grid):
    for row in grid:
        print("".join(str(cell) for cell in row))
    print()

def setup_pygame_display(width, height):
    print("Attempting to initialize Pygame...")
    pygame.init()
    screen_width = width * (CELL_SIZE + CELL_SEPARATION) - CELL_SEPARATION
    screen_height = height * (CELL_SIZE + CELL_SEPARATION) - CELL_SEPARATION
    try:
        screen = pygame.display.set_mode((screen_width, screen_height))
    except pygame.error as e:
        print(f"Error: {e}")
        return None
    pygame.display.set_caption("Conway's Game of Life")
    return screen

def create_initial_grid_with_rects(grid_width, grid_height):
    grid = []
    for r in range(grid_height):
        row_cells = []
        for c in range(grid_width):
            cell = Cell(CellState.DEAD, r, c)
            left = c * (CELL_SIZE + CELL_SEPARATION)
            top = r * (CELL_SIZE + CELL_SEPARATION)
            cell.rect = pygame.Rect(left, top, CELL_SIZE, CELL_SIZE)
            row_cells.append(cell)
        grid.append(row_cells)
    return grid

def draw_grid(screen, grid):
    for row in grid:
        for cell in row:
            color = ALIVE_COLOR if cell.state == CellState.ALIVE else DEAD_COLOR
            pygame.draw.rect(screen, color, cell.rect)

if __name__ == "__main__":
    grid_width = 40
    grid_height = 30

    screen = setup_pygame_display(grid_width, grid_height)
    if screen is None:
        pygame.quit()
        sys.exit(1)

    grid = create_initial_grid_with_rects(grid_width, grid_height)
    clock = pygame.time.Clock()

    # Glider pattern
    grid[1][3].state = CellState.ALIVE
    grid[2][1].state = CellState.ALIVE
    grid[2][3].state = CellState.ALIVE
    grid[3][2].state = CellState.ALIVE
    grid[3][3].state = CellState.ALIVE

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    simulation_active = not simulation_active
                    print(f"Simulation Active: {simulation_active}")
                elif event.key == pygame.K_BACKSPACE:
                    for row in grid:
                        for cell in row:
                            cell.state = CellState.DEAD
                elif event.key == pygame.K_r:
                    for row in grid:
                        for cell in row:
                            cell.state = CellState.ALIVE if random.random() < 0.2 else CellState.DEAD

            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for row in grid:
                    for cell in row:
                        if cell.rect.collidepoint(pos):
                            cell.state = CellState.DEAD if cell.state == CellState.ALIVE else CellState.ALIVE
                            break

        if simulation_active:
            grid = evolve_grid(grid)

        screen.fill(BACKGROUND_COLOR)
        draw_grid(screen, grid)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
