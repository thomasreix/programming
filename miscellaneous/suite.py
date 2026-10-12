def next(n):
    return 2 * n**2 - n + 1


def main():
    i = 1
    n = 1
    print(n)
    while i < 2024:
        i += 1
        n = next(n)
        print(n)


if __name__ == "__main__":
    main()
