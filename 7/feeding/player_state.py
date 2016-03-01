class PlayerState(object):
    """
    Represents data about the player that is kept track of by the dealer
    in order to prevent the player from modifying their data or acting out of turn
    the dealer only sends the minimum amount of data needed for the player to make
    choices
    """
    def __init__(self, name=None, food_bag=0, hand=[], species=[]):
        self.name = name
        self.food_bag = food_bag
        self.hand = hand
        self.species = species

    def __str__(self):
        return "PlayerState(Food=%d, Hand=%s, Species=%s" % (self.food_bag, self.hand, self.species)

    def __eq__(self, other):
        return all([isinstance(other, PlayerState),
                    self.name == other.name,
                    self.food_bag == other.food_bag,
                    self.hand == other.hand,
                    self.species == other.species])