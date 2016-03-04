import unittest

from convert import Convert
from dealer.player import PlayerState
from dealer.species import Species
from dealer.traitcard import TraitCard
from dealer.globals import *
from dealer.dealer import Dealer


class TestConvert(unittest.TestCase):

    def setUp(self):
        self.jt_1 = CARNIVORE
        self.jt_2 = FATTISSUE
        self.jt_3 = BURROWING
        self.jt_4 = CLIMBING

        self.jSpecies_1 = [[FOOD, 2], [BODY, 2], [POPULATION, 2], [TRAITS, [self.jt_1]]]
        self.jSpecies_2 = [[FOOD, 2], [BODY, 3], [POPULATION, 3], [TRAITS, [self.jt_2]], [FATFOOD, 0]]
        self.jSpecies_3 = [[FOOD, 2], [BODY, 3], [POPULATION, 4], [TRAITS, [self.jt_3, self.jt_4]]]
        self.jSpecies_4 = [[FOOD, 2], [BODY, 2], [POPULATION, 2], [TRAITS, [self.jt_3, self.jt_4]]]

        self.jPlayer_1 = [[ID, 1], [SPECIES, [self.jSpecies_1]], [BAG, 2]]
        self.jPlayer_2 = [[ID, 2], [SPECIES, [self.jSpecies_2]], [BAG, 1]]
        self.jPlayer_3 = [[ID, 3], [SPECIES, [self.jSpecies_3, self.jSpecies_4]], [BAG, 3]]
        self.jPlayer_4 = [[ID, 2], [SPECIES, []], [BAG, 1]]


        self.json_feeding = [self.jPlayer_1, 10, [self.jPlayer_2, self.jPlayer_3]]
        self.json_feed_1 = False
        self.json_feed_2 = self.jSpecies_3
        self.json_feed_3 = [self.jSpecies_2, 3]
        self.json_feed_4 = [self.jSpecies_1, self.jPlayer_2, self.jSpecies_2]

        self.t_1 = TraitCard(CARNIVORE)
        self.t_2 = TraitCard(FATTISSUE)
        self.t_3 = TraitCard(BURROWING)
        self.t_4 = TraitCard(CLIMBING)

        self.species_1 = Species(2, 2, 2, [self.t_1])
        self.species_2 = Species(3, 2, 3, [self.t_2], 0)
        self.species_3 = Species(4, 2, 3, [self.t_3, self.t_4])
        self.species_4 = Species(2, 2, 2, [self.t_3, self.t_4])

        self.player_1 = PlayerState(name=1, food_bag=2, species=[self.species_1])
        self.player_2 = PlayerState(name=2, food_bag=1, species=[self.species_2])
        self.player_3 = PlayerState(name=3, food_bag=3, species=[self.species_3, self.species_4])
        self.player_4 = PlayerState(name=2, food_bag=1, species=[])

        self.feeding = [self.player_1, 10, [self.player_2, self.player_3]]
        self.feed_1 = False
        self.feed_2 = self.species_3
        self.feed_3 = [self.species_2, 3]
        self.feed_4 = [self.species_1, self.player_2, self.species_2]

        self.jSpecies_card1 = [2, WARNINGCALL]
        self.jSpecies_card2 = [5, CARNIVORE]
        self.jSpecies_card3 = [-3, BURROWING]
        self.jSpecies_card4 = [3, AMBUSH]
        self.jSpecies_card5 = [0, SCAVENGER]

        self.species_card1 = TraitCard(WARNINGCALL, 2)
        self.species_card2 = TraitCard(CARNIVORE, 5)
        self.species_card3 = TraitCard(BURROWING, -3)
        self.species_card4 = TraitCard(AMBUSH, 3)
        self.species_card5 = TraitCard(SCAVENGER, 0)

        self.jList_of_players = [self.jPlayer_1, self.jPlayer_4, self.jPlayer_3]
        self.jDeck = [self.jSpecies_card1, self.jSpecies_card2, self.jSpecies_card3,
                      self.jSpecies_card4, self.jSpecies_card5]
        self.jDealer = [self.jList_of_players, 12, self.jDeck]

        self.list_of_players = [self.player_1, self.player_4, self.player_3]
        self.deck = [self.species_card1, self.species_card2, self.species_card3,
                     self.species_card4, self.species_card5]

        self.dealer1 = Dealer(self.list_of_players, 12, self.deck)

    def test_json_to_trait(self):
        self.assertEqual(Convert.json_to_trait(self.jt_1), self.t_1)
        self.assertNotEqual(Convert.json_to_trait(self.jt_1), self.t_2)

    def test_trait_to_json(self):
        self.assertEqual(Convert.trait_to_json(self.t_1), self.jt_1)
        self.assertNotEqual(Convert.trait_to_json(self.t_1), self.jt_2)

    def test_json_to_species(self):
        self.assertTrue(Convert.json_to_species(self.jSpecies_1).equal_attributes(self.species_1))
        self.assertTrue(Convert.json_to_species(self.jSpecies_2).equal_attributes(self.species_2))
        self.assertFalse(Convert.json_to_species(self.jSpecies_1).equal_attributes(self.species_2))
        self.jSpecies_1[0][1] = -1
        self.assertRaises(AssertionError, Convert.json_to_species, self.jSpecies_1)

    def test_species_to_json(self):
        self.assertEqual(Convert.species_to_json(self.species_1), self.jSpecies_1)
        self.assertNotEqual(Convert.species_to_json(self.species_1), self.jSpecies_2)
        self.species_1.population = -1
        self.assertRaises(AssertionError, Convert.species_to_json, self.species_1)

    def test_json_to_player(self):
        self.assertTrue(Convert.json_to_player(self.jPlayer_1), self.player_1)
        self.assertNotEqual(Convert.json_to_player(self.jPlayer_1), self.player_2)
        self.jPlayer_1[0][1] = -1
        self.assertRaises(AssertionError, Convert.json_to_player, self.jPlayer_1)

    def test_player_to_json(self):
        self.assertEqual(Convert.player_to_json(self.player_1), self.jPlayer_1)
        self.assertNotEqual(Convert.player_to_json(self.player_1), self.jPlayer_2)
        self.player_1.food_bag = -1
        self.assertRaises(AssertionError, Convert.player_to_json, self.player_1)

    def test_json_to_feeding(self):
        self.assertEqual(Convert.json_to_feeding(self.json_feeding), self.feeding)

    def test_json_to_dealer(self):
        self.assertTrue(Convert.json_to_dealer(self.jDealer).equal_attributes(self.dealer1))

    def test_dealer_to_json(self):
        self.assertEquals(Convert.dealer_to_json(self.dealer1), self.jDealer)


if __name__ == '__main__':
    unittest.main()
