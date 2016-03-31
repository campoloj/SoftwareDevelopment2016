class Action4(object):
    """
    Represents a players actions for a turn.
    """
    def __init__(self, player, actions):
        """
        Creates an Action4
        :param player: Player State of the player choosing actions
        :param actions: List of Actions the player is committing.
        :return:
        """
        self.player = player
        self.actions = actions

    def apply_all(self, dealer):
        """
        Applies each action to this dealer for this player and discards all the cards that need to be discarded.
        :param dealer: The dealer we are applying the actions to.
        :return:
        """
        discards = []
        for action in self.actions:
            discards += action.apply(dealer, self.player)

        self.player.discard_all(discards)
