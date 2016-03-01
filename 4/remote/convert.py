import os
import sys
game_object_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..%s..%s2%stake5" % (os.sep, os.sep, os.sep))
sys.path.append(game_object_path)

from Assignment_2 import Card, Stack


class Conversions:
    def __init__(self):
        pass

    @staticmethod
    def convert_json_to_stack(json_stack):
        """
        Converts json formatted stacks into Stack objects
        :param json_stack: list of json cards
        :return: Stack object
        """
        list_of_cards = []
        for json_card in json_stack:
            card = Conversions.convert_json_to_card(json_card)
            list_of_cards.append(card)
        stack = Stack(list_of_cards)
        return stack

    @staticmethod
    def convert_stack_to_json(stack):
        """
        Converts Stack object to list of json cards
        :param stack: Stack object
        :return: list of json cards
        """
        json_stack = []
        for card in stack.list_of_cards:
            json_card = Conversions.convert_card_to_json(card)
            json_stack.append(json_card)
        return json_stack

    @staticmethod
    def convert_json_to_card(json_card):
        """
        Converts json card to Card object
        :param json_card: [int, int]
        :return: Card object
        """
        card = Card(json_card[0], json_card[1])
        return card

    @staticmethod
    def convert_card_to_json(card):
        """
        Converts Card object to json card
        :param card: Card object
        :return: [int, int]
        """
        json_card = [card.face_value, card.bull_points]
        return json_card