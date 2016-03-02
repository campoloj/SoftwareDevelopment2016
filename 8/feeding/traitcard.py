class TraitCard(object):
    """
    A Trait Card of the Evolution game
    """
    def __init__(self, trait, food_points=0):
        self.trait = trait
        self.food_points = food_points

    def __str__(self):
        return "TraitCard(trait=%s, food=%d)" % (self.trait, self.food_points)

    def __eq__(self, other):
        return all([isinstance(other, TraitCard),
                    self.trait == other.trait,
                    self.food_points == other.food_points])
