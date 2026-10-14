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

# Each piece is represented by four (x, y) cells.
TETROMINOS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # I
    [(0, 0), (0, 1), (1, 1), (2, 1)],  # J
    [(2, 0), (0, 1), (1, 1), (2, 1)],  # L
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # O
    [(1, 0), (2, 0), (0, 1), (1, 1)],  # S
    [(1, 0), (0, 1), (1, 1), (2, 1)],  # T
    [(0, 0), (1, 0), (1, 1), (2, 1)],  # Z
]


def generate_grid(width: int, height: int) -> list[list[int | None]]:
    return [[None for _ in range(width)] for _ in range(height)]


def can_place(grid, cells):
    """Return whether all cells fit inside the board and avoid settled blocks."""
    for x, y in cells:
        if x < 0 or x >= GRID_WIDTH or y < 0 or y >= GRID_HEIGHT:
            return False
        if grid[y][x] is not None:
            return False
    return True


def move_piece(grid, active, dx=0, dy=0):
    """Move the active piece if the destination is valid."""
    moved = [(x + dx, y + dy) for x, y in active]
    if can_place(grid, moved):
        return moved, True
    return active, False


def clear_full_rows(grid):
    """Remove complete rows and add empty rows at the top."""
    remaining = [row for row in grid if any(cell is None for cell in row)]
    cleared = GRID_HEIGHT - len(remaining)
    return [[None] * GRID_WIDTH for _ in range(cleared)] + remaining


def spawn_piece(grid, piece_index):
    shape = TETROMINOS[piece_index]
    piece_width = max(x for x, _ in shape) + 1
    start_x = (GRID_WIDTH - piece_width) // 2
    active = [(x + start_x, y) for x, y in shape]
    if not can_place(grid, active):
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


def display_grid(screen, grid, active, active_index, preview_index):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            draw_cell(screen, x, y, GRID_COLORS[(x + y) % 2])

    for y, row in enumerate(grid):
        for x, piece_index in enumerate(row):
            if piece_index is not None:
                draw_cell(screen, x, y, TETROMINO_COLORS[piece_index])

    if active is not None:
        for x, y in active:
            draw_cell(screen, x, y, TETROMINO_COLORS[active_index])

    # Preview area to the right of the board.
    preview_x = GRID_WIDTH + 1
    for y in range(4):
        for x in range(4):
            draw_cell(
                screen,
                preview_x + x,
                y,
                GRID_COLORS[(x + y) % 2],
            )

    if preview_index is not None:
        shape = TETROMINOS[preview_index]
        shape_width = max(x for x, _ in shape) + 1
        shape_height = max(y for _, y in shape) + 1
        offset_x = preview_x + (4 - shape_width) // 2
        offset_y = (4 - shape_height) // 2
        for x, y in shape:
            draw_cell(
                screen,
                offset_x + x,
                offset_y + y,
                TETROMINO_COLORS[preview_index],
            )


def main():
    pygame.init()
    screen = pygame.display.set_mode(
        ((GRID_WIDTH + 5) * CELL_SIZE, GRID_HEIGHT * CELL_SIZE)
    )
    pygame.display.set_caption("Tetromino")
    clock = pygame.time.Clock()

    grid = generate_grid(GRID_WIDTH, GRID_HEIGHT)
    active_index = randint(0, len(TETROMINOS) - 1)
    preview_index = randint(0, len(TETROMINOS) - 1)
    active = spawn_piece(grid, active_index)
    game_over = active is None
    fall_timer = 0

    while True:
        dt = clock.tick(FPS)
        fall_timer += dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                # Down moves once per key press. Horizontal movement is handled
                # below by polling held keys, so it can happen only once per frame.
                if event.key == pygame.K_DOWN and active is not None:
                    active, moved = move_piece(grid, active, dy=1)
                    if not moved:
                        fall_timer = 1000

        keys = pygame.key.get_pressed()
        if not game_over and active is not None:
            if keys[pygame.K_LEFT]:
                active, _ = move_piece(grid, active, dx=-1)
            elif keys[pygame.K_RIGHT]:
                active, _ = move_piece(grid, active, dx=1)

        if not game_over and active is not None and fall_timer >= 1000:
            fall_timer = 0
            active, moved = move_piece(grid, active, dy=1)

            if not moved:
                # Lock the piece into the settled grid.
                for x, y in active:
                    grid[y][x] = active_index

                grid = clear_full_rows(grid)
                active_index = preview_index
                preview_index = randint(0, len(TETROMINOS) - 1)
                active = spawn_piece(grid, active_index)
                if active is None:
                    game_over = True

        display_grid(screen, grid, active, active_index, preview_index)

        if game_over:
            font = pygame.font.Font(None, 48)
            message = font.render("GAME OVER", True, "white")
            screen.blit(
                message,
                message.get_rect(
                    center=(GRID_WIDTH * CELL_SIZE // 2, GRID_HEIGHT * CELL_SIZE // 2),
                ),
            )

        pygame.display.flip()


if __name__ == "__main__":
    main()
