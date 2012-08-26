#/usr/bin/env python
import main
from main import *
main.TRACE_MOVES = False

import random
import itertools

def group_n(a, n):
    return map(lambda e: map(lambda t: t[0], e[1]), itertools.groupby(zip(a, [i / n for i in range(len(a))]), lambda e: e[1]))

def deal():
    deck = [Card(n) for n in range(1, 13) for suit in xrange(4)]
    random.shuffle(deck)
    return deck[0:4], group_n(deck[4:28], 4), group_n(deck[28:52], 4)

def play(algo1, algo2, round_limit=100):
    table, hands1, hands2 = deal()

    rounds = 0
    while True:
        if rounds >= round_limit * 2:
            # print 'draw after', round_limit, 'rounds'
            return 'draw'
        rounds += 1
        player, hands, name = [[algo1, hands1, 'player 1'], [algo2, hands2, 'player2']][random.randrange(0, 2)]
        execute_trade(player.turn(table, hands), table, hands)
        win1, win2 = map(lambda hands: hands_are_solved(hands), [hands1, hands2])
        if win1 and win2:
            return 'tie'
        if win1:
            return 'player 1'
        if win2:
            return 'player 2'

def compare(algo1, algo2, games=100):
    outcomes = {}
    for i in xrange(games):
        outcome = play(algo1, algo2)
        # print i + 1, outcome
        if outcome not in outcomes:
            outcomes[outcome] = 0
        outcomes[outcome] += 1
    for k in sorted(outcomes.keys()):
        print k, outcomes[k], '(%2.0f%%)' % (100.0 * outcomes[k] / games)

if __name__ == '__main__':
    compare(algos.MOStressPlayer(), algos.MSSimple1(debug=False))
