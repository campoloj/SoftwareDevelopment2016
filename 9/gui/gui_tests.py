import unittest
from player_state import PlayerState
from species import Species
from traitcard import TraitCard
from dealer import Dealer
from globals import *
import gui

class TestGui(unittest.TestCase):

    def setUp(self):
        self.trait1 = TraitCard(CARNIVORE, 2)
        self.trait2 = TraitCard(SCAVENGER, 3)
        self.trait3 = TraitCard(FATTISSUE, 2)
        self.trait4 = TraitCard(FORAGING, 3)
        self.species_1 = Species(4, 4, 4, [self.trait3], 3)
        self.species_2 = Species(4, 4, 4)
        self.species_3 = Species(4, 4, 3)
        self.species_4 = Species(4, 3, 3)
        self.species_5 = Species(3, 1, 3)
        self.species_6 = Species(4, 3, 3)
        self.species_7 = Species(4, 4, 4)
        self.player_1 = PlayerState(1, 2, [self.trait1, self.trait2], [self.species_4, self.species_5, self.species_6])
        self.player_2 = PlayerState(2, 10, [], [self.species_1])
        self.player_3 = PlayerState(3, 4, [self.trait4], [self.species_2, self.species_3, self.species_7])
        self.dealer_1 = Dealer([self.player_1, self.player_2, self.player_3], 10, [self.trait1, self.trait2])

    def test_player_display(self):
        player_1_text = """Player 1:
    Species ([Food, Body, Population, Traits, Fat-food]):
        [3, 3, 4, [], None]
        [1, 3, 3, [], None]
        [3, 3, 4, [], None]
    Bag: 2
    Hand: [[2, carnivore], [3, scavenger]]"""
        self.assertEquals(gui.render_player(self.player_1), player_1_text)

    def test_dealer_display(self):
        dealer_1_text = """Dealer Configuration:
    Watering Hole: 10
    Deck: [[2, carnivore], [3, scavenger]]
    Players:
        Player 1:
            Species ([Food, Body, Population, Traits, Fat-food]):
                [3, 3, 4, [], None]
                [1, 3, 3, [], None]
                [3, 3, 4, [], None]
            Bag: 2
            Hand: [[2, carnivore], [3, scavenger]]
        Player 2:
            Species ([Food, Body, Population, Traits, Fat-food]):
                [4, 4, 4, [fat-tissue], 3]
            Bag: 10
            Hand: []
        Player 3:
            Species ([Food, Body, Population, Traits, Fat-food]):
                [4, 4, 4, [], None]
                [4, 3, 4, [], None]
                [4, 4, 4, [], None]
            Bag: 4
            Hand: [[3, foraging]]"""
        self.assertEquals(gui.render_dealer(self.dealer_1), dealer_1_text)

    def test_display(self):
        gui.display(gui.render_dealer(self.dealer_1))
        gui.display(gui.render_player(self.player_1))

if __name__ == '__main__':
    unittest.main()



