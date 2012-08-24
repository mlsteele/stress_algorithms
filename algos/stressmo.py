from sets import Set
from random import choice


class MOStressPlayer(object):
    # table : array of 4 Cards
    # hands : array of 6 arrays of 4 Cards
    # returns : None for no action, array of 2 Cards for a trade
    def turn(s, table, hands):
        # Ignore hands that have four of a kind
        hands = [hand for hand in hands if len(hand_ranks(hand)) > 1]

        # Does any card on the table increment a hand that has (3, 2, 1) of a kind?
        # If so, swap it for one of the other cards in that hand.
        for count in [3, 2, 1]:
            # print count, list(hands_with_kinds(hands, count))
            for rank, hand in hands_with_kinds(hands, count):
                if rank in (card.n() for card in table):
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

        # Otherwise, swap a random card that doesn't contribute to a set for a random card on the table.
        return choice(choice(hands)), choice(table)


# Return the number of different ranks in the card in hands
def hand_ranks(hand):
    return Set(card.n() for card in hand)


# Generate a sequence of tuples of (rank, hand) where `hand` has `count` cards of rank `rank`.
def hands_with_kinds(hands, count):
    for hand in hands:
        for rank in hand_ranks(hand):
            if sum(int(card.n() == rank) for card in hand) == count:
                yield rank, hand
