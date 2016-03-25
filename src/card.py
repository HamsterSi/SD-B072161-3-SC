# Define a Card class
# Can be used to initialise all game cards
class Card(object):
    def __init__(self, name, values=(0, 0), cost=1, clan=None):
        self.name = name
        self.cost = cost
        self.values = values
        self.clan = clan
    def __str__(self):
        return 'Name %-11s costing %s with attack %s and money %s' % (self.name, self.cost, self.values[0], self.values[1])
    def get_Attack(self):
        return self.values[0]
    def get_Money(self):
        return self.values[1]