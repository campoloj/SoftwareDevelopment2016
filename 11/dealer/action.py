class Action(object):
    """
    Represents a player action which includes information on what the player wishes to do with each card
    such as submitting to the watering whole, growing species attributes, creating new species, or replacing traits
    """
    def __init__(self):
        pass

    def apply(self, dealer, player):
        """
        Updates the Dealer configuration according to the Action for this PlayerState
        :param dealer: the Dealer object
        :param player: the PlayerState of the Player choosing their action
        :return: List of Nat representing indecies of TraitCards that this PlayerState must discard
        """
        return NotImplemented


class FoodCardAction(Action):
    """
    Represents an action of submitting a TraitCard to be used as food on the watering hole.
    """
    def __init__(self, trait_card_index):
        """
        Creates a FoodCardAction
        :param trait_card_index: Natural that represents the index in the players hand of the card to be placed.
        :return: FoodCardAction
        """
        super(FoodCardAction, self).__init__()
        self.trait_card_index = trait_card_index

    def apply(self, dealer, player):
        """
        :effect Adds the food value of the specified Trait Card to the watering hole
        :param dealer: Dealer being modified
        :param player: Player choosing this action
        :return: List of Nat representing indecies of TraitCards that this PlayerState must discard
        """
        dealer.watering_hole += player.hand[self.trait_card_index].food_points
        return [self.trait_card_index]


class GrowAction(Action):
    """
    Represents an action of growing the population of a species in the players hand.
    """
    def __init__(self, attribute, species_board_index, trait_card_index):
        """
        Creates a GrowPopAction
        :param attribute: One of:
                            - "body"
                            - "population"
        :param species_board_index: Natural that represents the index of the species board in the player's Species that
                                    the action is applied to.
        :param trait_card_index: Natural that represents the index in the players hand of the card to be traded.
        :return: GrowPopAction
        """
        super(GrowAction, self).__init__()
        self.attribute = attribute
        self.species_board_index = species_board_index
        self.trait_card_index = trait_card_index

    def apply(self, dealer, player):
        """
        :effect Adds 1 to specified attribute of the Species.
        :param dealer: Dealer being modified
        :param player: Player choosing this action
        :return: List of Nat representing indecies of TraitCards that this PlayerState must discard
        """
        player.grow_attribute(self)
        return [self.trait_card_index]


class AddSpeciesAction(Action):
    """
    Represents an action of adding a new Species to the PlayerState's hand.
    """
    def __init__(self, trade_card_index, add_card_list):
        """
        Creates an AddSpeciesAction
        :param trade_card_index: Nat representing the index of the Trait Card in the players hand to discard.
        :param add_card_list: List of Nat representing the indicies of Trait Cards in the players hand to add to the
                              new species. This list can be up to length of 3.
        :return: AddSpeciesAction
        """
        super(AddSpeciesAction, self).__init__()
        self.trade_card_index = trade_card_index
        self.add_card_list = add_card_list

    def apply(self, dealer, player):
        """
        :effect Adds a new Species to the right of the player's current Species with the
                specified Trait Cards from the hand.
        :param dealer: Dealer being modified
        :param player: Player choosing this action
        :return: List of Nat representing indecies of TraitCards that this PlayerState must discard
        """
        player.add_species(self.add_card_list)
        self.add_card_list.append(self.trade_card_index)
        return self.add_card_list


class ReplaceTraitAction(Action):
    """
    Represents an action of replacing a TraitCard on one of the PlayerState's Species
    """
    def __init__(self, species_board_index, card_to_replace_index, replacement_card_index):
        """
        Creates a ReplaceTraitAction
        :param species_board_index: Nat representing the index into the PlayerState's species boards
        :param card_to_replace_index: Nat representing the index into the Species's traits
        :param replacement_card_index: Nat representing the index into the PlayerState's hand
        :return: A ReplaceTraitAction
        """
        super(ReplaceTraitAction, self).__init__()
        self.species_board_index = species_board_index
        self.card_to_replace_index = card_to_replace_index
        self.replacement_card_index = replacement_card_index

    def apply(self, dealer, player):
        """
        :effect Replaces the specified TraitCard on the specified Species with the PlayerState's replacement TraitCard
        :param dealer: Dealer being modified
        :param player: Player choosing this action
        :return: List of Nat representing indecies of TraitCards that this PlayerState must discard
        """
        player.replace_trait(self)
        return [self.replacement_card_index]