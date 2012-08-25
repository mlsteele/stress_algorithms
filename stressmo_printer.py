from card import Card
from algos.stressmo import *


def turn(table, hands):
    table = map(Card, table)
    hands = [map(Card, ranks) for ranks in hands]
    player = MOStressPlayer()
    move = player.turn(table, hands)
    if move:
        put, call = move
        table2 = [put if card == call else card for card in table]
        hands2 = [[call if card == put else card for card in hand] for hand in hands]
        print " ".join(map(lambda card: str(card.n()), table)), "\t", hands, "\t", "discard", put, "take", call, "->\t", table2, "\t", hands2
    else:
        print table, hands, "none"

turn([1, 2, 3, 4], [[1, 1, 1, 5]])
turn([1, 2, 3, 4], [[1, 1, 4, 5]])
turn([1, 2, 3, 4], [[1, 4, 5, 6]])
# operate on the hand with 3 even if there's a hand with 2
turn([1, 2, 3, 4], [[1, 1, 4, 5], [3, 3, 3, 6]])
turn([1, 2, 3, 4], [[1, 1, 4, 5], [7, 7, 7, 6]])

# nothing to take; should discard a card that's useful in another hand
turn([1, 2, 3, 4], [[5, 6, 7, 8], [10, 7, 11, 12]])

# Don't discard a 3 to increase a 1
turn([1, 2, 3, 4], [[5, 5, 5, 1]])
