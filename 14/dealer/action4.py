class Action4(object):
    """
    Represents a players actions for a turn.
    """
    def __init__(self, food_card, grow_pop=False, grow_body=False, add_species=False, replace_trait=False):
        """
        Creates an Action4
        :param food_card: FoodCardAction
        :param grow_pop: List of GrowAction with a population attribute
        :param grow_body: List of GrowAction with a body attribute
        :param add_species: List of AddSpeciesActions with a population attribute
        :param replace_trait: List of ReplaceTraitActions
        :return: Action4
        """
        self.food_card = food_card
        self.grow_pop = grow_pop if grow_pop else []
        self.grow_body = grow_body if grow_body else []
        self.add_species = add_species if add_species else []
        self.replace_trait = replace_trait if replace_trait else []

    def __eq__(self, other):
        return all([isinstance(other, Action4),
                    self.food_card == other.food_card,
                    self.grow_pop == other.grow_pop,
                    self.grow_body == other.grow_body,
                    self.add_species == other.add_species,
                    self.replace_trait == other.replace_trait])

    def apply_all(self, dealer, player):
        """
        Applies each action to this dealer for this player and discards all the cards that need to be discarded.
        :param dealer: The Dealer we are applying the actions to.
        :param player: Player State of the player choosing actions
        """
        discards = []
        for action in self.get_all_actions():
            discards += action.apply(dealer, player)

        dealer.watering_hole = max(0, dealer.watering_hole)
        player.discard_all(discards)

    def get_all_actions(self):
        """
        Returns a list of all the actions in this action4 in the order they should be executed
        :return: List of Action
        """
        return [self.food_card] + self.add_species + self.grow_pop + self.grow_body + self.replace_trait

    def validate_hand(self, player):
        """
        Validates that each index into their hand requested by a player is unique and within bounds
        :param player: the PlayerState of the acting player
        :raise AssertionError of invalid indices requested
        """
        hand_indices = self.requested_hand_indices()
        assert(len(hand_indices) <= len(player.hand))
        assert(len(set(hand_indices)) == len(hand_indices))
        for index in hand_indices:
            assert(0 <= index < len(player.hand))

    def requested_hand_indices(self):
        """
        Returns all the indices into the given list attribute as requested by the PlayerState for this Action4
        :return: {String: List of Nat or Tuple} representing list attribute names mapped to
                  indices into the list attribute (tuple represents (species_index trait_index))
        """
        hand_indices = []
        for action in self.get_all_actions():
            hand_indices += action.requested_hand_indices()
        return hand_indices

    def convert_to_json(self):
        """
        Converts this Action4 into its respective JSON representation
        :return: Action4 as specified in http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        return [self.food_card.convert_to_json(),
                [gp.convert_to_json() for gp in self.grow_pop],
                [gb.convert_to_json() for gb in self.grow_body],
                [add_spec.convert_to_json() for add_spec in self.add_species],
                [rt.convert_to_json() for rt in self.replace_trait]]