import sys

import pygame


BOARD_SIZE = 6
HORIZONTAL_CAR = 0
VERTICAL_CAR = 1


def levels(n):
    levels = [
        [(0, 2, 0), (4, 2, 1)],
        [(1, 2, 0), (4, 2, 1), (3, 1, 0), (2, 0, 1), (4, 4, 1)],
    ]

    if n > len(levels) or n < 1:
        print("wrong level selected")
        return []

    print(f"level {n} selected")
    return levels[n - 1]


def draw_board(screen, screen_size, even_color, odd_color):
    cell_size = screen_size / BOARD_SIZE

    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            x = col * cell_size
            y = row * cell_size

            if (row + col) % 2 == 0:
                color = even_color
            else:
                color = odd_color

            pygame.draw.rect(
                screen,
                color,
                (x, y, cell_size, cell_size),
            )


def draw_cars(screen, screen_size, cars, colors):
    cell_size = screen_size / BOARD_SIZE

    for index, car in enumerate(cars):
        color = colors[index % len(colors)]
        car_x, car_y, car_type = car

        x = car_x * cell_size
        y = car_y * cell_size

        # Horizontal car by default.
        w = cell_size * 2
        h = cell_size

        if car_type == VERTICAL_CAR:
            w = cell_size
            h = cell_size * 2

        pygame.draw.rect(screen, color, (x, y, w, h))


def car_cells(car) -> list[tuple[int, int]]:
    car_x, car_y, car_type = car

    if car_type == HORIZONTAL_CAR:
        return [
            (car_x, car_y),
            (car_x + 1, car_y),
        ]

    return [
        (car_x, car_y),
        (car_x, car_y + 1),
    ]


def clicked_car(cars, mouse_position, screen_size):
    cell_size = screen_size / BOARD_SIZE
    x = int(mouse_position[0] // cell_size)
    y = int(mouse_position[1] // cell_size)

    for index, car in enumerate(cars):
        if (x, y) in car_cells(car):
            return index

    return None


def occupied(cars, cell, ignored_car_index=None):
    x, y = cell

    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        return True

    for index, car in enumerate(cars):
        if index == ignored_car_index:
            continue

        if cell in car_cells(car):
            return True

    return False


def move_car(cars, mouse_position, mouse_button, screen_size):
    clicked_car_index = clicked_car(cars, mouse_position, screen_size)

    if clicked_car_index is None:
        return cars

    x, y, car_type = cars[clicked_car_index]

    if mouse_button == 1:
        if car_type == HORIZONTAL_CAR:
            moved_car = (x - 1, y, car_type)
        else:
            moved_car = (x, y - 1, car_type)

    elif mouse_button == 3:
        if car_type == HORIZONTAL_CAR:
            moved_car = (x + 1, y, car_type)
        else:
            moved_car = (x, y + 1, car_type)

    else:
        return cars

    for moved_cell in car_cells(moved_car):
        if occupied(cars, moved_cell, clicked_car_index):
            return cars

    cars[clicked_car_index] = moved_car
    return cars


def add_car(cars, mouse_position, mouse_button, screen_size):
    cell_size = screen_size / BOARD_SIZE
    car_x = int(mouse_position[0] // cell_size)
    car_y = int(mouse_position[1] // cell_size)

    if mouse_button == 1:
        car_type = HORIZONTAL_CAR
    elif mouse_button == 3:
        car_type = VERTICAL_CAR

    added_car = (car_x, car_y, car_type)

    for added_cell in car_cells(added_car):
        if occupied(cars, added_cell):
            return cars

    cars.append(added_car)
    return cars


def remove_car(cars, mouse_position, mouse_button, screen_size):
    if mouse_button != 2:
        return cars

    car_index = clicked_car(cars, mouse_position, screen_size)

    if car_index is not None:
        cars.pop(car_index)

    return cars


def main():
    pygame.init()

    screen_size = 600
    screen = pygame.display.set_mode((screen_size, screen_size))

    gray = "#5f5f5f"
    silver = "#afafaf"

    colors = [
        "#ff0f0f",  # red
        "#0faf0f",  # green
        "#5f5f0f",  # clay
        "#0f0fff",  # blue
        "#af0faf",  # magenta
        "#0f5f5f",  # turquoise
        "#5f0f0f",  # maroon
        "#0fff0f",  # neon
        "#afaf0f",  # sand
        "#0f0faf",  # aqua
        "#5f0f5f",  # violet
        "#0fffff",  # diamond
        "#af0f0f",  # wine
        "#0f5f0f",  # moss
        "#ffff0f",  # yellow
        "#0f0f5f",  # lapis
        "#ff0fff",  # pink
        "#0fafaf",  # sky
    ]

    mode = "play"  # play or edit

    cars = levels(1)

    level_keys = [
        pygame.K_1,
        pygame.K_2,
        pygame.K_3,
        pygame.K_4,
        pygame.K_5,
        pygame.K_6,
        pygame.K_7,
        pygame.K_8,
        pygame.K_9,
        pygame.K_0,
    ]

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mode == "play":
                    cars = move_car(
                        cars,
                        event.pos,
                        event.button,
                        screen_size,
                    )
                elif mode == "edit":
                    if event.button == 2:
                        cars = remove_car(
                            cars,
                            event.pos,
                            event.button,
                            screen_size,
                        )
                    else:
                        cars = add_car(
                            cars,
                            event.pos,
                            event.button,
                            screen_size,
                        )

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if mode == "play":
                        mode = "edit"
                    else:
                        mode = "play"

                elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    print(cars)

                elif event.key in level_keys:
                    for key_index, level_key in enumerate(level_keys):
                        if event.key == level_key:
                            n = key_index + 1
                            cars = levels(n)

        draw_board(screen, screen_size, gray, silver)
        draw_cars(screen, screen_size, cars, colors)

        pygame.display.flip()


if __name__ == "__main__":
    main()
