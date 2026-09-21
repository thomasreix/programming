import sys
import pygame

CELL_SIZE = 5
RULE = 30
NEIGHBORHOOD = [[-1, -1], [0, -1], [1, -1]]


def create_grid(cols, rows, value=0):
    return [[value for _ in range(rows)] for _ in range(cols)]


def get_cell(grid, col, row, cols, rows):
    if 0 <= col < cols and 0 <= row < rows:
        return grid[col][row]
    return 0


def step_row(grid, cols, rows, row, rule, neighborhood):
    rule_bits = [int(b) for b in format(rule, "08b")]

    for col in range(cols):
        states = []
        for offset in neighborhood:
            neighbor_col = col + offset[0]
            neighbor_row = row + offset[1]
            states.append(get_cell(grid, neighbor_col, neighbor_row, cols, rows))

        pattern = (states[0] << 2) | (states[1] << 1) | states[2]

        if 0 <= col < cols and 0 <= row < rows:
            grid[col][row] = rule_bits[7 - pattern]


def draw_world(
    screen,
    grid,
    view_start,
    visible_cols,
    visible_rows,
    cell_size,
    x_offset,
    alive_color,
    dead_color,
):
    for screen_col in range(visible_cols):
        world_col = view_start + screen_col
        for screen_row in range(visible_rows):
            color = alive_color if grid[world_col][screen_row] == 1 else dead_color
            pygame.draw.rect(
                screen,
                color,
                (
                    x_offset + screen_col * cell_size,
                    screen_row * cell_size,
                    cell_size,
                    cell_size,
                ),
            )


def draw_menu(screen, menu_width, menu_height, line_color, bg_color):
    spacing = 50
    grid_count = 3
    tile_size = (menu_width - spacing * 2) // grid_count
    pygame.draw.rect(screen, bg_color, (0, 0, menu_width, menu_height))
    for i in range(4):
        pygame.draw.line(
            screen,
            line_color,
            (spacing, spacing + i * tile_size),
            (menu_width - spacing, spacing + i * tile_size),
            6,
        )
        pygame.draw.line(
            screen,
            line_color,
            (spacing + i * tile_size, spacing),
            (spacing + i * tile_size, menu_width - spacing),
            6,
        )


def main():
    pygame.init()

    menu_width = 280
    world_pixel_size = 540
    screen_width = world_pixel_size + menu_width
    screen_height = world_pixel_size
    pygame.display.set_caption("life")
    screen = pygame.display.set_mode((screen_width, screen_height))

    black = "#0f0f0f"
    white = "#ffffff"
    orange = "#ef934d"

    visible_cols = world_pixel_size // CELL_SIZE
    visible_rows = screen_height // CELL_SIZE

    padding_cols = visible_rows * 2
    world_cols = visible_cols + padding_cols * 2
    world_rows = visible_rows
    view_start = padding_cols
    seed_col = view_start + visible_cols // 2

    grid = create_grid(world_cols, world_rows)
    grid[seed_col][0] = 1  # seed at top
    current_row = 1  # start from second row

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if current_row < world_rows:
            step_row(grid, world_cols, world_rows, current_row, RULE, NEIGHBORHOOD)
            current_row += 1  # go downward

        screen.fill(black)
        draw_world(
            screen,
            grid,
            view_start,
            visible_cols,
            visible_rows,
            CELL_SIZE,
            menu_width + 5,
            white,
            black,
        )
        draw_menu(screen, menu_width, screen_height, orange, black)
        pygame.draw.line(
            screen, orange, (menu_width + 5, 0), (menu_width + 5, screen_height), 6
        )
        pygame.display.flip()


if __name__ == "__main__":
    main()
