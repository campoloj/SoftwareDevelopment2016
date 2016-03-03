import unittest
from species import Species
from traitcard import TraitCard
from player import Player
from player_state import PlayerState
from globals import *
from dealer import Dealer
'''
species (self, population=1, food=0, body=0, traits=None, fat_storage=None):
'''

class TestDealer(unittest.TestCase):

    def setUp(self):
        self.carnivore_trait = TraitCard(CARNIVORE, 3)
        self.burrowing_trait = TraitCard(BURROWING, 2)
        self.fattissue_trait = TraitCard(FATTISSUE, 4)

        self.species1 = Species(1, 0, 2, [])
        self.species2 = Species(6, 2, 1, [self.carnivore_trait])
        self.species3 = Species(3, 3, 3, [self.fattissue_trait], 0)
        self.species4 = Species(5, 5, 5, [self.burrowing_trait])
        self.species5 = Species(5, 3, 4, [])
        self.species6 = Species(2, 1, 7, [self.carnivore_trait, self.fattissue_trait], 0)
        self.species7 = Species(7, 1, 6, [])

        self.player1_species = [self.species1, self.species2]
        self.player2_species = [self.species3, self.species4, self.species5]
        self.player3_species = [self.species6, self.species7]

        self.player1 = PlayerState(1, 0, [], self.player1_species)
        self.player2 = PlayerState(2, 3, [self.carnivore_trait, self.fattissue_trait], self.player2_species)
        self.player3 = PlayerState(3, 6, [self.burrowing_trait], self.player3_species)

        self.public_player1 = PlayerState(1, None, None, self.player1_species)
        self.public_player2 = PlayerState(2, None, None, self.player2_species)
        self.public_player3 = PlayerState(3, None, None, self.player3_species)

        self.list_of_players = [self.player1, self.player2, self.player3]

        self.dealer1 = Dealer(self.list_of_players, 10, [])

    def test_public_players(self):
        self.assertEquals(self.dealer1.get_public_players(1), [self.public_player2, self.public_player3])
        self.assertEquals(self.dealer1.get_public_players(2), [self.public_player1, self.public_player3])
        self.assertEquals(self.dealer1.get_public_players(3), [self.public_player1, self.public_player2])
        self.assertEquals(self.dealer1.get_public_players(),
                          [self.public_player1, self.public_player2, self.public_player3])

    def test_any_attackers(self):
        self.assertTrue(self.dealer1.any_attackers([self.species2, self.species6]))
        self.assertTrue(self.dealer1.any_attackers([self.species6]))
        self.assertTrue(self.dealer1.any_attackers([self.species2]))
        self.dealer1.list_of_players[1].species = [self.species4]
        self.dealer1.list_of_players[2].species = []
        self.dealer1.list_of_players[0].species = [self.species2, self.species6]
        self.assertTrue(self.dealer1.any_attackers([self.species2, self.species6]))
        self.dealer1.list_of_players[0].species = [self.species2]
        self.assertFalse(self.dealer1.any_attackers([self.species2]))

    def test_handle_feed_result(self):
        # Herbivore Feeding
        self.assertEquals(self.species1.food, 0)
        self.assertEquals(self.dealer1.watering_hole, 10)
        self.dealer1.handle_feed_result(0, self.player1)
        self.assertEquals(self.species1.food, 1)
        self.assertEquals(self.dealer1.watering_hole, 9)
        # Carnivore Feeding
        self.assertEquals(self.species2.food, 2)
        self.assertEquals(self.species3.population, 3)
        self.dealer1.handle_feed_result([1, 1, 0], self.player1)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.dealer1.watering_hole, 8)
        self.assertEquals(self.species3.population, 2)
        # Check extinction
        self.assertEquals(self.species1.population, 1)
        self.assertTrue(self.species1 in self.player1.species)
        self.dealer1.handle_feed_result([1, 0, 0], self.player1)
        self.assertEquals(self.species2.food, 4)
        self.assertEquals(self.dealer1.watering_hole, 7)
        self.assertFalse(self.species1 in self.player1.species)
        # Fat Feeding
        self.assertEquals(self.species3.food, 3)
        self.assertEquals(self.species3.fat_storage, 0)
        self.assertEquals(self.species3.population, 2)
        self.dealer1.handle_feed_result([0, 2], self.player2)
        self.assertEquals(self.species3.food, 3)
        self.assertEquals(self.species3.fat_storage, 2)
        self.assertEquals(self.species3.population, 2)
        self.assertEquals(self.dealer1.watering_hole, 5)

    def test_feed1(self):
        self.assertEquals(self.dealer1.watering_hole, 10)
        self.assertEquals(self.species1.food, 0)
        self.dealer1.feed1(self.player1)
        self.assertEquals(self.species1.food, 1)
        self.assertEquals(self.dealer1.watering_hole, 9)
        self.assertEquals(self.species2.food, 2)
        self.assertEquals(self.species7.population, 7)
        self.dealer1.feed1(self.player1)
        self.assertEquals(self.species2.food, 3)
        self.assertEquals(self.dealer1.watering_hole, 8)
        self.assertEquals(self.species7.population, 6)









if __name__ == '__main__':
    unittest.main()
