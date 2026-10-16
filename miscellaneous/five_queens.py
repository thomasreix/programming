EMPTY = 0
QUEEN = 1


def empty():
    board = []
    size = 5
    for y in range(size):
        row = []
        for x in range(size):
            row.append(EMPTY)
        board.append(row)

    return board


def display(board):
    for row in board:
        displayed_row = ""
        for cell in row:
            if cell is EMPTY:
                displayed_row += "- "
            else:
                displayed_row += "♕ "
        print(displayed_row)


def status(board):
    used = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell == QUEEN:
                position = (x, y)
                used.append(position)
    for i, pos0 in enumerate(used):
        for j, pos1 in enumerate(used):
            if i != j:
                if (
                    pos0[0] == pos1[0]
                    or pos0[1] == pos1[1]
                    or pos0[0] + pos0[1] == pos1[0] + pos1[1]
                    or pos0[0] - pos0[1] == pos1[0] - pos1[1]
                ):
                    return False
    return True


def backtrack():
    board = empty()
    path = []
    visited = []
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if 

    

            


def main():
    display(board)


if __name__ == "__main__":
    main()
