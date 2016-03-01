class Player(object):
    def __init__(self):
        self.hand = []

    def pick_discard(self):
        """
        Player selects card from hand to discard
        :return: card to discard
        """
        selected_card = self.hand[0]
        selected_face = selected_card.face_value
        for card in self.hand:
            if card.face_value < selected_face:
                selected_face = card.face_value
                selected_card = card
        self.hand.remove(selected_card)
        return selected_card

    def pick_stack(self, list_of_stacks):
        """
        Player selects stack to add to their hand
        :param dealer: the dealer object
        :return: index of stack to pick up
        """
        min_stack = list_of_stacks[0]
        for stack in list_of_stacks:
            if stack.total_bull < min_stack.total_bull:
                min_stack = stack
        return min_stack