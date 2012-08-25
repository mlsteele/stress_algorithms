from sets import Set
from random import choice
from itertools import groupby


class MOStressPlayer(object):
    def __init__(self, trace=False, largest_only=True):
        self.trace = trace
        self.largest_only = largest_only

    # table : array of 4 Cards
    # hands : array of 6 arrays of 4 Cards
    # returns : None for no action, array of 2 Cards for a trade
    def turn(self, table, hands):
        move = self._turn(table, hands)
        trace = self.trace
        if move and trace:
            c1, c2 = move
            hand = [hand for hand in hands if c1 in hand or c2 in hand][0]
            if c2 in hand:
                c1, c2 = c2, c1
            print "trade", c1, "from", hand, "for", c2, '->', [c for c in hand if c != c1] + [c2]
        return move

    def _turn(self, table, hands):
        # Ignore hands that have four of a kind
        hands = [hand for hand in hands if len(hand_ranks(hand)) > 1]
        if not hands:
            return None

        # Does any card on the table increment a hand that has (3, 2, 1) of a kind?
        # If so, swap it for one of the other cards in that hand.
        for count in [3, 2, 1]:
            for rank, hand in hands_with_kinds(hands, count):
                if rank in (card.n() for card in table) and (not self.largest_only or hand_max_kind_count(hand) == count):
                    other_cards = [card for card in hand if card.n() != rank]
                    return other_cards[0], [card for card in table if card.n() == rank][0]

        # Else, does any card in a hand increment another hand that has (3, 2, 1) of a kind?
        # If so, swap it for a card on the table.
        for count in [3, 2, 1]:
            for rank, hand in hands_with_kinds(hands, count):
                for another_hand in filter(lambda h: h != hand, hands):
                    if rank in (card.n() for card in another_hand):
                        other_cards = [card for card in another_hand if card.n() == rank]
                        return other_cards[0], table[0]

        # Otherwise look for a singleton
        for hand in hands:
            for card in hand:
                if sum(int(other_card.n() == card.n()) for other_card in hand) == 1:
                    return card, choice(table)

        # Otherwise, swap a random card that doesn't contribute to a set for a random card on the table.
        return choice(choice(hands)), choice(table)


# Return the greatest count of same-ranked cards in a hand
def hand_max_kind_count(hand):
    return max(len(list(xs)) for _, xs in groupby(sorted(card.n() for card in hand)))


# Return the ranks in hand
def hand_ranks(hand):
    return Set(card.n() for card in hand)


# Generate a sequence of tuples of (rank, hand) where `hand` has `count` cards of rank `rank`.
def hands_with_kinds(hands, count):
    for hand in hands:
        for rank in hand_ranks(hand):
            if sum(int(card.n() == rank) for card in hand) == count:
                yield rank, hand
