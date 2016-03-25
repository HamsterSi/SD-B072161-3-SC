import itertools, random
from card import *
from player import *

# Define a Central Area class to manage the central cards
class Central(object):
    def __init__(self, name, active=None, activeSize=5, supplement=None, deck=None):
        self.name   = name
        self.active = active
        self.activeSize = activeSize
        self.supplement = supplement
        self.deck   = deck

    # Print the available cards and supplements
    def print_Cards(self):
        for i in range(0, len(self.active)):
            print "Available Cards [%d]: %s" % (i, self.active[i])
        if len(self.supplement) > 0:
            print "Supplements        :", self.supplement[0]

    # Put the cards to the central for players to buy form the deck
    def put_To_central(self):
        for i in range(0, self.activeSize):
            self.active.append(self.deck.pop())