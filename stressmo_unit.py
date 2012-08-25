import unittest
from card import Card
from algos.stressmo import *

class TestMOStressPlayerUtilities(unittest.TestCase):

    def test_hand_max_kind_count(self):
        self.assertEqual(hand_max_kind_count(make_hand(1, 2, 3, 4)), 1)
        self.assertEqual(hand_max_kind_count(make_hand(1, 1, 3, 4)), 2)
        self.assertEqual(hand_max_kind_count(make_hand(1, 2, 1, 4)), 2)
        self.assertEqual(hand_max_kind_count(make_hand(1, 1, 1, 4)), 3)
        self.assertEqual(hand_max_kind_count(make_hand(1, 1, 1, 1)), 4)

    def test_hand_ranks(self):
        self.assertEqual(hand_ranks(make_hand(1, 2, 3, 4)), Set([1, 2, 3, 4]))
        self.assertEqual(hand_ranks(make_hand(1, 1, 3, 4)), Set([1, 3, 4]))
        self.assertEqual(hand_ranks(make_hand(1, 2, 1, 4)), Set([1, 2, 4]))
        self.assertEqual(hand_ranks(make_hand(1, 1, 1, 4)), Set([1, 4]))
        self.assertEqual(hand_ranks(make_hand(1, 1, 1, 1)), Set([1]))

    def test_hands_with_kinds(self):
        h0 = make_hand(1, 2, 3, 4)
        h1 = make_hand(1, 1, 2, 2)
        h2 = make_hand(5, 5, 5, 6)
        h3 = make_hand(7, 7, 7, 7)
        hands = [h0, h1, h2, h3]
        self.assertEqual(list(hands_with_kinds(hands, 4)), [(7, h3)])
        self.assertEqual(list(hands_with_kinds(hands, 3)), [(5, h2)])
        self.assertEqual(list(hands_with_kinds(hands, 2)), [(1, h1), (2, h1)])
        self.assertEqual(list(hands_with_kinds(hands, 1)), [(1, h0), (2, h0), (3, h0), (4, h0), (6, h2)])


class TestMOStressPlayer(unittest.TestCase):

    def setUp(self):
        self.algo = MOStressPlayer()

    def test_turn(self):
        pass


def make_hand(*ranks):
    return [Card(rank) for rank in ranks]

if __name__ == '__main__':
    unittest.main()
