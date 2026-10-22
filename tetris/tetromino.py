from itertools import combinations


def unique(tetromino: list[tuple[int, int]]) -> bool:
    size = len(tetromino)
    previous = -1
    for cell in tetromino:
        current = cell[0] + cell[1] * size
        if current == previous:
            return False
        previous = current
    return True


def connected(tetromino: list[tuple[int, int]]) -> bool:
    size = len(tetromino)
    connected_cells = 0
    for cell in tetromino:
        for neighbor in tetromino:
            if (
                cell[0] == neighbor[0]
                and cell[1] + 1 == neighbor[1]
                or cell[0] == neighbor[0]
                and cell[1] - 1 == neighbor[1]
                or cell[1] == neighbor[1]
                and cell[0] + 1 == neighbor[0]
                or cell[1] == neighbor[1]
                and cell[0] - 1 == neighbor[0]
            ):
                connected_cells += 1
    return connected_cells >= (size - 1) * 2


def most_connections(tetromino: list[tuple[int, int]]) -> tuple[int, int]:
    cells_connections = []
    for cell in tetromino:
        cell_connections = 0
        for neighbor in tetromino:
            if cell[0] == neighbor[0] and cell[1] + 1 == neighbor[1]:
                cell_connections += 1
            if cell[0] == neighbor[0] and cell[1] - 1 == neighbor[1]:
                cell_connections += 1
            if cell[1] == neighbor[1] and cell[0] + 1 == neighbor[0]:
                cell_connections += 1
            if cell[1] == neighbor[1] and cell[0] - 1 == neighbor[0]:
                cell_connections += 1
        cells_connections.append(cell_connections)
    most_connections_cells = []
    past_cell_conections = 0
    for i, cell_connections in enumerate(cells_connections):
        if cell_connections > past_cell_conections:
            most_connections_cells = [tetromino[i]]
            past_cell_conections = cell_connections
        elif cell_connections == past_cell_conections:
            most_connections_cells.append(tetromino[i])
            past_cell_conections = cell_connections
    most_connections_cell = most_connections_cells[0]
    return most_connections_cell


def mesure(tetromino: list[tuple[int, int]]) -> int:
    size = len(tetromino)
    offset_x = size
    offset_y = size
    for x, y in tetromino:
        offset_x = min(offset_x, x)
        offset_y = min(offset_y, y)
    width = 0
    height = 0
    for x, y in tetromino:
        width = max(width, x)
        height = max(height, y)
    lenth = max(width - offset_x, height - offset_y) + 1
    return lenth


def centered(tetromino: list[tuple[int, int]]) -> bool:
    center_cell = most_connections(tetromino)
    print(center_cell)
    lenth = mesure(tetromino)
    print(lenth)
    if lenth == 2:
        center_cells = [(0, 0)]
    elif lenth % 2 == 0:
        center_cells = [
            (lenth / 2 - 1, lenth / 2 - 1),
            (lenth / 2 - 1, lenth / 2),
            (lenth / 2, lenth / 2 - 1),
            (lenth / 2, lenth / 2),
        ]
    else:
        center_cells = [(lenth // 2, lenth // 2)]
    return center_cell in center_cells


def generate_tetrominos(size=4) -> list[list[tuple[int, int]]]:
    cells = []
    for x in range(size):
        for y in range(size):
            cell = (x, y)
            cells.append(cell)
    tetrominos = []
    for tetromino in combinations(cells, size):
        if unique(tetromino) and connected(tetromino) and centered(tetromino):
            tetrominos.append(tetromino)
    return tetrominos


def display(tetromino: list[tuple[int, int]]):
    for y in range(4):
        row = f"{y} "
        for x in range(4):
            if (x, y) in tetromino:
                row += " ■"
            else:
                row += "  "
        print(row)


def main() -> int:
    tetrominos = generate_tetrominos()

    # for pack in tetrominos:
    #     print()
    #     for tetromino in pack:
    #         print(tetromino)
    for tetromino in tetrominos:
        print(tetromino)
        display(tetromino)

    print(f"\n{len(tetrominos)}\n")


if __name__ == "__main__":
    main()
