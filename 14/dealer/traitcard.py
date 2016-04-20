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

    def __ne__(self, other):
        return not self.__eq__(other)

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

    def trait_to_json(self):
        """
        Converts a TraitCard into a JSON Trait or SpeciesCard
        :param trait_card: a TraitCard object
        :return: a JSON Trait or SpeciesCard as specified by the data definitions at
                 http://www.ccs.neu.edu/home/matthias/4500-s16/5.html and
                 http://www.ccs.neu.edu/home/matthias/4500-s16/8.html, respectively.
        """
        return '[%s, %d]' % (self.trait, self.food_points)

    @classmethod
    def show_all_changes(cls, traitcards_before, traitcards_after):
        """
        Creates a string representation of the changed attributes between a list of TraitCards before and after
        an imperative function is called on it.
        :param traitcards_before: List of TraitCard before modification
        :param traitcards_after: List of TraitCard after modification
        :return: String of attribute changes, or "" if unchanged.
        """
        if len(traitcards_before) < len(traitcards_after):
            new_cards = [CARD_TEMPLATE % (card.trait, card.food_points) for card in traitcards_after
                         if card not in traitcards_before]
            return "new cards: %s" % ", ".join(new_cards)
        elif len(traitcards_before) > len(traitcards_after):
            removed_cards = [CARD_TEMPLATE % (card.trait, card.food_points) for card in traitcards_before
                             if card not in traitcards_after]
            return "removed cards: %s" % ", ".join(removed_cards)
        else:
            changed_cards = []
            for i in range(len(traitcards_before)):
                before, after = (traitcards_before[i], traitcards_after[i])
                if before != after:
                    changed_cards.append(CHANGE_TEMPLATE % (str(i), CARD_TEMPLATE % (before.trait, before.food_points),
                                                            CARD_TEMPLATE % (after.trait, after.food_points)))
            return ", ".join(changed_cards) if changed_cards else ""