EMPTY = 0
QUEEN = 1


def empty_board():
    board = []
    size = 5
    for y in range(size):
        row = []
        for x in range(size):
            row.append(EMPTY)
        board.append(row)

    return board


def display_board(board):
    for row in board:
        displayed_row = ""
        for cell in row:
            if cell is EMPTY:
                displayed_row += "- "
            else:
                displayed_row += "Q "
        print(displayed_row)


def main():
    board = empty_board()
    display_board(board)
    while True:
        pass


if __name__ == "__main__":
    main()
