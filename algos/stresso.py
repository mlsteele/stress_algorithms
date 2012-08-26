from sets import Set
from random import choice
from itertools import groupby, product


class OStressPlayer(object):
    def __init__(self, trace=False):
        self.trace = trace

    # table : array of 4 Cards
    # hands : array of 6 arrays of 4 Cards
    # returns : None for no action, array of 2 Cards for a trade
    def turn(self, table, hands):
        # Ignore hands that have four of a kind
        hands = [hand for hand in hands if len(hand_ranks(hand)) > 1]
        if not hands:
            return None

        value = self.evaluate(table, hands)
        for move_generator in self.turns(table, hands):
            move = maximize(move_generator(), lambda move: self.evaluate_move(table, hands, move), min=value)
            if move:
                return move

        return None

    # Returns [discard, take] or None
    def turns(self, table, hands):
        generators = []

        # Does any card on the table increment a hand that has (3, 2, 1) of a kind?
        # If so, swap it for one of the other cards in that hand.
        def increment_hand():
            for count in [3, 2, 1]:
                for rank, hand in hands_with_kinds(hands, count):
                    if rank in (card.n() for card in table) and hand_max_kind_count(hand) == count:
                        other_cards = [card for card in hand if card.n() != rank]
                        # does any of these increment a rank in another hand?
                        other_ranks = Set(card.n() for other_hand in hands if other_hand != hand for card in other_hand) - Set([rank])
                        contributing_cards = [card for card in other_cards if card.n() in other_ranks]
                        take = next(card for card in table if card.n() == rank)
                        if contributing_cards:
                            for discard in contributing_cards:
                                yield discard, take
                        else:
                            yield other_cards[0], take
        generators.append(increment_hand)

        # Else, does any card in a hand increment another hand that has (3, 2, 1) of a kind?
        # If so, swap it for a card on the table.
        def donate_to_other_hand():
            for count in [3, 2, 1]:
                for rank, hand in hands_with_kinds(hands, count):
                    for another_hand in filter(lambda h: h != hand, hands):
                        if rank in (card.n() for card in another_hand):
                            other_cards = [card for card in another_hand if card.n() == rank]
                            yield other_cards[0], table[0]
        generators.append(donate_to_other_hand)

        # Otherwise look for a singleton
        def donate_singleton():
            for hand in hands:
                for card in hand:
                    if sum(int(other_card.n() == card.n()) for other_card in hand) == 1:
                        yield card, choice(table)
        # doesn't seem to help
        # generators.append(donate_singleton)

        # Otherwise, swap a random card that doesn't contribute to a set for a random card on the table.
        def donate_random_card():
            yield choice(choice(hands)), choice(table)
        generators.append(donate_random_card)

        # 52s
        def exhaustive():
            for take in table:
                for hand in hands:
                    for card in hand:
                        yield card, take
        # return [exhaustive]

        return generators

    def evaluate(self, table, hands):
        hand_rank_scores = [None, 0, 10, 20, 1000]
        table_contribution_scores = [None, 0, 1, 2, 100]
        score = 0
        score += sum(hand_rank_scores[hand_max_kind_count(hand)] for hand in hands)
        score += sum(table_contribution_scores[hand_max_kind_count(hand + [card])] for hand in hands for card in table)
        return score

    def evaluate_move(self, table, hands, move):
        # print 'evaluateing', move
        if move:
            discard, take = move
            table = [discard if card == take else card for card in table]
            hands = [[take if card == discard else card for card in hand] for hand in hands]
        return self.evaluate(table, hands)


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


def maximize(sequence, fn, min=float("-inf")):
    best_score, best_value = min, None
    for x in sequence:
        score = fn(x)
        if score > best_score:
            best_value, best_score = x, score
    return best_value
