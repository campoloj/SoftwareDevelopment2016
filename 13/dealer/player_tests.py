import unittest
from species import Species
from traitcard import TraitCard
from player import Player
from player_state import PlayerState
from globals import *
from feeding_choice import *
from action4 import Action4
from action import *


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.species_1 = Species(4, 4, 4)
        self.species_2 = Species(4, 4, 4)
        self.species_3 = Species(4, 4, 3)
        self.species_4 = Species(4, 3, 3)
        self.species_5 = Species(3, 1, 3)
        self.species_6 = Species(4, 3, 3)
        self.species_7 = Species(4, 4, 4)

        self.ambush_1 = TraitCard(AMBUSH, 1)
        self.ambush_3 = TraitCard(AMBUSH, 3)
        self.foraging_0 = TraitCard(FORAGING, 0)
        self.carnivore_7 = TraitCard(CARNIVORE, 7)
        self.carnivore_neg7 = TraitCard(CARNIVORE, -7)
        self.longneck_neg2 = TraitCard(LONGNECK, -2)
        self.scavenger_neg3 = TraitCard(SCAVENGER, -3)

        self.species_list = [self.species_2, self.species_4, self.species_3, self.species_5, self.species_1]
        self.ext_player1 = Player()
        self.player_1 = PlayerState(species=[self.species_4, self.species_5, self.species_6],
                                    ext_player=self.ext_player1)
        self.ext_player1.player_state = self.player_1
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
        self.assertEqual(self.ext_player1.feed_herbivores([self.species_4, self.species_5]), HerbivoreFeeding(0))

    def test_feed_carnivore(self):
        self.species_4.traits = [TraitCard(CARNIVORE, 4)]
        self.species_5.traits = [TraitCard(CARNIVORE)]
        self.species_6.traits = [TraitCard(CARNIVORE)]

        # Test tie in largest carnivore in attacking player's hand => first species chosen
        self.assertEqual(self.ext_player1.feed_carnivore(self.player_1.species, [self.player_2, self.player_3]),
                         CarnivoreFeeding(0, 0, 0))

        # Repeat to test first is chosen again when order is changed
        self.player_1.species = [self.species_6, self.species_5, self.species_4]
        self.assertEqual(self.ext_player1.feed_carnivore(self.player_1.species, [self.player_2, self.player_3]),
                         CarnivoreFeeding(0, 0, 0))

        # Test tie in largest target between defending players' hands => first given player chosen
        self.assertEqual(self.ext_player1.feed_carnivore(self.player_1.species, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 0, 0))

        # Test tie in largest target within defending player's hand => first species chosen
        self.player_3.species = [self.species_7, self.species_3, self.species_2]
        self.assertEqual(self.ext_player1.feed_carnivore(self.player_1.species, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 0, 0))

        # Retest tie, but with first species unattackable => second largest chosen
        self.species_7.traits = [TraitCard(CLIMBING)]
        self.assertEqual(self.ext_player1.feed_carnivore(self.player_1.species, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 0, 2))

        # Repeat again, but since both largest in first player's hand are unattackable => second player w/ largest
        self.species_2.traits = [TraitCard(BURROWING)]
        self.assertEqual(self.ext_player1.feed_carnivore(self.player_1.species, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 1, 0))

        # Test that if all largest species are unattackable, a smaller species is chosen
        self.species_1.traits = [TraitCard(CLIMBING)]
        self.assertEqual(self.ext_player1.feed_carnivore(self.player_1.species, [self.player_3, self.player_2]),
                         CarnivoreFeeding(0, 0, 1))

        # Test that a carnivore with overriding traits attacks the largest species attackable
        self.species_3.traits = [TraitCard(CLIMBING)]
        self.species_4.traits.append(TraitCard(CLIMBING))
        self.assertEqual(self.ext_player1.feed_carnivore(self.player_1.species, [self.player_3, self.player_2]),
                         CarnivoreFeeding(2, 0, 0))

    def test_next_feeding(self):
        self.species_4.traits = [TraitCard(CARNIVORE)]
        self.species_5.traits, self.species_5.fat_storage = ([TraitCard(FATTISSUE)], 0)
        # Test if fat_tissue_species
        self.assertEqual(self.ext_player1.next_feeding(self.player_1, 10, [self.player_2, self.player_3]), FatFeeding(1, 3))
        # Test if hungry_herbivores
        self.species_5.traits = []
        self.assertEqual(self.ext_player1.next_feeding(self.player_1, 10, [self.player_2]), HerbivoreFeeding(2))
        # Test if hungry_carnivore
        self.species_5.traits = [TraitCard(CARNIVORE)]
        self.species_6.traits = [TraitCard(CARNIVORE)]
        self.assertEqual(self.ext_player1.next_feeding(self.player_1, 10, [self.player_2, self.player_3]),
                                             CarnivoreFeeding(0, 0, 0))
        # Test no attackable species
        self.assertEqual(self.ext_player1.next_feeding(self.player_1, 10, []), None)

    def test_show_changes(self):
        self.assertEquals(self.player_1.show_changes(self.player_2), 'Species 0: [[food, 3->4], [body, 3->4]], '
                                                                     'Species 1: Species removed, '
                                                                     'Species 2: Species removed')
        self.player_2.food_bag = 3
        self.player_2.active = False
        self.assertEquals(self.player_1.show_changes(self.player_2),
                          '[food_bag, 0->3], '
                          'Species 0: [[food, 3->4], [body, 3->4]], '
                          'Species 1: Species removed, '
                          'Species 2: Species removed, '
                          '[active, True->False]')
        self.assertEquals(self.player_2.show_changes(self.player_1),
                          "[food_bag, 3->0], "
                          "Species 0: [[food, 4->3], [body, 4->3]], "
                          "Species 1: New Species: [[food, 1], [body, 3], [population, 3], [traits, []]], "
                          "Species 2: New Species: [[food, 3], [body, 3], [population, 4], [traits, []]], "
                          "[active, False->True]")

    def test_choose(self):
        player_1_hand = [self.ambush_3,  # 2nd
                         self.carnivore_7,  # 4th
                         self.carnivore_neg7,  # 3rd
                         self.ambush_1,  # 1st
                         self.longneck_neg2,  # 6th
                         self.foraging_0,  # 5th
                         self.scavenger_neg3]  # Not used
        self.player_1.hand = player_1_hand
        action4_1 = Action4(FoodCardAction(3),
                            [GrowAction(POPULATION, 3, 1)],
                            [GrowAction(BODY, 3, 5)],
                            [AddSpeciesAction(0, [2])],
                            [ReplaceTraitAction(3, 0, 4)])
        result_action4 = self.player_1.choose([])
        self.assertEquals(result_action4.food_card, action4_1.food_card)
        self.assertEquals(result_action4.grow_pop, action4_1.grow_pop)
        self.assertEquals(result_action4.grow_body, action4_1.grow_body)
        self.assertEquals(result_action4.add_species, action4_1.add_species)
        self.assertEquals(result_action4.replace_trait, action4_1.replace_trait)
        self.assertEquals(result_action4, action4_1)




if __name__ == '__main__':
    unittest.main()
