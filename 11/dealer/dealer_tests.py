import unittest
from species import Species
from traitcard import TraitCard
from player_state import PlayerState
from globals import *
from dealer import Dealer
from action import *
from action4 import Action4
import copy


class TestDealer(unittest.TestCase):

    def setUp(self):
        # Traits (Trait, Food-value)
        self.carnivore = TraitCard(CARNIVORE, 3)
        self.burrowing = TraitCard(BURROWING, 2)
        self.fattissue = TraitCard(FATTISSUE, 2)
        self.foraging = TraitCard(FORAGING, 2)
        self.horns = TraitCard(HORNS, 0)
        self.cooperation = TraitCard(COOPERATION, 1)
        self.scavenger = TraitCard(SCAVENGER, 2)

        # Species (Population, Food, Body, Traits, Fat-Storage)
        self.species1 = Species(1, 0, 2, [self.cooperation])
        self.species2 = Species(6, 2, 1, [self.carnivore])
        self.species3 = Species(3, 3, 3, [self.fattissue], 0)
        self.species4 = Species(5, 5, 5, [self.burrowing])
        self.species5 = Species(5, 3, 4, [self.foraging])
        self.species6 = Species(2, 1, 7, [self.carnivore, self.fattissue, self.scavenger], 0)
        self.species7 = Species(7, 1, 6, [self.horns])

        self.player1_species = [self.species1, self.species2]
        self.player2_species = [self.species3, self.species4, self.species5]
        self.player3_species = [self.species6, self.species7]

        # Players (Name, Bag, Hand, Species)
        self.player1 = PlayerState(1, 0, [self.horns, self.foraging], self.player1_species)
        self.player2 = PlayerState(2, 3, [self.carnivore, self.fattissue], self.player2_species)
        self.player3 = PlayerState(3, 6, [self.burrowing], self.player3_species)

        self.public_player1 = PlayerState(1, False, False, self.player1_species)
        self.public_player2 = PlayerState(2, False, False, self.player2_species)
        self.public_player3 = PlayerState(3, False, False, self.player3_species)

        self.list_of_players = [self.player1, self.player2, self.player3]

        # Dealer (List of Players, Watering Hole, Deck)
        self.dealer1 = Dealer(self.list_of_players, 10, [])

        # Action
        self.action4_1 = Action4([FoodCardAction(1), GrowAction(POPULATION, 0, 0)])
        self.action4_2 = Action4([FoodCardAction(0), ReplaceTraitAction(1, 0, 1)])
        self.action4_3 = Action4([AddSpeciesAction(0, [])])
        self.action4_list = [self.action4_1, self.action4_2, self.action4_3]

    def test_make_deck(self):
        deck = Dealer.make_deck()
        self.assertEqual(len(deck), LOC_MAX)
        self.assertEqual(len(deck), len(set(deck)))

    def test_deal_cards(self):
        self.dealer1.deck = Dealer.make_deck()
        self.assertEqual([len(self.dealer1.deck), len(self.player1.hand)], [LOC_MAX, 2])
        self.dealer1.deal_cards(self.player1, 10)
        self.assertEqual([len(self.dealer1.deck), len(self.player1.hand)], [LOC_MAX - 10, 12])

    def test_public_players(self):
        public_players = self.dealer1.public_players(self.player1)
        self.assertTrue(public_players[0].equal_attributes(self.public_player2))
        self.assertTrue(public_players[1].equal_attributes(self.public_player3))

    def test_step4(self):
        old_dealer = copy.deepcopy(self.dealer1)
        self.dealer1.step4(self.action4_list)
        self.assertEqual(old_dealer.show_changes(self.dealer1),
                         'Player 1:removed cards: [horns, 0], [foraging, 2], '
                         'Species 0: [[population, 1->2], [food, 0->2]], '
                         'Species 1: [[food, 2->3]], '
                         'Player 2:removed cards: [carnivore, 3], [fat-tissue, 2], '
                         'Species 1: [[traits: [0, [burrowing, 2]->[fat-tissue, 2]]], [fat-tissue, False->5]], '
                         'Player 3:removed cards: [burrowing, 2], '
                         'Species 0: [[fat-tissue, 0->7]], '
                         'Species 2: New Species: [[food, 0], [body, 0], [population, 1], [traits, []]], '
                         '[watering_hole, 10->0]')

    # TODO deal with order being rearranged
    # def test_feed1(self):
    #     # Auto-feeding
    #     self.species3.fat_storage = 3
    #     self.dealer1.list_of_players, self.dealer1.watering_hole = ([self.player2, self.player1, self.player3], 20)
#
    #     self.assertEqual([self.species5.food, self.dealer1.watering_hole], [3, 20])
    #     self.dealer1.feed1()
    #     self.assertEqual([self.species5.food, self.dealer1.watering_hole], [5, 18])
#
    #     # NoFeeding
    #     self.assertTrue(self.player2.active)
    #     self.dealer1.feed1()
    #     self.assertEqual([self.species5.food, self.dealer1.watering_hole, self.player2.active], [5, 18, False])
