#!/usr/bin/env python3

number_players = 5
state_players = []


def main():
    player = 0

    for _i in range(number_players):
        state_players.append(True)

    player = solve()

    print(player)


def solve():
    player = 0
    for _i in range(number_players - 1):
        state_players[(player + 1) % number_players] = False
        player += 2
        print(state_players)
    player %= number_players
    return player


if __name__ == "__main__":
    main()
