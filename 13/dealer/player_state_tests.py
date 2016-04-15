import unittest
import copy
from traitcard import TraitCard
from species import Species
from player_state import PlayerState
from globals import *
from action import GrowAction


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.carnivore = TraitCard(CARNIVORE, 3)
        self.burrowing = TraitCard(BURROWING, 2)
        self.fattissue = TraitCard(FATTISSUE, 4)
        self.foraging = TraitCard(FORAGING, 2)
        self.horns = TraitCard(HORNS, 6)
        self.cooperation = TraitCard(COOPERATION, 1)
        self.scavenger = TraitCard(SCAVENGER, 2)
        self.species_1 = Species(4, 4, 4, [])
        self.species_2 = Species(4, 4, 4)
        self.species_3 = Species(4, 4, 3)
        self.species_4 = Species(4, 3, 3)
        self.species_5 = Species(3, 1, 3)
        self.species_6 = Species(4, 3, 3)
        self.species_7 = Species(4, 4, 4)
        self.species_list = [self.species_2, self.species_4, self.species_3, self.species_5, self.species_1]
        self.player_1 = PlayerState(species=[self.species_4, self.species_5, self.species_6], hand=[self.carnivore])
        self.player_2 = PlayerState(species=[self.species_1], hand=[self.carnivore, self.fattissue])
        self.player_3 = PlayerState(species=[self.species_2, self.species_3, self.species_7], hand=[self.foraging])

    def test_grow_attribute(self):
        growpop = GrowAction("population", 0, 0)
        growbody = GrowAction("body", 0, 0)
        old_player = copy.deepcopy(self.player_1)

        self.player_1.grow_attribute(growpop)
        self.player_1.grow_attribute(growpop)
        self.player_1.grow_attribute(growbody)
        self.assertEqual(old_player.show_changes(self.player_1), 'Species 0: [[population, 4->6], [body, 3->4]]')

    def test_add_species(self):
        old_player_1 = copy.deepcopy(self.player_1)
        old_player_2 = copy.deepcopy(self.player_2)

        self.player_1.add_species([])
        self.assertEqual(old_player_1.show_changes(self.player_1),
                         'Species 3: New Species: [[food, 0], [body, 0], [population, 1], [traits, []]]')
        self.player_1.add_species([0])
        self.assertEqual(old_player_1.show_changes(self.player_1),
                         'Species 3: New Species: [[food, 0], [body, 0], [population, 1], [traits, []]], '
                         'Species 4: New Species: [[food, 0], [body, 0], [population, 1], [traits, [[carnivore, 3]]]]')

        self.player_2.add_species([0, 1])
        self.assertEqual(old_player_2.show_changes(self.player_2),
                         'Species 1: '
                         'New Species: '
                         '[[food, 0], [body, 0], [population, 1], [traits, [[carnivore, 3], [fat-tissue, 4]]]]')

    def test_discard_all(self):
        self.player_1.hand = [self.carnivore, self.fattissue, self.foraging, self.burrowing, self.cooperation]
        old_player = copy.deepcopy(self.player_1)

        self.player_1.discard_all([0, 2, 4])
        self.assertEqual(old_player.show_changes(self.player_1),
                         'removed cards: [carnivore, 3], [foraging, 2], [cooperation, 1]')
        return

    def test_show_changes(self):
        self.assertEquals(self.player_1.show_changes(self.player_2), 'new cards: [fat-tissue, 4], '
                                                                     'Species 0: [[food, 3->4], [body, 3->4]], '
                                                                     'Species 1: Species removed, '
                                                                     'Species 2: Species removed')
        self.player_2.food_bag = 3
        self.player_2.active = False
        self.assertEquals(self.player_1.show_changes(self.player_2),
                          '[food_bag, 0->3], '
                          'new cards: [fat-tissue, 4], '
                          'Species 0: [[food, 3->4], [body, 3->4]], '
                          'Species 1: Species removed, '
                          'Species 2: Species removed, '
                          '[active, True->False]')
        self.assertEquals(self.player_2.show_changes(self.player_1),
                          "[food_bag, 3->0], "
                          'removed cards: [fat-tissue, 4], '
                          "Species 0: [[food, 4->3], [body, 4->3]], "
                          "Species 1: New Species: [[food, 1], [body, 3], [population, 3], [traits, []]], "
                          "Species 2: New Species: [[food, 3], [body, 3], [population, 4], [traits, []]], "
                          "[active, False->True]")


if __name__ == '__main__':
    unittest.main()
