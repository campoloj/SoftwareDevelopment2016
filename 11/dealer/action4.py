class Action4(object):
    """
    Represents a players actions for a turn.
    """
    def __init__(self, actions):
        """
        Creates an Action4
        :param actions: List of Actions the player is committing.
        :return:
        """
        self.actions = actions

    def apply_all(self, dealer, player):
        """
        Applies each action to this dealer for this player and discards all the cards that need to be discarded.
        :param dealer: The Dealer we are applying the actions to.
        :param player: Player State of the player choosing actions
        :return:
        """
        discards = []
        for action in self.actions:
            discards += action.apply(dealer, player)

        dealer.watering_hole = max(0, dealer.watering_hole)
        player.discard_all(discards)

    def validate_all_indices(self, player):
        """
        Validates that all the indices requested by the given PlayerState for this Action4
        :param player: the PlayerState of the acting player
        :raise AssertionError of invalid indices requested
        """
        self.validate_indices("hand", player)
        self.validate_indices("species", player)

    def validate_indices(self, list_attr, player):
        """
        Validates that each index requested by a player for the given list attribute is unique and within bounds
        :param list_attr: One of:
                            - "hand"
                            - "species"
        :param player: the PlayerState of the acting player
        :raise AssertionError of invalid indices requested
        """
        requested_indices = self.requested_indices(list_attr)
        player_list_attr = (player.hand if list_attr == "hand" else player.species)
        assert(len(requested_indices) <= len(player_list_attr))
        assert(len(set(requested_indices)) == len(requested_indices))
        for index in requested_indices:
            assert(0 <= index < len(player_list_attr))

    def requested_indices(self, list_attr):
        """
        Returns all the indices into the given list attribute as requested by the PlayerState for this Action4
        :param list_attr: One of:
                            - "hand"
                            - "species"
        :return: List of Nat representing indices into a specified list
        """
        indices = []
        for action in self.actions:
            indices += action.requested_indices(list_attr)
        return indices
