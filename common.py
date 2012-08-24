# python 2.7

ENABLE_GRAPHICS = True

import random, itertools, time, pprint
pp = pprint.pprint

import algos
if ENABLE_GRAPHICS:
  try:
    import graphics
  except ImportError:
    import sys
    print >> sys.stderr, "Couldn't import pygame; skipping"
    ENABLE_GRAPHICS = False

class Card(object):
  def __init__(s, val):
    s._val = val

  def n(s):
    return s._val

  def __repr__(s):
    return "*%s" % s._val

def hands_are_solved(hands):
  return all(map(lambda hand: all(map(lambda card: card.n() == hand[0].n(), hand)), hands))

def execute_trade(trade_cards, table, hands):
  print "execute_trade(%s, table, hands)" % str(trade_cards)

  if trade_cards == None: return
  c1, c2 = trade_cards
  if c2 in table:
    c1, c2 = c2, c1
  table[table.index(c1)] = c2
  for hand in hands:
    if hand.count(c2) == 1:
      hand[hand.index(c2)] = c1

def main():
  deck = reduce(lambda x,y:x+y, [[Card(n) for n in range(1,14)] for suit in xrange(4)], [])
  random.shuffle(deck)

  def group_n(a, n):
    return map(lambda e: map(lambda t: t[0], e[1]), itertools.groupby(zip(a, [i / n for i in range(len(a))]), lambda e: e[1]))

  table = deck[0:4]
  hands1 = group_n(deck[4:28], 4)
  hands2 = group_n(deck[28:52], 4)

  algo1 = algos.MOStressPlayer()
  algo2 = algos.MSSimple1()

  while not all(map(lambda hands: hands_are_solved(hands), [hands1, hands2])):
    print "\nturn\n"
    print "table"
    pp(table)
    print "hands1"
    pp(hands1)
    print "hands2"
    pp(hands2)

    if ENABLE_GRAPHICS:
      graphics.render("%s\n%s\n%s" % (str(table), str(hands1), str(hands2)))
      graphics.handle_events()
      time.sleep(0.2)

    execute_trade(algo1.turn(table, hands1), table, hands1)
    execute_trade(algo2.turn(table, hands2), table, hands2)

  print "game over"


try:
  main()
except KeyboardInterrupt: 
  pass
except:
  raise
