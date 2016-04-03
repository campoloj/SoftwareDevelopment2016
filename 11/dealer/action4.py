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
        for action in self.actions:
            hand_indices += action.requested_hand_indices()
        return hand_indices