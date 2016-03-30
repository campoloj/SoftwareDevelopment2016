class Action4(object):
    """
    Represents a players actions for a turn.
    """
    def __init__(self, player, actions, dealer):
        """
        Creates an Action4
        :param player: Player State of the player choosing actions
        :param actions: List of Actions the player is committing.
        :param dealer: The dealer we are modifying.
        :return:
        """
        self.player = player
        self.actions = actions
        self.dealer = dealer

    def apply_all(self):
        """
        Applies each action to this dealer for this player and discards all the cards that need to be discarded.
        :return:
        """
        discards = []
        for action in self.actions:
            discards += action.apply(self.dealer, self.player)

        self.player.discard_all(discards)
