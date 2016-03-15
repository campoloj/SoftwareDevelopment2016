from globals import *


class PlayerState(object):
    """
    Represents data about the player that is kept track of by the dealer
    in order to prevent the player from modifying their data or acting out of turn
    the dealer only sends the minimum amount of data needed for the player to make
    choices
    """
    def __init__(self, name=None, food_bag=0, hand=None, species=None, active=True):
        self.name = name
        self.food_bag = food_bag
        self.hand = hand if hand else []
        self.species = species if species else []
        self.active = active

    def __str__(self):
        return "PlayerState(Food=%d, Hand=%s, Species=%s" % (self.food_bag, self.hand, self.species)

    def __eq__(self, other):
        species_equal = True
        for spec in self.species:
            if len(self.species) != len(other.species):
                return False
            elif not other.species[self.species.index(spec)].equal_attributes(spec):
                species_equal = False
        return all([isinstance(other, PlayerState),
                    self.name == other.name,
                    self.food_bag == other.food_bag,
                    self.hand == other.hand,
                    species_equal])



    def get_left_neighbor(self, species):
        """
        Gets the left neighbor of the given Species in the list of species for this player
        :param species: Species of which to find neighbor
        :return: The Species to the left of the given Species
        """
        species_index = self.species.index(species)
        return False if species_index == 0 else self.species[species_index - 1]


    def get_right_neighbor(self, species):
        """
        Gets the right neighbor of the given Species in the list of species for this player
        :param species: Species of which to find neighbor
        :return: The Species to the right of the given Species
        """
        species_index = self.species.index(species)
        return False if species_index == len(self.species) - 1 else self.species[species_index + 1]

    def get_hungry_species(self, carnivores=False):
        """
        Gets any hungry species in this player's species in the desired group.
        :param carnivores: True if only carnivores are desired,
                            else False if only herbivores are desired
        :return: List of Species, Where species are hungry herbivores.
        """
        return [species for species in self.species
                if (CARNIVORE in species.trait_names() if carnivores else CARNIVORE not in species.trait_names()) and
                species.food < species.population]

    def get_needy_fats(self):
        """
        Gets any needy species that have a Fat-tissue trait.
        :return: List of Species, Where species fat-tissue is not full
        """
        return [species for species in self.species
                if FATTISSUE in species.trait_names() and
                species.fat_storage < species.body]

