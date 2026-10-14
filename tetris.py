import sys
from random import randint

import pygame

CELL_SIZE = 50


def generate_tetrominos() -> list[list[tuple[int, int]]]:
    cells = []
    for x in range(4):
        for y in range(2):
            cell = (x, y)
            cells.append(cell)

    permutations = []
    for i in [0, 1, 2, 3, 5, 6]:
        for j in [0, 1, 2, 3, 5, 6]:
            for k in [0, 1, 2, 3, 5, 6]:
                for l in [0, 1, 2, 3, 5, 6]:
                    if i < j < k < l:
                        permutation = [i, j, k, l]
                        permutations.append(permutation)

    tetrominos = []
    for permutation in permutations:
        tetromino = []
        for p in permutation:
            x = p % 4
            y = 0 if p < 4 else 1
            cell = (x, y)
            tetromino.append(cell)

        neighbors = 0
        total_neighbors = 0
        for cell in tetromino:
            cell_neighbors = 0
            for neighbor in tetromino:
                if (
                    cell[0] + 1 == neighbor[0]
                    and cell[1] == neighbor[1]
                    or cell[1] + 1 == neighbor[1]
                    and cell[0] == neighbor[0]
                    or cell[0] - 1 == neighbor[0]
                    and cell[1] == neighbor[1]
                    or cell[1] - 1 == neighbor[1]
                    and cell[0] == neighbor[0]
                ):
                    cell_neighbors += 1
                    total_neighbors += 1
            if cell_neighbors > 0:
                neighbors += 1
        if neighbors == 4 and total_neighbors > 5:
            tetrominos.append(tetromino)
    tetrominos.pop(1)
    shifted_tetrominos = []
    for tetromino in tetrominos:
        if tetromino[0] != (0, 0):
            shifted_tetromino = []
            for cell in tetromino:
                cell_x, cell_y = cell
                shifted_cell = (cell_x - 1, cell_y)
                shifted_tetromino.append(shifted_cell)
            shifted_tetrominos.append(shifted_tetromino)
        else:
            shifted_tetrominos.append(tetromino)
    return shifted_tetrominos


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


def generate_grid(width: int, height: int) -> list[list[None]]:
    grid = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append(None)
        grid.append(row)
    return grid


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
    grid: list[list[int | None]], active: tuple[int, int], tetrominos: list[list[tuple[int, int]]]
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
                if not(y > 20 - height):
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
    tetrominos: list[list[tuple[int, int]]]
) -> list[list[list[int | None]], tuple[int, int]]:

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
