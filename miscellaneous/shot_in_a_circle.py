#!/usr/bin/env python3


def solve(n: int) -> int:
    players = list(range(n))
    current = 0
    while len(players) > 1:
        # print(f"current={current} players={players}")
        if current == len(players) - 1:  # Last
            del players[0]
            current = 0
        else:
            del players[(current + 1) % len(players)]
            current = (current + 1) % (len(players))
    return players[0]


def main():
    print(f"solve(n=100)={solve(n=100)}")


if __name__ == "__main__":
    main()
