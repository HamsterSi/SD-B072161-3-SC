import itertools, random
from card import *
from player import *
from central_Area import *

# Initialise the players and the central area
def initialise_Game(player, computer, central): 
    sdc = [ 4 * [Card('Archer',    (3, 0), 2)], 4 * [Card('Baker',       (0, 3), 2)],
            3 * [Card('Swordsman', (4, 0), 3)], 2 * [Card('Knight',      (6, 0), 5)],
            3 * [Card('Tailor',    (0, 4), 3)], 3 * [Card('Crossbowman', (4, 0), 3)],
            3 * [Card('Merchant',  (0, 5), 4)], 4 * [Card('Thug',        (2, 0), 1)],
            4 * [Card('Thief',     (1, 1), 1)], 2 * [Card('Catapault',   (7, 0), 6)], 
            2 * [Card('Caravan',   (1, 5), 5)], 2 * [Card('Assassin',    (5, 0), 4)]]
    deck = list(itertools.chain.from_iterable(sdc))
    random.shuffle(deck)
    central.deck = deck 
    central.put_To_central()
    central.supplement = 10 * [Card('Levy', (1, 2), 2)]

    deck = [8 * [Card('Serf', (0, 1), 0)], 2 * [Card('Squire', (1, 0), 0)]]
    player.deck   = list(itertools.chain.from_iterable(deck))
    player.put_To_Hand()
    computer.deck = list(itertools.chain.from_iterable(deck)) 
    computer.put_To_Hand()


# Player's turn to play the deck card game
def player_Turn(player, computer, central):
    print "\n", 25*'-', "Player Turn", 25*'-', "\n"
    while True:
        print "HEALTH INFO:\tPlayer: %2s,\tComputer: %2s" % (player.health, computer.health)
        print "YOUR VALUES:\tMoney : %2s,\tAttack  : %2s\n" % (player.money,  player.attack)
        player.print_Cards()

        print "\nChoose Action: ('p' = play all, [0-n] = play that card, \n\t\t'b' = Buy Card, 'a' = Attack, 'e' = end turn)"
        index = raw_input("Choose Action: "); print "\n"

        if   index == 'P' or index == 'p': player.play_All_Cards()
        elif index.isdigit():              player.play_That_Card(int(index))
        elif index == 'B' or index == 'b': player_Buy(player, central)
        elif index == 'A' or index == 'a': 
            # Attack computer, then check if computer dies and player wins the game
            player.attack_Opponent(computer)
            if decide_Winner(player, computer, central) != True: 
                return True; break
        elif index == 'E' or index == 'e': # End player's turn
            player.put_To_Discards()
            player.put_To_Hand()
            print 23*'-', "Player Turn End", 23*'-', "\n"; break
        else: print ">>> ERROR: Please enter a valid option"

        print "\n", 18*'-', "Player Card Information", 18*'-', "\n"


# Computer's turn to play the deck card game
def computer_Turn(player, computer, central, aggressive):
    print "\n", 24*'-', "Computer Turn", 24*'-', "\n"
    print "HEALTH INFO:\t Player: %2s,\tComputer: %2s" % (player.health, computer.health)

    computer.money = 0; computer.attack = 0
    computer.play_All_Cards() # Computer always plays all cards
    print "COMPUTER VALUES: Money : %2s,\tAttack  : %2s\n" % (computer.money, computer.attack)

    computer.attack_Opponent(player) # Computer attacks user
    print "HEALTH INFO:\t Player: %2s,\tComputer: %2s" % (player.health, computer.health)

    # Decide if computer wins the game after attacking user
    if decide_Winner(player, computer, central) != True: 
        return True;

    print "\nComputer starts buying, money value %s" % computer.money
    if computer.money > 0:  computer_Buy(computer, central, aggressive) # Computer buys cards
    else: print ">>> ERROR: Insufficient money to buy"
    
    computer.put_To_Discards()
    computer.put_To_Hand()
    print "\n", 22*'-', "Computer Turn End", 22*'-', "\n"


#  Player buys cards from the central area
def player_Buy(player, central):
    if player.money <= 0: print ">>> ERROR: Insufficient money to buy"
    while player.money > 0:
        print "\n", 24*'-', "Buying Cards", 23*'-', "\n"
        print "MONEY VALUE: ", player.money, "\n"
        central.print_Cards()

        print "\nChoose a card to buy [0-n], 's' for supplement, 'e' to end buying"
        index = raw_input("Choose option: "); print "\n"

        if index.isdigit(): player.buy_Cards(central, int(index))
        elif index == 'S' or index == 's': player.buy_Supplements(central)
        elif index == 'E' or index == 'e': print ">>> End buying cards"; break
        else: print ">>> ERROR: Please enter a valid option"


# Computer buys cards from the central area
def computer_Buy(computer, central, aggressive):
    tempList = []
    while computer.money > 0:
        tempList = []; hIndex = 0

        # Add cards to the temp list
        if len(central.supplement) > 0 and computer.money > central.supplement[0].cost:
                tempList.append(('S', central.supplement[0]))
        for i in range (0, central.activeSize):
            if central.active[i].cost <= computer.money:
                tempList.append((i, central.active[i]))

        if len(tempList) > 0:
            for i in range(0, len(tempList)):
                # Pick the most expensive supplement or card
                if tempList[i][1].cost  > tempList[hIndex][1].cost: hIndex = i
                if tempList[i][1].cost == tempList[hIndex][1].cost:
                    # If computer is aggressive then choose the one with higher attack
                    if aggressive and tempList[i][1].get_Attack() > tempList[hIndex][1].get_Attack():
                            hIndex = i
                    elif tempList[i][1].get_Attack() > tempList[hIndex][1].get_Money():
                            hIndex = i
            i = tempList[hIndex][0]
            if i in range(0, 5): computer.buy_Cards(central, i)
            elif i == 'S': computer.buy_Supplements(central)
        else: break


# The decide_Winner function is called by players every turn to check if there is a winner
def decide_Winner(player, computer, central):
    if central.activeSize == 0:
        print "\n", 63*'-', "\n>>> GMAE END: No more cards available in central"
        if   player.health > computer.health: print ">>> GMAE END: Player Wins on Health\n"
        elif player.health < computer.health: print ">>> GMAE END: Computer Wins on Health\n"
        else:
            pStrength = 0; cStrength = 0
            for card in player.hand:      pStrength = pStrength + card.get_Attack()
            for card in player.discard:   pStrength = pStrength + card.get_Attack()
            for card in computer.hand:    cStrength = cStrength + card.get_Attack()
            for card in computer.discard: cStrength = cStrength + card.get_Attack()
            if   pStrength > cStrength: print ">>> GMAE END: Player Wins on Card Strength\n"
            elif pStrength < cStrength: print ">>> GMAE END: Computer Wins on Card Strength\n"
            else: print "Draw"
    elif player.health   <= 0: print "\n", 63*'-', "\n>>> GMAE END: Computer wins\n"
    elif computer.health <= 0: print "\n", 63*'-', "\n>>> GMAE END: Player Wins\n"
    else: return True
