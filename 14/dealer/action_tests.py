import unittest
import copy
from action import *
from action4 import Action4
from traitcard import TraitCard
from species import Species
from player_state import PlayerState
from dealer import Dealer
from globals import *
from feeding_choice import *


class TestActions(unittest.TestCase):

    def setUp(self):
        # Traits (Trait, Food-value)
        self.carnivore = TraitCard(CARNIVORE, 3)
        self.burrowing = TraitCard(BURROWING, 2)
        self.fattissue = TraitCard(FATTISSUE, 4)
        self.foraging = TraitCard(FORAGING, 2)
        self.horns = TraitCard(HORNS, 6)
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
        self.player1 = PlayerState(1, 0, [self.fattissue], self.player1_species)
        self.player2 = PlayerState(2, 3, [self.fattissue, self.carnivore], self.player2_species)
        self.player3 = PlayerState(3, 6, [self.burrowing], self.player3_species)

        self.public_player1 = PlayerState(1, False, False, self.player1_species)
        self.public_player2 = PlayerState(2, False, False, self.player2_species)
        self.public_player3 = PlayerState(3, False, False, self.player3_species)

        self.list_of_players = [self.player1, self.player2, self.player3]

        # Dealer (List of Players, Watering Hole, Deck)
        self.dealer1 = Dealer(self.list_of_players, 10, [])

        # Actions
        self.food_card_action1 = FoodCardAction(0)
        self.food_card_action2 = FoodCardAction(1)
        self.grow_action_pop = GrowAction(POPULATION, 0, 0)
        self.grow_action_body = GrowAction(BODY, 1, 1)
        self.add_species_action1 = AddSpeciesAction(0, [1])
        self.add_species_action2 = AddSpeciesAction(0, [])
        self.replace_trait_action1 = ReplaceTraitAction(0, 0, 0)
        self.replace_trait_action2 = ReplaceTraitAction(2, 0, 1)
        self.replace_trait_action3 = ReplaceTraitAction(0, 2, 0)

        # Action4
        self.action4_1 = Action4(self.food_card_action1)
        self.action4_2 = Action4(self.food_card_action2, grow_pop=[self.grow_action_pop])

    def test_food_card_action(self):
        old_dealer = copy.deepcopy(self.dealer1)
        self.food_card_action1.apply(self.dealer1, self.player1)
        self.assertEquals(old_dealer.show_changes(self.dealer1), '[watering_hole, 10->14]')
        old_dealer = copy.deepcopy(self.dealer1)
        self.food_card_action2.apply(self.dealer1, self.player2)
        self.assertEquals(old_dealer.show_changes(self.dealer1), '[watering_hole, 14->17]')

    def test_grow_action(self):
        old_dealer = copy.deepcopy(self.dealer1)
        self.grow_action_pop.apply(self.dealer1, self.player1)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 1: '
                          'Species 0: [[population, 1->2]]')
        old_dealer = copy.deepcopy(self.dealer1)
        self.grow_action_body.apply(self.dealer1, self.player2)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 2: '
                          'Species 1: [[body, 5->6]]')

    def test_add_species_action(self):
        old_dealer = copy.deepcopy(self.dealer1)
        self.add_species_action1.apply(self.dealer1, self.player2)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          "Player 2: "
                          "Species 3: New Species: [[food, 0], [body, 0], [population, 1], "
                                                   "[traits, [[carnivore, 3]]]]")
        old_dealer = copy.deepcopy(self.dealer1)
        self.add_species_action2.apply(self.dealer1, self.player3)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 3: '
                          'Species 2: New Species: [[food, 0], [body, 0], [population, 1], [traits, []]]')

    def test_replace_trait_action(self):
        old_dealer = copy.deepcopy(self.dealer1)
        self.replace_trait_action1.apply(self.dealer1, self.player1)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 1: '
                          'Species 0: [[traits: [0, [cooperation, 1]->[fat-tissue, 4]]]]')
        old_dealer = copy.deepcopy(self.dealer1)
        self.replace_trait_action2.apply(self.dealer1, self.player2)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 2: '
                          'Species 2: [[traits: [0, [foraging, 2]->[carnivore, 3]]]]')
        old_dealer = copy.deepcopy(self.dealer1)
        self.replace_trait_action3.apply(self.dealer1, self.player3)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 3: '
                          'Species 0: [[traits: [2, [scavenger, 2]->[burrowing, 2]]]]')

    def test_action4_apply_all(self):
        old_dealer = copy.deepcopy(self.dealer1)
        self.action4_1.apply_all(self.dealer1, self.player1)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 1: '
                          'removed cards: [fat-tissue, 4], '
                          '[watering_hole, 10->14]')
        old_dealer = copy.deepcopy(self.dealer1)
        self.action4_2.apply_all(self.dealer1, self.player2)
        self.assertEquals(old_dealer.show_changes(self.dealer1),
                          'Player 2: '
                          'removed cards: [fat-tissue, 4], [carnivore, 3], '
                          'Species 0: [[population, 3->4]], '
                          '[watering_hole, 14->17]' )






if __name__ == '__main__':
    unittest.main()