from itertools import combinations


def normalize(tetromino):
    min_x = min(x for x, y in tetromino)
    min_y = min(y for x, y in tetromino)

    normalized = []
    for x, y in tetromino:
        normalized.append((x - min_x, y - min_y))

    return tuple(sorted(normalized))


def rotate(tetromino):
    rotated = []
    for x, y in tetromino:
        rotated.append((y, -x))

    return normalize(rotated)


def rotation_key(tetromino):
    rotations = []
    rotated = normalize(tetromino)

    for _ in range(4):
        rotations.append(rotated)
        rotated = rotate(rotated)

    return min(rotations)


def generate_tetrominos(size=4):
    cells = []
    for x in range(size):
        for y in range(size):
            cells.append((x, y))

    if size % 2:
        center = [(size // 2, size // 2)]
    else:
        middle = size // 2
        center = [(middle - 1, middle - 1)]

    groups = {}
    orientations = {}

    for permutation in combinations(cells, size):
        centered = False
        touches_edge = False

        for x, y in permutation:
            if (x, y) in center:
                centered = True
            if x == 0 or y == 0:
                touches_edge = True

        if not centered or not touches_edge:
            continue

        connected = [permutation[0]]
        stack = [permutation[0]]

        while stack:
            x, y = stack.pop()

            neighbors = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1),
            ]

            for neighbor in neighbors:
                if neighbor in permutation and neighbor not in connected:
                    connected.append(neighbor)
                    stack.append(neighbor)

        if len(connected) == size:
            key = rotation_key(permutation)
            orientation = normalize(permutation)

            if key not in groups:
                groups[key] = []
                orientations[key] = []

            if orientation not in orientations[key]:
                orientations[key].append(orientation)
                groups[key].append(permutation)

    return list(groups.values())


def main():
    tetrominos = generate_tetrominos()

    for group in tetrominos:
        print()
        for tetromino in group:
            print(tetromino)


if __name__ == "__main__":
    main()