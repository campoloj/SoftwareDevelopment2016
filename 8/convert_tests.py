import unittest

from convert import Convert
from dealer import player_state
from dealer import species
from dealer import traitcard


class TestConvert(unittest.TestCase):

    def setUp(self):
        self.jt_1 = "carnivore"
        self.jt_2 = "fat-tissue"
        self.jt_3 = "burrowing"
        self.jt_4 = "climbing"

        self.jSpecies_1 = [["food", 2], ["body", 2], ["population", 2], ["traits", [self.jt_1]]]
        self.jSpecies_2 = [["food", 2], ["body", 3], ["population", 3], ["traits", [self.jt_2]], ["fat-food", 0]]
        self.jSpecies_3 = [["food", 2], ["body", 3], ["population", 4], ["traits", [self.jt_3, self.jt_4]]]
        self.jSpecies_4 = [["food", 2], ["body", 2], ["population", 2], ["traits", [self.jt_3, self.jt_4]]]

        self.jPlayer_1 = [["id", 1], ["species", [self.jSpecies_1]], ["bag", 2]]
        self.jPlayer_2 = [["id", 2], ["species", [self.jSpecies_2]], ["bag", 1]]
        self.jPlayer_3 = [["id", 3], ["species", [self.jSpecies_3, self.jSpecies_4]], ["bag", 3]]

        self.json_feeding = [self.jPlayer_1, 10, [self.jPlayer_2, self.jPlayer_3]]
        self.json_feed_1 = False
        self.json_feed_2 = self.jSpecies_3
        self.json_feed_3 = [self.jSpecies_2, 3]
        self.json_feed_4 = [self.jSpecies_1, self.jPlayer_2, self.jSpecies_2]

        self.t_1 = traitcard.TraitCard("carnivore")
        self.t_2 = traitcard.TraitCard("fat-tissue")
        self.t_3 = traitcard.TraitCard("burrowing")
        self.t_4 = traitcard.TraitCard("climbing")

        self.species_1 = species.Species(2, 2, 2, [self.t_1])
        self.species_2 = species.Species(3, 2, 3, [self.t_2], 0)
        self.species_3 = species.Species(4, 2, 3, [self.t_3, self.t_4])
        self.species_4 = species.Species(2, 2, 2, [self.t_3, self.t_4])

        self.player_1 = player_state.PlayerState(name=1, food_bag=2, species=[self.species_1])
        self.player_2 = player_state.PlayerState(name=2, food_bag=1, species=[self.species_2])
        self.player_3 = player_state.PlayerState(name=3, food_bag=3, species=[self.species_3, self.species_4])

        self.feeding = [self.player_1, 10, [self.player_2, self.player_3]]
        self.feed_1 = False
        self.feed_2 = self.species_3
        self.feed_3 = [self.species_2, 3]
        self.feed_4 = [self.species_1, self.player_2, self.species_2]

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

if __name__ == '__main__':
    unittest.main()
