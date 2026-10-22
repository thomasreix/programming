import sys
from random import randint

import pygame

from tetromino import generate_tetrominos

CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 9
SPEED = 1

BACKGROUND_COLOR = "#0F0F0F"
GRID_COLORS = ["#5F5F5F", "#AFAFAF"]
TETROMINO_COLORS = [
    "#0FAFFF",
    "#0F0FAF",
    "#FF0F0F",
    "#FF5F0F",
    "#FF0FAF",
    "#FFFF0F",
    "#0FAF0F",
]

TETROMINOS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
    [(0, 0), (0, 1), (1, 1), (2, 1)],  # J
    [(2, 0), (0, 1), (1, 1), (2, 1)],  # L
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # O
    [(1, 0), (2, 0), (0, 1), (1, 1)],  # S
    [(1, 0), (0, 1), (1, 1), (2, 1)],  # T
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z
]

TETROMINO_COLORS = generate_tetrominos(4)


def generate_grid(width: int, height: int) -> list[list[None]]:
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(None)
        grid.append(row)
    return grid


def placeable(grid: list[list[int | None]], tetromino: list[tuple[int, int]]) -> bool:
    for x, y in tetromino:
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        if grid[y][x] is not None:
            return False
    return True


def move(
    grid: list[list[int | None]], tetromino: list[tuple[int, int]], dx=0, dy=0
) -> list[tuple[int, int]]:
    moved = []
    for x, y in tetromino:
        moved_cell = (x + dx, y + dy)
        moved.append(moved_cell)
    if placeable(grid, moved):
        return moved
    return tetromino


def clear_completed_rows(grid: list[list[int | None]]) -> list[list[int | None]]:
    completed_rows = []
    for y, row in enumerate(grid):
        completed = True
        for cell in row:
            if cell is None:
                completed = False
        if completed:
            completed_rows.append(y)
    for row in completed_rows:
        grid.pop(row)
        cleared_row = []
        for cell in range(GRID_WIDTH):
            cleared_row.append(None)
        grid.insert(0, cleared_row)
    return grid


def tetromino_size(tetromino: list[tuple[int, int]]) -> tuple[int, int]:
    axises = []
    for axis in range(2):
        axis_size = 0
        for cell in tetromino:
            axis_size = max(axis_size, cell[axis])
        axis_size += 1
        axises.append(axis_size)
    size = (axises[0], axises[1])
    return size


def random() -> int:
    return randint(0, len(TETROMINOS) - 1)


def spawn_active(grid: list[list[int | None]], index: int) -> list[tuple[int, int]]:
    tetromino = TETROMINOS[index]
    width = tetromino_size(tetromino)[0]
    spawn_x = randint(0, (GRID_WIDTH - width))
    active = []
    for cell in tetromino:
        x, y = cell
        active_cell = (x + spawn_x, y)
        active.append(active_cell)
    if not placeable(grid, active):
        return None
    return active


def draw_cell(screen, x: int, y: int, color: str):
    pygame.draw.rect(
        screen,
        color,
        (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
    )


def draw_grid(screen, offset_x, width, height):
    for y in range(height):
        for x in range(width):
            color = GRID_COLORS[(x + y) % 2]
            draw_cell(screen, x + offset_x, y, color)


def display_preview(screen, preview_index):
    preview_x = GRID_WIDTH + 1
    draw_grid(screen, preview_x, 4, 4)

    tetromino = TETROMINOS[preview_index]
    width, height = tetromino_size(tetromino)
    offset_x = preview_x + (4 - width) // 2
    offset_y = (4 - height) // 2
    for x, y in tetromino:
        color = TETROMINO_COLORS[preview_index]
        draw_cell(screen, x + offset_x, y + offset_y, color)


def display_game(
    screen,
    grid: list[list[int | None]],
    active: list[tuple[int, int]],
    active_index: int,
):
    draw_grid(screen, 0, GRID_WIDTH, GRID_HEIGHT)
    for y, row in enumerate(grid):
        for x, index in enumerate(row):
            if index is not None:
                color = TETROMINO_COLORS[index]
                draw_cell(screen, x, y, color)
    for x, y in active:
        color = TETROMINO_COLORS[active_index]
        draw_cell(screen, x, y, color)


def main() -> int:
    pygame.init()
    screen_width = (GRID_WIDTH + 5) * CELL_SIZE
    screen_height = GRID_HEIGHT * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    grid = generate_grid(GRID_WIDTH, GRID_HEIGHT)
    active_index = random()
    preview_index = random()
    active = spawn_active(grid, active_index)
    game_over = False
    tick = 0
    while True:
        screen.fill(BACKGROUND_COLOR)
        dt = clock.tick(60)
        tick += dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_LEFT:
                    active = move(grid, active, dx=-1)
                if event.key == pygame.K_RIGHT:
                    active = move(grid, active, dx=1)
                if event.key == pygame.K_DOWN:
                    active = move(grid, active, dy=1)
                if event.key == pygame.K_UP:
                    for row in range(GRID_HEIGHT):
                        active = move(grid, active, dy=1)

                if event.key == pygame.K_KP_0:
                    print("you can not rotate")
                if event.key == pygame.K_KP_ENTER:
                    print("you can not rotate")

        if active is not None:
            display_game(screen, grid, active, active_index)
            display_preview(screen, preview_index)

            if tick >= 1000 / SPEED:
                tick = 0
                previous_active = active
                active = move(grid, active, dy=1)
                if previous_active == active:
                    for x, y in active:
                        grid[y][x] = active_index
                    grid = clear_completed_rows(grid)
                    active_index = preview_index
                    preview_index = random()
                    active = spawn_active(grid, active_index)
                    if active is None:
                        game_over = True

        if game_over:
            grid = generate_grid(GRID_WIDTH, GRID_HEIGHT)
            active_index = random()
            preview_index = random()
            active = spawn_active(grid, active_index)
            game_over = False
            tick = 0

        pygame.display.flip()


if __name__ == "__main__":
    main()