#
    #     # HerbivoreFeeding
    #     self.species2.traits.pop()
    #     self.dealer1.list_of_players = [self.player1, self.player2, self.player3]
    #     self.assertEqual([self.species1.food, self.species2.food, self.dealer1.watering_hole, self.player1.active],
    #                      [0, 2, 18, True])
    #     self.dealer1.feed1()
    #     self.assertEqual([self.species1.food, self.species2.food, self.dealer1.watering_hole, self.player1.active],
    #                      [0, 3, 17, True])
#
    #     # FatFeeding
    #     self.dealer1.list_of_players = [self.player3, self.player2, self.player1]
    #     self.assertEqual([self.species6.fat_storage, self.dealer1.watering_hole], [0, 17])
    #     self.dealer1.feed1()
    #     self.assertEqual([self.species6.fat_storage, self.dealer1.watering_hole], [7, 10])
#
    #     # CarnivoreFeeding
    #     self.species7.traits.append(self.carnivore)
    #     self.assertEqual([self.species2.population, self.species7.food, self.species6.food, self.dealer1.watering_hole],
    #                      [6, 1, 1, 10])
    #     self.dealer1.feed1()
    #     self.assertEqual([self.species2.population, self.species7.food, self.species6.food, self.dealer1.watering_hole],
    #                      [5, 2, 2, 8])

    def test_feed_species(self):
        # Regular Feeding
        self.assertEqual([self.species2.food, self.dealer1.watering_hole], [2, 10])
        self.dealer1.feed_species(self.species2, self.player1)
        self.assertEqual([self.species2.food, self.dealer1.watering_hole], [3, 9])

        # Cooperation Feeding
        self.assertEqual(self.species1.food, 0)
        self.dealer1.feed_species(self.species1, self.player1)
        self.assertEqual([self.species1.food, self.species2.food, self.dealer1.watering_hole], [1, 4, 7])

        # Foraging and Cooperation
        self.species1.population, self.species1.food = (3, 0)
        self.species1.traits.append(self.foraging)

        self.dealer1.feed_species(self.species1, self.player1)
        self.assertEqual([self.species1.food, self.species2.food, self.dealer1.watering_hole], [2, 6, 3])

        # Cooperation Chain / Watering Hole runs out
        self.player1.species.append(self.species5)
        self.species2.food, self.species2.traits, self.dealer1.watering_hole = (4, [self.cooperation, self.foraging], 4)

        self.dealer1.feed_species(self.species1, self.player1)
        self.assertEqual([self.species1.food, self.species2.food, self.species5.food, self.dealer1.watering_hole],
                         [3, 6, 4, 0])

    def test_handle_attack_situation(self):
        # Regular Attack
        self.assertEqual([self.species3.population, self.species3.food], [3, 3])
        self.dealer1.handle_attack_situation(self.species2, self.species3, self.player1, self.player2)
        self.assertEqual([self.species3.population, self.species3.food], [2, 2])

        # Horns
        self.assertEqual([self.species2.population, self.species7.population], [6, 7])
        self.dealer1.handle_attack_situation(self.species2, self.species7, self.player1, self.player3)
        self.assertEqual([self.species2.population, self.species7.population], [5, 6])

        # Double Extinction
        self.species2.population = 1
        self.species7.population = 1
        self.dealer1.deck = [self.foraging, self.scavenger, self.cooperation]
        self.dealer1.handle_attack_situation(self.species2, self.species7, self.player1, self.player3)
        self.assertEqual([self.species2.population, self.species7.population, self.player1.hand, self.player3.hand,
                          self.dealer1.deck],
                         [0, 0, [self.horns, self.foraging, self.cooperation],
                          [self.burrowing, self.foraging, self.scavenger], []])
        self.assertFalse(self.species2 in self.player1.species)
        self.assertFalse(self.species7 in self.player3.species)

    def test_handle_scavenging(self):
        # Regular
        self.assertEqual([self.species6.food, self.dealer1.watering_hole], [1, 10])
        self.dealer1.handle_scavenging()
        self.assertEqual([self.species6.food, self.dealer1.watering_hole], [2, 9])

        # Foraging
        self.species6.population, self.species6.traits[0] = (6, self.foraging)
        self.dealer1.handle_scavenging()
        self.assertEqual([self.species6.food, self.dealer1.watering_hole], [4, 7])

        # Cooperation
        self.species6.traits[1] = self.cooperation
        self.assertEqual([self.species6.food, self.species7.food, self.dealer1.watering_hole], [4, 1, 7])
        self.dealer1.handle_scavenging()
        self.assertEqual([self.species6.food, self.species7.food, self.dealer1.watering_hole], [6, 3, 3])

    def test_show_changes(self):
        old_dealer = copy.deepcopy(self.dealer1)
        self.dealer1.feed1()
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 1:'
                            'Species 0: [[food, 0->1]], '
                            'Species 1: [[food, 2->3]], '
                          '[watering_hole, 10->8]')


if __name__ == '__main__':
    unittest.main()
