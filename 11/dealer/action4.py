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
