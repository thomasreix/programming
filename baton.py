#!/usr/bin/env python3
import random
import sys


def check_win(baton, range):
    if baton <= 0:
        return True


def ask(range, player):
    taken = None
    while not taken:
        try:
            taken = int(input(f"{player} prends 1 à {range} baton: "))
        except ValueError:
            continue
        if taken < 1 or taken > range:
            taken = None
    print("")
    return taken


def sys_argv():
    if len(sys.argv) > 1:
        try:
            apponant = sys.argv[1]
        except ValueError:
            sys.exit(1)
        if apponant != "bot" and apponant != "adversaire":
            sys.exit(1)

        try:
            range = int(sys.argv[2])
        except ValueError:
            sys.exit(1)
        if range < 1:
            sys.exit(1)

        try:
            batons = int(sys.argv[3])
        except ValueError:
            sys.exit(1)
        if batons < 1:
            sys.exit(1)
    else:
        apponant = "bot"
        batons = 20
        range = 4

    arg = [apponant, batons, range]
    return arg


def main():
    arg = sys_argv()
    apponant = arg[0]
    batons = arg[1]
    range = arg[2]

    if len(sys.argv) > 1:
        try:
            apponant = sys.argv[1]
        except ValueError:
            sys.exit(1)
        if apponant != "bot" and apponant != "adversaire":
            sys.exit(1)
    else:
        apponant = "bot"

    turn = 0
    while batons > 0:
        print(f"Il reste {batons} batons")

        turn += 1
        if turn % 2 == 1:
            taken = ask(range, "Joueur")
        else:
            if apponant == "bot":
                taken = (batons - 1) % (range + 1)
                if taken == 0:
                    taken = random.randint(1, range)
                print(f"Le bot prend {taken} batons\n")
            else:
                taken = ask(range, "Adversaire")

        batons -= taken
        if check_win(batons, range):
            if turn % 2 == 1:
                print(f"{apponant} a gagné !")
            else:
                print("Joueur a gagné !")
            sys.exit(0)


if __name__ == "__main__":
    main()
