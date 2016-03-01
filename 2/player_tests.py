import unittest
from player import *


class test_Player(unittest.TestCase):

    def setUp(self):
        self.card_4 = Card(face_value=4, bull=2)
        self.card_5 = Card(face_value=5, bull=3)
        self.card_6 = Card(face_value=6, bull=4)
        self.card_7 = Card(face_value=7, bull=4)
        self.card_8 = Card(face_value=8, bull=3)
        self.card_9 = Card(face_value=9, bull=2)
        self.card_10 = Card(face_value=10, bull=4)

        self.stack_1 = Stack([self.card_4])
        self.stack_2 = Stack([self.card_5])
        self.stack_3 = Stack([self.card_6, self.card_7])
        self.stack_4 = Stack([self.card_8])

        self.player_1 = Player(1)
        self.player_1.hand = [self.card_9, self.card_10]

        self.dealer = Dealer([self.player_1])
        self.dealer.list_of_stacks = [self.stack_1, self.stack_2, self.stack_3, self.stack_4]

    def test_discard_card(self):
        self.assertEqual(len(self.player_1.hand), 2)
        discard = self.player_1.discard_card()
        self.assertEqual(len(self.player_1.hand), 1)
        self.assertEqual(discard.face_value, 10)

    def test_select_stack(self):
        stack = self.player_1.select_stack(self.dealer)
        self.assertEqual(stack.total_bull, 2)

if __name__ == '__main__':
    unittest.main()