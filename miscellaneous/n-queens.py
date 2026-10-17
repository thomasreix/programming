EMPTY = 0
QUEEN = 1

SOLUTIONS = []


def empty(n):
    board = []
    for y in range(n):
        row = []
        for x in range(n):
            row.append(EMPTY)
        board.append(row)

    return board


def rotate(board):
    n = len(board)
    rotated = []
    for col in range(n):
        row = []
        for y in range(n - 1, -1, -1):
            row.append(board[y][col])
        rotated.append(row)
    return rotated


def flip(board):
    return [row[::-1] for row in board]


def unique(solutions):
    unique_solutions = []
    seen = []
    for board in solutions:
        variants = []
        rotated = board
        for _ in range(4):
            variants.append([row[:] for row in rotated])
            reflected = flip(rotated)
            variants.append([row[:] for row in reflected])
            rotated = rotate(rotated)
        canonical = min(variants)
        if canonical not in seen:
            seen.append(canonical)
            unique_solutions.append(board)
    return unique_solutions


def display(boards, width):
    if not boards:
        return
    n = len(boards[0])
    for start in range(0, len(boards), width):
        group = boards[start : start + width]
        for row in range(n):
            string = ""
            for board in group:
                for cell in board[row]:
                    if cell == QUEEN:
                        string += "♕ "
                    else:
                        string += "_ "
                string += "   "
            print(string)
        print()


def is_safe(board, row, col):
    n = len(board)
    y = row
    left = col
    right = col
    while y >= 0:
        if (
            left >= 0
            and board[y][left] == 1
            or board[y][col] == 1
            or right < n
            and board[y][right] == 1
        ):
            return False
        else:
            y -= 1
            left -= 1
            right += 1
    return True


def is_solution(n, row):
    return row == n


def backtrack(board, row, solutions):
    n = len(board)
    if is_solution(n, row):
        solution = [row[:] for row in board]
        solutions.append(solution)
        return solutions
    for col in range(n):
        if is_safe(board, row, col):
            board[row][col] = QUEEN
            backtrack(board, row + 1, solutions)
            board[row][col] = EMPTY
    return solutions


def main():
    n = 8
    board = empty(n)
    solutions = backtrack(board, 0, [])
    unique_solutions = unique(solutions)
    number_of_solutions = len(solutions)
    number_of_unique_solutions = len(unique_solutions)
    print(f"The {n} queen problem has {number_of_solutions} solutions.")
    print(f"where {number_of_unique_solutions} solutions are unique. \n")
    display(unique_solutions, 4)


if __name__ == "__main__":
    main()
