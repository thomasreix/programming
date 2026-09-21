import sys
import pygame


def menger_carpet(screen_size, algorithm, iteration):
    square_vertices = [
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
    ]

    square_faces = [
        [0, 1, 2],
        [0, 2, 3],
    ]

    def next_iteration(original_square):
        squares = []
        for x in range(3):
            for y in range(3):
                if not (x == 1 and y == 1):
                    square = (x + original_square[0] * 3, y + original_square[1] * 3)
                    squares.append(square)
        return squares

    menger_squares = [(0, 0)]

    for _ in range(iteration):
        new_squares = []
        for square in menger_squares:
            new_squares.extend(next_iteration(square))
        menger_squares = new_squares

    menger_faces = []
    margin = 30
    menger_size = screen_size - 2 * margin
    square_size = menger_size / (3**iteration)

    if algorithm:
        # --- Merge adjacent squares into larger rectangles ---
        square_set = set(menger_squares)
        visited = set()
        rectangles = []  # each: (x, y, w, h) in grid units

        for sx, sy in sorted(menger_squares):
            if (sx, sy) in visited:
                continue

            # Grow width (horizontal run)
            w = 1
            while (sx + w, sy) in square_set and (sx + w, sy) not in visited:
                w += 1

            # Grow height (as long as the full width strip exists)
            h = 1
            grow = True
            while grow:
                for dx in range(w):
                    if (sx + dx, sy + h) not in square_set or (
                        sx + dx,
                        sy + h,
                    ) in visited:
                        grow = False
                        break
                if grow:
                    h += 1

            for dx in range(w):
                for dy in range(h):
                    visited.add((sx + dx, sy + dy))

            rectangles.append((sx, sy, w, h))

        # Each rectangle → 2 triangles
        for rx, ry, rw, rh in rectangles:
            x0 = rx * square_size + margin
            y0 = ry * square_size + margin
            x1 = (rx + rw) * square_size + margin
            y1 = (ry + rh) * square_size + margin

            # Triangle 1: bottom-left, bottom-right, top-right
            menger_faces.append([(x0, y0), (x1, y0), (x1, y1)])
            # Triangle 2: bottom-left, top-right, top-left
            menger_faces.append([(x0, y0), (x1, y1), (x0, y1)])

    else:
        for square in menger_squares:
            for face in square_faces:
                vertex_1 = (
                    (square[0] + square_vertices[face[0]][0]) * square_size + margin,
                    (square[1] + square_vertices[face[0]][1]) * square_size + margin,
                )
                vertex_2 = (
                    (square[0] + square_vertices[face[1]][0]) * square_size + margin,
                    (square[1] + square_vertices[face[1]][1]) * square_size + margin,
                )
                vertex_3 = (
                    (square[0] + square_vertices[face[2]][0]) * square_size + margin,
                    (square[1] + square_vertices[face[2]][1]) * square_size + margin,
                )
                menger_faces.append([vertex_1, vertex_2, vertex_3])

    return menger_faces


def main():
    pygame.init()

    screen_size = 600
    screen = pygame.display.set_mode((screen_size, screen_size))

    faces = menger_carpet(screen_size, True, 2)

    black = pygame.Color("#0f0f0f")
    blue = pygame.Color("#0fafff")
    lapis = pygame.Color("#0f0faf")

    colors = [blue, lapis]

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(black)

        color = 0
        for face in faces:
            color += 1
            pygame.draw.polygon(screen, colors[color % 2], [face[0], face[1], face[2]])

        pygame.display.flip()


if __name__ == "__main__":
    main()
