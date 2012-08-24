import random, itertools, pprint
pp = pprint.pprint

class StressfulAlgorithm(object):
  # table : array of 4 Cards
  # hands : array of 6 arrays of 4 Cards
  # returns : None for no action, tuple of 2 Cards for a trade
  def turn(s, table, hands):
    return None

class DoNothing(StressfulAlgorithm):
  pass

class TradeConstant(StressfulAlgorithm):
  def turn(s, table, hands):
    return table[0], hands[0][0]

class RandomTrade(StressfulAlgorithm):
  def turn(s, table, hands):
    return random.choice(table), random.choice(random.choice(hands))
