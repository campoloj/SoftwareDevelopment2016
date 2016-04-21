import unittest
from player_state import PlayerState
from species import Species
from traitcard import TraitCard
from globals import *


class TestSpecies(unittest.TestCase):

    def setUp(self):
        self.attacker = Species()
        self.attacker.traits = [TraitCard(CARNIVORE)]
        self.defender = Species()
        self.left_neighbor = Species()
        self.right_neighbor = Species()

        self.species_1 = Species(4, 4, 4)
        self.species_2 = Species(4, 4, 4)
        self.species_3 = Species(4, 4, 3)
        self.species_4 = Species(4, 3, 3)
        self.species_5 = Species(3, 3, 3)
        self.species_list = [self.species_2, self.species_4, self.species_3, self.species_5, self.species_1]

        self.player_1 = PlayerState(1)
        self.player_2 = PlayerState(2)

    def test_all_attackable_species(self):
        self.species_1.traits = [TraitCard(CARNIVORE)]
        self.species_2.traits = [TraitCard(CLIMBING)]
        self.species_4.traits = [TraitCard(HARDSHELL)]
        self.player_1.species = [self.species_2, self.species_3]
        self.player_2.species = [self.species_4, self.species_5]
        self.assertEqual(self.species_1.all_attackable_species([self.player_1, self.player_2]),
                         [self.species_3, self.species_5])

    def test_trait_names(self):
        self.assertEqual(self.defender.trait_names(), [])
        self.assertEqual(self.attacker.trait_names(), [CARNIVORE])

    def test_attackable(self):
        self.assertTrue(self.defender.is_attackable(self.attacker))

    def test_no_carnivore(self):
        self.attacker.traits = []
        self.assertFalse(self.defender.is_attackable(self.attacker))

    def test_burrowing(self):
        self.defender.traits = [TraitCard(BURROWING)]
        self.defender.population, self.defender.food = (4, 4)
        self.assertFalse(self.defender.is_attackable(self.attacker))
        self.defender.food = 3
        self.assertTrue(self.defender.is_attackable(self.attacker))

    def test_climbing(self):
        self.defender.traits = [TraitCard(CLIMBING)]
        self.assertFalse(self.defender.is_attackable(self.attacker))
        self.attacker.traits.append(TraitCard(CLIMBING))
        self.assertTrue(self.defender.is_attackable(self.attacker))

    def test_hard_shell(self):
        self.defender.traits = [TraitCard(HARDSHELL)]
        self.defender.body = 3
        self.attacker.body = 6
        self.assertFalse(self.defender.is_attackable(self.attacker))
        self.attacker.body = 7
        self.assertTrue(self.defender.is_attackable(self.attacker))

    def test_herding(self):
        self.defender.traits = [TraitCard(HERDING)]
        self.defender.population = 4
        self.attacker.population = 3
        self.assertFalse(self.defender.is_attackable(self.attacker))
        self.attacker.population = 5
        self.assertTrue(self.defender.is_attackable(self.attacker))

    def test_symbiosis(self):
        self.defender.traits = [TraitCard(SYMBIOSIS)]
        self.defender.body = 3
        self.right_neighbor.body = 5
        self.assertFalse(self.defender.is_attackable(self.attacker, right_neighbor=self.right_neighbor))
        self.right_neighbor.body = 2
        self.assertTrue(self.defender.is_attackable(self.attacker, right_neighbor=self.right_neighbor))

    def test_warning_call(self):
        self.left_neighbor.traits = [TraitCard(WARNINGCALL)]
        self.right_neighbor.traits = [TraitCard(WARNINGCALL)]
        self.assertFalse(self.defender.is_attackable(self.attacker, left_neighbor=self.left_neighbor))
        self.assertFalse(self.defender.is_attackable(self.attacker, right_neighbor=self.right_neighbor))
        self.attacker.traits.append(TraitCard(AMBUSH))
        self.assertTrue(self.defender.is_attackable(self.attacker, left_neighbor=self.left_neighbor))

    def test_show_changes(self):
        self.assertEquals(self.species_1.show_changes(self.species_3), '[[body, 4->3]]')
        self.assertEquals(self.species_1.show_changes(self.species_2), '')
        self.species_2.traits = [TraitCard(CLIMBING)]
        self.assertEquals(self.species_1.show_changes(self.species_2), '[[traits: new cards: [climbing, 0]]]')
        self.species_3.traits = [TraitCard(HERDING)]
        self.assertEquals(self.species_2.show_changes(self.species_3), '[[body, 4->3], [traits: [0, [climbing, 0]->[herding, 0]]]]')
        self.species_3.population = 1
        self.species_3.food = 0
        self.species_3.traits.append(TraitCard(BURROWING))
        self.assertEquals(self.species_2.show_changes(self.species_3),
                          '[[population, 4->1], [food, 4->0], [body, 4->3], '
                          '[traits: new cards: [herding, 0], [burrowing, 0]]]')
        self.species_2.traits = [TraitCard(CLIMBING)]
        self.species_3.traits = [TraitCard(CLIMBING)]
        self.assertEquals(self.species_2.show_changes(self.species_3),
                          '[[population, 4->1], [food, 4->0], [body, 4->3]]')



if __name__ == '__main__':
    unittest.main()


