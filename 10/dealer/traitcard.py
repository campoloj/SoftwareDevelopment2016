from globals import *


class TraitCard(object):
    """
    Represents a TraitCard of the Evolution game
    """
    def __init__(self, trait, food_points=False):
        """
        Craates a TraitCard
        :param trait: String representing the name of the TraitCard
        :param food_points: Integer representing the food points of the TraitCard
        :return: a TraitCard object
        """
        self.trait = trait
        self.food_points = food_points

    def __eq__(self, other):
        return all([isinstance(other, TraitCard),
                    self.trait == other.trait,
                    self.food_points == other.food_points])

    @classmethod
    def validate_all_unique(cls, list_of_traitcard, total_deck):
        """
        Validates the uniqueness of all TraitCards in the given list.
        :param list_of_traitcard: a list of TraitCard objects to be validated
        :param total_deck: a list of TraitCards representing all valid card possibilities
        :raise ValueError if duplicate cards exist
        """
        for card in list_of_traitcard:
            card.validate_unique(total_deck)

    def validate_unique(self, total_deck):
        """
        Validates this TraitCard by checking that it exists in the given deck of possible cards
        :param total_deck: a list of TraitCards representing all valid card possibilities
        :raise ValueError if card is not valid / a duplicate
        """
        if self.food_points is not False:
            total_deck.remove(self)

    @classmethod
    def validate_all_attributes(cls, list_of_traitcard):
        """
        Validates the attributes of all TraitCards in the given list
        :param list_of_traitcard: a list of TraitCard objects to be validated
        :raise AssertionError if any card attributes are out of bounds
        """
        for card in list_of_traitcard:
            card.validate_attributes()

    def validate_attributes(self):
        """
        Validates the attributes of this TraitCard
        :raise AssertionError if attributes are out of game bounds
        """
        assert(isinstance(self.trait, basestring) and self.trait in TRAITS_LIST)
        if self.food_points is not False:
            assert(isinstance(self.food_points, int) and
                   (CARN_FOOD_MIN <= self.food_points <= CARN_FOOD_MAX if self.trait == CARNIVORE
                   else HERB_FOOD_MIN <= self.food_points <= HERB_FOOD_MAX))
