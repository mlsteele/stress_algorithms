from common import *

class MSSimple1(StressfulAlgorithm):
  def turn(s, table, hands):
    def most_common(a, cmp):
      return sorted(zip(a, map(lambda e: len(filter(lambda e2: cmp(e, e2), a)), a)), key=lambda p: p[1])[-1]
    cdv = lambda c: c.n()
    rci = lambda: random.randrange(4)

    # print "MSSimple1 turn BEGIN"
    # def hand_processor(hand):
    #   print "here's a hand for processing: %s" % hand
    #   sorted_hand = sorted(hand, key=cdv)
    #   print "sorted hand: %s" % sorted_hand
    #   def kgsortmonkey(kg):
    #     print "kgsortmonkey -kg: %s" % list(kg[1])
    #     r = len(list(kg[1]))
    #     print "kgsortmonkey -r: %s" % r
    #     return r
    #   k, g = sorted(itertools.groupby(sorted_hand, cdv), key=kgsortmonkey)[-1]
    #   print "k: %s" % k
    #   print "g: %s" % g
    #   count = len(list(g))
    #   print "processed hand to: %s" % ([k, count, sorted_hand])
    #   return k, count, sorted_hand

    def hand_processor(hand):
      # print "here's a hand for processing: %s" % hand
      sorted_hand = sorted(hand, key=cdv)
      # print "sorted hand: %s" % sorted_hand
      k, count = most_common(sorted_hand, lambda a,b: a.n() == b.n())
      # print "processed hand to: %s" % ([k, count, sorted_hand])
      return k, count, sorted_hand

    sorted_phands = list(reversed(sorted(map(hand_processor, hands), key=lambda ph: ph[1])))
    # print "sorted_phands\n---"
    # pp(sorted_phands)
    # print "--"

    # gather unused cards to throw
    unused_cards = []
    for k, count, hand in sorted_phands:
      for card in hand:
        if card.n() != k.n():
          unused_cards.append(card)

    # consider hands in order of interesting
    for k, count, hand in sorted_phands:
      if count == 4:
        # print "hand has 4 of a kind: %s" % hand
        pass
      elif count > 1:
        # print "hand has multiple of a kind: %s" % hand
        if any(map(lambda tc: tc.n() == k.n(), table)):
          # print "relevant cards on table"
          throw_card = filter(lambda c: c.n() != k.n(), hand)[0]
          get_card = filter(lambda c: c.n() == k.n(), table)[0]
          return throw_card, get_card
      else:
        # print "hand has uniques: %s" % hand
        return random.choice(table), random.choice(unused_cards)
