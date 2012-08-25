class Card(object):
    def __init__(s, val):
        s._val = val

    def n(s):
        return s._val

    def __repr__(s):
        return "*%s" % s._val
