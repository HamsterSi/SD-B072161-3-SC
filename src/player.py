
import itertools, random
from card import *
from central_Area import *

# Define the Player class with their own values and functions
class Player(object):
    def __init__(self, name, health=30, deck=None, hand=None, handsize=5, active=None, discard=None, money=0, attack=0):
        self.name = name
        self.health = health
        self.deck = deck
        self.hand = hand
        self.handsize = handsize
        self.active = active
        self.discard = discard
        self.money = money
        self.attack = attack

    # Put the card to player's hand from the deck
    # If no card left in deck, then deck takes cards from the discard pile
    def put_To_Hand(self):
        for i in range(0, self.handsize):
            if len(self.deck) == 0:
                random.shuffle(self.discard)
                self.deck = self.discard
                self.discard = []
            self.hand.append(self.deck.pop())

    # Print the hand cards and played (Active) cards for the player
    def print_Cards(self):
        for i in range(0, len(self.hand)):
            print "Hand Cards [%d]: %s" % (i, self.hand[i])
        for card in self.active:
            print ">>> Active Cards:", card

    # Player plays all hand cards, these cards are put into the active area
    # The value of money and attack are calculated automatically
    def play_All_Cards(self):
        if len(self.hand) > 0:
            for i in range(0, len(self.hand)):
                card = self.hand.pop()
                self.active.append(card)
                self.money  = self.money  + card.get_Money()
                self.attack = self.attack + card.get_Attack()
            print ">>> Played all cards"
        else: print ">>> ERROR: No more hand cards available"

    # Player plays only one card, the card is put into the active area
    # The value of money and attack are calculated automatically
    def play_That_Card(self, i):
        if i >= 0 and i < len(self.hand) and len(self.hand) > 0: 
            self.money = 0; self.attack = 0       
            self.active.append(self.hand.pop(i))
            for card in self.active:
                self.money = self.money + card.get_Money()
                self.attack = self.attack + card.get_Attack()
            print ">>> Played card %d" % i
        else: print ">>> ERROR: Please enter a valid option"

    # Player buys cards from the central area
    def buy_Cards(self, central, i):
        if i > len(central.active):
            print ">>> ERROR: Please enter a valid option"
        elif self.money < central.active[i].cost:
            print ">>> ERROR: Insufficient money to buy"
        else:
            self.money = self.money - central.active[i].cost
            card = central.active.pop(i)
            self.discard.append(card)
            if(len(central.deck) > 0):
                central.active.append(central.deck.pop())
            else:
                central.activeSize = central.activeSize - 1
            print ">>> Card %s bought, cost %d, %d moeny left" % (card.name, card.cost, self.money)
            if self.money == 0: print ">>> End buying cards"

    # Player buys supplements from the central area
    def buy_Supplements(self, central):
        if len(central.supplement) <= 0:
            print ">>> ERROR: No supplements left"
        elif self.money < central.supplement[0].cost:
            print ">>> ERROR: Insufficient money to buy"
        else:
            self.money = self.money - central.supplement[0].cost
            self.discard.append(central.supplement[0])
            card = self.discard[len(self.discard) - 1]
            print ">>> Supplement %s bought, cost %d, %d moeny left" % (card.name, card.cost, self.money)
            if self.money == 0: print ">>> End buying cards"

    # Player attacks opponent with all available attack values
    def attack_Opponent(self, opponent):
        if self.attack <= 0: print ">>> ERROR: No attack value"
        else: 
            print ">>> %s attacked %s with strength %s" % (self.name, opponent.name, self.attack)
            opponent.health = opponent.health - self.attack
            self.attack = 0

    # Player's turn ends, put the hand cards and active cards into the discard pile
    def put_To_Discards(self):
        for i in range(0, len(self.hand)):   
            self.discard.append(self.hand.pop())
        for i in range(0, len(self.active)): 
            self.discard.append(self.active.pop())
