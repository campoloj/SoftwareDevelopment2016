import unittest
from species import Species
from traitcard import TraitCard
from player import Player
from player_state import PlayerState
from globals import *
from feeding_choice import *


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.species_1 = Species(4, 4, 4)
        self.species_2 = Species(4, 4, 4)
        self.species_3 = Species(4, 4, 3)
        self.species_4 = Species(4, 3, 3)
        self.species_5 = Species(3, 1, 3)
        self.species_6 = Species(4, 3, 3)
        self.species_7 = Species(4, 4, 4)
        self.species_list = [self.species_2, self.species_4, self.species_3, self.species_5, self.species_1]
        self.player_1 = PlayerState(species=[self.species_4, self.species_5, self.species_6])
        self.player_2 = PlayerState(species=[self.species_1])
        self.player_3 = PlayerState(species=[self.species_2, self.species_3, self.species_7])

    def test_sort_largest(self):
        sorted_list = [self.species_2, self.species_1, self.species_3, self.species_4, self.species_5]
        self.assertEqual(Player.sort_by_size(self.species_list), sorted_list)
        self.assertNotEqual(Player.sort_by_size(self.species_list), self.species_list)

    def test_largest_fatty_need(self):
        self.species_1.traits = self.species_2.traits = self.species_4.traits = [TraitCard(FATTISSUE)]
        self.species_1.fat_storage = self.species_2.fat_storage = self.species_4.fat_storage = 0
        self.assertEqual(Player.largest_fatty_need([self.species_1, self.species_4]), self.species_1)
        self.assertEqual(Player.largest_fatty_need([self.species_1, self.species_2]), self.species_1)

    def test_feed_herbivore(self):
        self.assertEqual(Player.feed_herbivores([self.species_4, self.species_5], self.player_1), HerbivoreFeeding(0))

    def test_feed_carnivore(self):
        self.species_4.traits = [TraitCard(CARNIVORE, 4)]
        self.species_5.traits = [TraitCard(CARNIVORE)]
        self.species_6.traits = [TraitCard(CARNIVORE)]

        # Test tie in largest carnivore in attacking player's hand => first species chosen
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_2, self.player_3]),
                         CarnivoreFeeding(0, 0, 0))

        # Repeat to test first is chosen again when order is changed
        self.player_1.species = [self.species_6, self.species_5, self.species_4]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_2, self.player_3]),
                         CarnivoreFeeding(0, 0, 0))

        # Test tie in largest target between defending players' hands => first given player chosen
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 0, 0))

        # Test tie in largest target within defending player's hand => first species chosen
        self.player_3.species = [self.species_7, self.species_3, self.species_2]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 0, 0))

        # Retest tie, but with first species unattackable => second largest chosen
        self.species_7.traits = [TraitCard(CLIMBING)]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 0, 2))

        # Repeat again, but since both largest in first player's hand are unattackable => second player w/ largest
        self.species_2.traits = [TraitCard(BURROWING)]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 1, 0))

        # Test that if all largest species are unattackable, a smaller species is chosen
        self.species_1.traits = [TraitCard(CLIMBING)]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 0, 1))

        # Test that a carnivore with overriding traits attacks the largest species attackable
        self.species_3.traits = [TraitCard(CLIMBING)]
        self.species_4.traits.append(TraitCard(CLIMBING))
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         CarnivoreFeeding(2, 0, 0))

    def test_next_feeding(self):
        self.species_4.traits = [TraitCard(CARNIVORE)]
        self.species_5.traits, self.species_5.fat_storage = ([TraitCard(FATTISSUE)], 0)
        # Test if fat_tissue_species
        self.assertEqual(Player.next_feeding(self.player_1, 10, [self.player_2, self.player_3]), FatFeeding(1, 3))
        # Test if hungry_herbivores
        self.species_5.traits = []
        self.assertEqual(Player.next_feeding(self.player_1, 10, [self.player_2]), HerbivoreFeeding(2))
        # Test if hungry_carnivore
        self.species_5.traits = [TraitCard(CARNIVORE)]
        self.species_6.traits = [TraitCard(CARNIVORE)]
        self.assertEqual(Player.next_feeding(self.player_1, 10, [self.player_2, self.player_3]),
                                             CarnivoreFeeding(0, 0, 0))
        # Test no attackable species
        self.assertEqual(Player.next_feeding(self.player_1, 10, []), NoFeeding())

    def test_show_changes(self):
        self.assertEquals(self.player_1.show_changes(self.player_2), 'Species 0: [[food, 3->4], [body, 3->4]]\n,'
                                                                     ' Species 1: [[population, 3->1], [body, 3->0]]\n,'
                                                                     ' Species 2: [[population, 4->1], [food, 3->0],'
                                                                     ' [body, 3->0]]\n')
        self.player_2.food_bag = 3
        self.player_2.active = False
        self.assertEquals(self.player_1.show_changes(self.player_2),
                          '[food_bag, 0->3], '
                          'Species 0: [[food, 3->4], [body, 3->4]]\n, '
                          'Species 1: [[population, 3->1], [body, 3->0]]\n, '
                          'Species 2: [[population, 4->1], [food, 3->0], [body, 3->0]]\n, '
                          '[active, True->False]')



if __name__ == '__main__':
    unittest.main()
