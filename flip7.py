from random import randint


def generate_deck(cards):
    deck = []
    for card in range(cards + 1):
        for n in range(card):
            deck.append(card)

    deck_size = len(deck)

    spaces = []
    for i in range(deck_size):
        spaces.append(i)

    shuffled_deck = []
    for i in range(deck_size):
        shuffled_deck.append(None)

    for i in range(deck_size):
        spaces_left = len(spaces)
        spaces_index = randint(0, spaces_left - 1)
        position = spaces[spaces_index]
        shuffled_deck[position] = deck[i]
        spaces.pop(spaces_index)

    return shuffled_deck


cards = 12

flip = 22
games = 10000
total = 0
for game in range(games):
    points = 0
    hand = []

    deck = generate_deck(cards)

    alive = True
    while alive:
        points += deck[0]
        for card in hand:
            if card == deck[0]:
                points = 0
                alive = False

        hand.append(deck[0])
        deck.pop(0)

        if points > flip:
            alive = False

    print(hand, points)
    total += points

average_score = total / games
print(average_score)
