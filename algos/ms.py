from common import *

class MSSimple1(StressfulAlgorithm):
  DEBUG = False

  def __init__(s, debug=True):
    s.DEBUG = debug

  def turn(s, table, hands):
    def most_common(a, eq):
      return sorted(zip(a, map(lambda e: len(filter(lambda e2: eq(e, e2), a)), a)), key=lambda p: p[1])[-1]
    cdv = lambda c: c.n()
    rci = lambda: random.randrange(4)

    if s.DEBUG: print "MSSimple1 turn BEGIN"

    def hand_processor(hand):
      if s.DEBUG: print "here's a hand for processing: %s" % hand
      sorted_hand = sorted(hand, key=cdv)
      if s.DEBUG: print "sorted hand: %s" % sorted_hand
      k, count = most_common(sorted_hand, lambda a,b: a.n() == b.n())
      if s.DEBUG: print "processed hand to: %s" % ([k, count, sorted_hand])
      # k is the card of the most common number
      return k, count, sorted_hand

    sorted_phands = list(reversed(sorted(map(hand_processor, hands), key=lambda ph: ph[1])))
    if s.DEBUG: print "sorted_phands\n---"
    if s.DEBUG: pp(sorted_phands)
    if s.DEBUG: print "--"

    # gather unused cards to throw
    unused_cards = []
    for k, count, hand in sorted_phands:
      for card in hand:
        if card.n() != k.n():
          unused_cards.append(card)
    if s.DEBUG: print "found %s unused cards" % len(unused_cards)

    # consider hands in order of interesting
    for k, count, hand in sorted_phands:
      if count == 4:
        if s.DEBUG: print "hand has 4 of a kind: %s" % hand
        pass
      elif count > 1:
        if s.DEBUG: print "hand has multiple of a kind: %s" % hand
        if any(map(lambda tc: tc.n() == k.n(), table)):
          if s.DEBUG: print "relevant cards on table"
          throw_card = filter(lambda c: c.n() != k.n(), hand)[0]
          get_card = filter(lambda c: c.n() == k.n(), table)[0]
          return throw_card, get_card
      else:
        if s.DEBUG: print "hand has uniques: %s" % hand

    if s.DEBUG: print "finished hands without action"
    if s.DEBUG: print "switching semi-randomly"
    if len(unused_cards) > 0:
      # # TODO: does this help at all?
      # k, count = most_common(table, lambda a,b: a.n() == b.n())
      # if count > 1:
      #   return filter(lambda c: c.n() == k.n(), table)[0], random.choice(unused_cards)
      # else:
      #   return random.choice(table), random.choice(unused_cards)
      return random.choice(table), random.choice(unused_cards)


class RandHand(StressfulAlgorithm):
  DEBUG = True

  def turn(s, table, hands):
    def most_common(a, eq):
      return sorted(zip(a, map(lambda e: len(filter(lambda e2: eq(e, e2), a)), a)), key=lambda p: p[1])[-1]
    cdv = lambda c: c.n()
    rci = lambda: random.randrange(4)

    if s.DEBUG: print "RandHand turn BEGIN"

    def hand_processor(hand):
      if s.DEBUG: print "here's a hand for processing: %s" % hand
      sorted_hand = sorted(hand, key=cdv)
      if s.DEBUG: print "sorted hand: %s" % sorted_hand
      k, count = most_common(sorted_hand, lambda a,b: a.n() == b.n())
      if s.DEBUG: print "processed hand to: %s" % ([k, count, sorted_hand])
      return k, count, sorted_hand

    # randomly choose one hand to play with
    phand = hand_processor(random.choice(hands))

    # gather unused cards to throw
    unused_cards = filter(lambda card: card.n() != phand[0], phand[2])
    if s.DEBUG: print "found %s unused cards" % len(unused_cards)

    # consider hands in order of interesting
    k, count, hand = phand
    if count == 4:
      if s.DEBUG: print "hand has 4 of a kind: %s" % hand
      pass
    elif count > 1:
      if s.DEBUG: print "hand has multiple of a kind: %s" % hand
      if any(map(lambda tc: tc.n() == k.n(), table)):
        if s.DEBUG: print "relevant cards on table"
        throw_card = filter(lambda c: c.n() != k.n(), hand)[0]
        get_card = filter(lambda c: c.n() == k.n(), table)[0]
        return throw_card, get_card
    else:
      if s.DEBUG: print "hand has uniques: %s" % hand

    if s.DEBUG: print "finished hands without action"
    if s.DEBUG: print "switching semi-randomly"
    if len(unused_cards) > 0:
      # # TODO: does this help at all?
      # k, count = most_common(table, lambda a,b: a.n() == b.n())
      # if count > 1:
      #   return filter(lambda c: c.n() == k.n(), table)[0], random.choice(unused_cards)
      # else:
      #   return random.choice(table), random.choice(unused_cards)
      return random.choice(table), random.choice(unused_cards)


# class Devious(StressfulAlgorithm):
#   DEBUG = True

#   def turn(s, table, hands):
#     def most_common(a, eq):
#       return sorted(zip(a, map(lambda e: len(filter(lambda e2: eq(e, e2), a)), a)), key=lambda p: p[1])[-1]
#     cdv = lambda c: c.n()
#     rci = lambda: random.randrange(4)

#     if s.DEBUG: print "Devious turn BEGIN"

#     def hand_processor(hand):
#       if s.DEBUG: print "here's a hand for processing: %s" % hand
#       sorted_hand = sorted(hand, key=cdv)
#       if s.DEBUG: print "sorted hand: %s" % sorted_hand
#       k, count = most_common(sorted_hand, lambda a,b: a.n() == b.n())
#       if s.DEBUG: print "processed hand to: %s" % ([k, count, sorted_hand])
#       return k.n(), count, sorted_hand

#     sorted_phands = list(reversed(sorted(map(hand_processor, hands), key=lambda ph: ph[1])))
#     if s.DEBUG: print "sorted_phands\n---"
#     if s.DEBUG: pp(sorted_phands)
#     if s.DEBUG: print "--"

#     unsolved_phands = filter(lambda ph: ph[1] != 4, sorted_phands)

#     table_ns = set.Set(map(cdv, table))
#     my_cards = reduce(lambda a, h: a + h, hands, [])

#     # my_unsolved_numbers = set.Set(map(cdv, reduce(lambda a, ph: a + ph[2], unsolved_phands, [])))

#     if one trade away from winning, do it
#     else
#       selfish moves = compile a list of selfish moves, sorted by beneficiality
#       do the most selfish move that does not give away
