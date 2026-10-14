import sys
from random import randint

import pygame

CELL_SIZE = 50
GRID_WIDTH = 10
GRID_HEIGHT = 20
FPS = 8

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


def generate_grid(width: int, height: int) -> list[list[None]]:
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(None)
        grid.append(row)
    return grid


def placeable(grid, tetromino):
    for x, y in tetromino:
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        if grid[y][x] is not None:
            return False
    return True


def move_active(grid, active, dx=0, dy=0):
    moved = []
    for cell in active:
        x, y = cell
        moved_cell = (x + dx, y + dy)
        moved.append(moved_cell)
    if can_place(grid, moved):
        return moved
    return active


def clear_completed_rows(grid):
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


def tetromino_size(tetromino, axis):
    axis_size = 0
    for cell in tetromino:
        if cell[axis] > axis_size:
            axis_size = cell[axis]
    axis_size += 1
    return axis_size

def spawn_active(grid, index):
    tetromino = TETROMINOS[index]
    width = tetromino_size(tetromino, 0)
    spawn_x = randint(0, (GRID_WIDTH - width))
    active = []
    for cell in tetromino:
        x, y = cell
        active_cell = (x + spawn_x, y)
        active.append(active_cell)
    if not placeable(grid, active):
        return None
    return active


def draw_cell(screen, x, y, color):
    pygame.draw.rect(
        screen,
        color,
        (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
    )
    pygame.draw.rect(
        screen,
        BACKGROUND_COLOR,
        (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        1,
    )


def display_game(screen, grid, active, active_index, preview_index):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = GRID_COLORS[(x + y) % 2]
            draw_cell(screen, x, y, color)
    for y, row in enumerate(grid):
        for x, index in enumerate(row):
            if index is not None:
                color = TETROMINO_COLORS[index]
                draw_cell(screen, x, y, color)
    if active is not None:
        for x, y in active:
            color = TETROMINO_COLORS[active_index]
            draw_cell(screen, x, y, color)

    preview_x = GRID_WIDTH + 1
    for y in range(4):
        for x in range(4):
            color = GRID_COLORS[(x + y) % 2]
            draw_cell(screen, x + preview_x, y, color)
    
    if preview_index is not None:
        tetromino = TETROMINOS[preview_index]
        width = tetromino_size()






















def tetromino_size(tetromino: list[tuple[int, int]]) -> int:
    lenth = 0
    for cell in tetromino:
        if cell[0] > lenth:
            lenth = cell[0]
    height = 0
    for cell in tetromino:
        if cell[1] > height:
            height = cell[1]
    size = (lenth + 1, height + 1)
    return size


def display_grid(
    screen,
    width: int,
    height: int,
    grid_colors: list[str, str],
    grid: list[list[int | None]],
    tetrominos: list[list[tuple[int, int]]],
    tetrominos_colors: list[str],
):
    for y in range(height):
        for x in range(width):
            index = (y + x) % 2
            grid_color = grid_colors[index]
            pygame.draw.rect(
                screen, grid_color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell is not None:
                tetromino_color = tetrominos_colors[cell]
                pygame.draw.rect(
                    screen,
                    tetromino_color,
                    (
                        (x) * CELL_SIZE,
                        (y) * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    ),
                )


def display_preview(
    screen,
    width: int,
    grid_colors: list[str, str],
    tetromino: int,
    tetrominos: list[list[tuple[int, int]]],
    tetrominos_colors: list[str],
):
    for y in range(4):
        for x in range(4):
            index = (y + x) % 2
            grid_color = grid_colors[index]
            pygame.draw.rect(
                screen,
                grid_color,
                ((x + width + 1) * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
            )

    if tetromino_size(tetrominos[tetromino])[0] == 2:
        n = 2
    else:
        n = 1

    tetromino_color = tetrominos_colors[tetromino]
    for cell in tetrominos[tetromino]:
        x, y = cell
        pygame.draw.rect(
            screen,
            tetromino_color,
            ((x + width + n) * CELL_SIZE, (y + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE),
        )


def update_game(
    grid: list[list[int | None]],
    active: tuple[int, int],
    tetrominos: list[list[tuple[int, int]]],
) -> list[list[list[int | None]], tuple[int, int] | None]:
    new_grid = generate_grid(10, 20)
    y = 20
    for row in reversed(grid):
        y -= 1
        for x, cell in enumerate(row):
            if cell is not None:
                height = tetromino_size(tetrominos[cell])[1]
                if height == 1:
                    continue
                if not (y > 20 - height):
                    if grid[y + 1][x] is None:
                        grid[y][x] = None
                        new_grid[y + 1][x] = cell
                    else:
                        new_grid[y][x] = cell
                else:
                    new_grid[y][x] = cell
    if active is not None:
        new_active = []
        for cell in active:
            x, y = cell
            y += 1
            new_cell = (x, y)
            new_active.append(new_cell)
    else:
        new_active = None
    return new_grid, new_active


def add_active(
    grid: list[list[int | None]], tetromino: int, tetrominos: list[tuple[int, int]]
):
    lenth = tetromino_size(tetrominos[tetromino])[0]
    position = randint(0, 10 - lenth)
    active = []
    for cell in tetrominos[tetromino]:
        x, y = cell
        grid[y][position + x] = tetromino
        active_cell = (x + position, y)
        active.append(active_cell)
    return grid, active


def move_active(
    grid: list[list],
    active: tuple[int, int],
    distance: int,
    tetrominos: list[list[tuple[int, int]]],
) -> list[list[list[int | None]], tuple[int, int]]:
    new_grid = grid.copy()
    new_active = []
    broken = False
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if (x, y) in active:
                if grid[y][x + distance] is None or (x + distance, y) in active:
                    new_grid[y][x + distance] = cell
                    new_grid[y][x] = None
                    active_cell = (x + distance, y)
                    new_active.append(active_cell)
                else:
                    broken = True
            else:
                new_grid[y][x] = cell
    if not broken:
        return new_grid, new_active
    else:
        return grid, active

    new_active = []
    for cell in active:
        x, y = cell
        tetromino = grid[y][x]
        grid[y][x + distance] = grid[y][x]
        grid[y][x] = None
        active_cell = (x + distance, y)
        new_active.append(active_cell)
    return grid, new_active


def main():
    pygame.init()

    width, height = 15 * CELL_SIZE, 20 * CELL_SIZE
    screen = pygame.display.set_mode((width, height))

    background_color = "#0F0F0F"

    grid_colors = ["#5F5F5F", "#AFAFAF"]

    tetrominos_colors = [
        "#0FAFFF",
        "#0F0FAF",
        "#ff0f0f",
        "#FF5F0F",
        "#FF0FAF",
        "#FFFF0F",
        "#0FAF0F",
    ]

    grid_width, grid_height = 10, 20
    grid = generate_grid(grid_width, grid_height)

    tetrominos = generate_tetrominos()
    preview = randint(0, 6)
    active = None

    clock = pygame.time.Clock()
    while True:
        clock.tick(5)

        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_q]:
                pygame.quit()
                sys.exit()
        if active is not None:
            if keys[pygame.K_RIGHT]:
                grid, active = move_active(grid, active, 1, tetrominos)
            elif keys[pygame.K_LEFT]:
                grid, active = move_active(grid, active, -1, tetrominos)

        new_grid, active = update_game(grid, active, tetrominos)

        if grid == new_grid:
            grid = new_grid
            grid, active = add_active(grid, preview, tetrominos)
            preview = randint(0, 6)
        else:
            grid = new_grid

        screen.fill(background_color)
        display_grid(
            screen,
            grid_width,
            grid_height,
            grid_colors,
            grid,
            tetrominos,
            tetrominos_colors,
        )
        display_preview(
            screen,
            grid_width,
            grid_colors,
            preview,
            tetrominos,
            tetrominos_colors,
        )

        pygame.display.flip()
        print(active)


if __name__ == "__main__":
    main()
