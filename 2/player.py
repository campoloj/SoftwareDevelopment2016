import random

deck_size = 104
bull_range = [2, 7]


class Card(object):
    """
    This class was not provided in the given interface but is necessary to implement
    a player object
    """
    def __init__(self, face_value, bull):
        self.face_value = face_value
        self.bull = bull


class Stack(object):
    """
    This class was not provided in the given interface but is necessary to implement
    a player object
    """
    def __init__(self, list_of_cards):
        self.list_of_cards = list_of_cards
        self.total_bull = sum([card.bull for card in self.list_of_cards])


class Player(object):
    def __init__(self, name):
        """
        Purpose Statement: creates a player object
        Ambiguity:
            The provided interface did not provide information about what attributes Player
            object should contain so we made assumptions based on the game specifications
        :param name: the name of the player
        :return: the player object
        """
        self.name = name
        self.bull_points = 0
        self.hand = []
        self.discard = None

    def discard_card(self):
        """
        Purpose Statement: The player will choose the card to discard
        Ambiguity:
            The provided interface defined discard_card as taking a card as an argument when
            it should instead return a card
        :return: the card to be discarded
        """
        high_card = None
        max_face = None
        for card in self.hand:
            if card.face_value > max_face:
                max_face = card.face_value
                high_card = card
        self.hand.remove(high_card)
        return high_card

    def select_stack(self, dealer):
        """
        Purpose Statement: The player selects the stack they wish to put in their hand
        Ambiguity:
            The player is only required to choose a stack in the case that their discard face value
            is lower than the face_value on the top card of all the stacks. This function should
            therefore not select the stack to put the card in but the stack to pick up in that case.
            This function must also take the dealer object which was not mentioned in order to provide
            the player with information about the stacks.
        :param dealer: the dealer object
        :return: the selected stack
        """
        stacks = dealer.list_of_stacks
        min_stack = stacks[0]
        for stack in stacks:
            if stack.total_bull < min_stack.total_bull:
                min_stack = stack
        return min_stack


class Dealer(object):
    """
    This class did not contain attributes in the given interface
    """
    def __init__(self, list_of_players):
        self.list_of_players = list_of_players
        deck = []
        for x in range(1, deck_size + 1):
            bull = random.choice(bull_range)
            card = Card(face_value=x, bull=bull)
            deck.append(card)
        self.deck = deck
        self.discards = {}
        self.list_of_stacks = []


