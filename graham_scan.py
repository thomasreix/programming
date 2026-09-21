import sys
import pygame
import random
import logging

logger = logging.getLogger(__name__)


def get_next_point(stack, points, next_point):
    past_point = stack[-2]
    last_point = stack[-1]
    next_point %= len(points)

    last_vector = pygame.Vector2(
        points[last_point][0] - points[past_point][0],
        -points[last_point][1] + points[past_point][1],
    )
    next_vector = pygame.Vector2(
        points[next_point][0] - points[last_point][0],
        -points[next_point][1] + points[last_point][1],
    )

    cross_product = last_vector.x * next_vector.y - next_vector.x * last_vector.y
    logging.info(
        f"stack={stack} points={points} last_point={last_point} next_point={next_point} past_point={past_point} current_vector={last_vector} next_vector={next_vector} cross_product={cross_product}"
    )
    if cross_product <= 0:
        stack.pop()
    else:
        stack.append(next_point)
        next_point += 1

    return stack, next_point


def lowest_point(points):
    lowest_point = 0
    for point in points:
        if point[1] > points[lowest_point][1]:
            lowest_point = points.index(point)

    return lowest_point


def display(points, stack, screen, size):
    black = "#0f0f0f"
    orange = "#ef934d"

    for point in points:
        pygame.draw.circle(screen, black, point, size * 2, size)

    a = 0
    for b in stack:
        A = points[a % len(points)]
        B = points[b % len(points)]
        pygame.draw.line(screen, orange, A, B, size)
        a = b


def sort_points(points, lowest):
    sorted_points = []
    slopes = []

    for point in points:
        delta_x = point[0] - points[lowest][0]
        delta_y = point[1] - points[lowest][1]
        slope = delta_x / delta_y if delta_y != 0 else None
        if slope is not None:
            slopes.append((slope, points.index(point)))
    slopes.sort()
    for slope, index in slopes:
        sorted_points.append(points[index])
    sorted_points.insert(0, points[lowest])

    return sorted_points


def random_points(n, width, height):
    points = []
    margin = 50
    for _ in range(n):
        x = random.randint(margin, width - margin)
        y = random.randint(margin, height - margin)
        points.append((x, y))
    return points


def main():
    logging.basicConfig(level=logging.INFO)

    pygame.init()
    logger.info("start")

    width, height = 600, 600
    screen = pygame.display.set_mode((width, height))

    white = "#ffffff"

    number_of_points = 1000
    points = random_points(number_of_points, width, height)
    size = 3

    lowest = lowest_point(points)
    stack = [0, 1]

    sorted_points = sort_points(points, lowest)
    next_point = 2
    finished = False

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for i in range(2, len(stack)):
            if stack[i] == 1:
                finished = True

        if not finished:
            clock.tick(60)

            screen.fill(white)
            display(sorted_points, stack, screen, size)
            stack, next_point = get_next_point(stack, sorted_points, next_point)

            pygame.display.flip()


if __name__ == "__main__":
    main()
