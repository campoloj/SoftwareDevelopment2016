class PlayerState(object):
    """
    Represents data about the player that is kept track of by the dealer
    in order to prevent the player from modifying their data or acting out of turn
    the dealer only sends the minimum amount of data needed for the player to make
    choices
    """
    def __init__(self, name=None, food_bag=0, hand=None, species=None):
        self.name = name
        self.food_bag = food_bag
        self.hand = hand if hand else []
        self.species = species if species else []

    def __str__(self):
        return "PlayerState(Food=%d, Hand=%s, Species=%s" % (self.food_bag, self.hand, self.species)

    def __eq__(self, other):
        return all([isinstance(other, PlayerState),
                    self.name == other.name,
                    self.food_bag == other.food_bag,
                    self.hand == other.hand,
                    self.species == other.species])

    @classmethod
    def get_left_neighbor(cls, species, list_of_species):
        """
        Gets the left neighbor of the given Species in the given list of species
        :param species: Species of which to find neighbor
        :param list_of_species: An ordered list of Species
        :return: The Species to the left of the given Species
        """
        species_index = list_of_species.index(species)
        return False if species_index == 0 else list_of_species[species_index - 1]

    @classmethod
    def get_right_neighbor(cls, species, list_of_species):
        """
        Gets the right neighbor of the given Species in the given list of species
        :param species: Species of which to find neighbor
        :param list_of_species: An ordered list of Species
        :return: The Species to the right of the given Species
        """
        species_index = list_of_species.index(species)
        return False if species_index == len(list_of_species) - 1 else list_of_species[species_index + 1]