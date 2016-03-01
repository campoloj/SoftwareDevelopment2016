import unittest
from Assignment_2 import Card, Stack, Dealer, Player


class Test_Assignment_2(unittest.TestCase):

    def setUp(self):
        self.card_8 = Card(face_value=8, bull=3)
        self.card_9 = Card(face_value=9, bull=2)
        self.card_10 = Card(face_value=10, bull=4)

        self.stack_1 = Stack([self.card_8, self.card_9])

        self.player_1 = Player(1)
        self.player_2 = Player(2)

        self.dealer = Dealer([self.player_1, self.player_2])

    def test_card(self):
        self.assertEqual(self.card_10.face_value, 10)
        self.assertEqual(self.card_10.bull, 4)

    def test_stack(self):
        self.assertEqual(self.stack_1.list_of_cards, [self.card_8, self.card_9])
        self.assertEqual(self.stack_1.total_bull, 5)

    def test_make_deck(self):
        self.dealer.make_deck()
        self.assertEqual(len(self.dealer.deck), 104)
        for card in self.dealer.deck:
            self.assertIn(card.face_value, range(1, 105))
            self.assertIn(card.bull, range(2, 8))

    def test_deal(self):
        self.dealer.make_deck()
        self.dealer.deal()
        for player in self.dealer.list_of_players:
            self.assertEqual(len(player.hand), 10)
        self.assertEqual(len(self.dealer.deck), 84)

    def test_create_stacks(self):
        self.dealer.make_deck()
        self.dealer.deal()
        self.dealer.create_initial_stacks()
        self.assertEqual(len(self.dealer.deck), 80)
        self.assertEqual(len(self.dealer.list_of_stacks), 4)
        for stack in self.dealer.list_of_stacks:
            self.assertEqual(len(stack.list_of_cards), 1)

    def test_collect_discards(self):
        print("Cannot test collecting player discards until Player is fully implemented")
        pass

    def test_add_to_stack(self):
        self.assertEqual(len(self.stack_1.list_of_cards), 2)
        self.assertEqual(self.stack_1.total_bull, 5)
        self.stack_1 = self.dealer.add_to_stack(self.card_10, self.stack_1)
        self.assertEqual(len(self.stack_1.list_of_cards), 3)
        self.assertEqual(self.stack_1.total_bull, 9)
        self.assertIn(self.card_10, self.stack_1.list_of_cards)

    def test_subtract_bull(self):
        self.assertEqual(self.player_1.bull_points, 0)
        self.dealer.subtract_bull(self.player_1, self.stack_1)
        self.assertEqual(self.player_1.bull_points, -5)

    def test_add_to_hand(self):
        self.assertEqual(len(self.player_1.hand), 0)
        self.dealer.add_to_hand(self.player_1, self.stack_1)
        self.assertEqual(len(self.player_1.hand), 2)
        for card in self.stack_1.list_of_cards:
            self.assertIn(card, self.player_1.hand)

    def test_fix_stacks(self):
        print("Cannot test collecting player discards until Player is fully implemented")
        pass

    def test_find_winner(self):
        self.assertIsNone(self.dealer.find_winner())
        self.dealer.list_of_players[0].bull_points -= 70
        self.assertEqual(self.dealer.find_winner(), [(2, 0), (1, -70)])

if __name__ == '__main__':
    unittest.main()