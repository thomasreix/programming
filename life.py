import sys
from random import random

import pygame

CELL_SIZE = 10


def random_grid(width: int, height: int) -> list[list]:
    grid = []
    for x in range(height):
        row = []
        for y in range(width):
            cell = round(random())
            row.append(cell)
        grid.append(row)
    return grid


def display_grid(screen, grid: list[list], color: str):
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == 1:
                pygame.draw.rect(
                    screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )


def count_neigbors(grid: list[list], x: int, y: int):
    neighbors = 0
    for i in [-1, 0, 1]:
        row = (y + i) % len(grid)
        for j in [-1, 0, 1]:
            col = (x + j) % len(grid[0])
            if j == 0 and i == 0:
                continue
            cell = grid[row][col]
            neighbors += cell
    return neighbors


def update_grid(grid: list[list]) -> list[list]:
    new_grid = []
    for y, row in enumerate(grid):
        new_row = []
        for x, cell in enumerate(row):
            neighbors = count_neigbors(grid, x, y)
            new_cell = 0
            if (cell == 1 and neighbors in [2, 3]) or (cell == 0 and neighbors == 3):
                new_cell = 1
            new_row.append(new_cell)
        new_grid.append(new_row)
    return new_grid


def main():
    pygame.init()
    width, height = 960, 540
    screen = pygame.display.set_mode((width, height))

    black = "#0f0f0f"
    white = "#ffffff"
    _orange = "#ef934d"

    grid = random_grid(width // CELL_SIZE, height // CELL_SIZE)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(black)
        grid = update_grid(grid)
        display_grid(screen, grid, white)
        pygame.display.flip()


if __name__ == "__main__":
    main()
