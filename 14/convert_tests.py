import unittest

from convert import Convert
from dealer.player_state import PlayerState
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

        self.jSpecies_card1 = [2, WARNINGCALL]
        self.jSpecies_card2 = [5, CARNIVORE]
        self.jSpecies_card3 = [-3, BURROWING]
        self.jSpecies_card4 = [3, AMBUSH]
        self.jSpecies_card5 = [0, SCAVENGER]

        self.jSpecies_1 = [[FOOD, 2], [BODY, 2], [POPULATION, 2], [TRAITS, [self.jt_1]]]
        self.jSpecies_2 = [[FOOD, 2], [BODY, 3], [POPULATION, 3], [TRAITS, [self.jt_2]]]
        self.jSpecies_3 = [[FOOD, 2], [BODY, 3], [POPULATION, 4], [TRAITS, [self.jt_3, self.jt_4]]]
        self.jSpecies_4 = [[FOOD, 2], [BODY, 2], [POPULATION, 2], [TRAITS, [self.jt_3, self.jt_4]]]

        self.jPlayer_1 = [[ID, 1], [SPECIES, [self.jSpecies_1]], [BAG, 2]]
        self.jPlayer_2 = [[ID, 2], [SPECIES, [self.jSpecies_2]], [BAG, 1]]
        self.jPlayer_3 = [[ID, 3], [SPECIES, [self.jSpecies_3, self.jSpecies_4]], [BAG, 3]]
        self.jPlayer_4 = [[ID, 2], [SPECIES, []], [BAG, 1]]

        self.jLob = [[self.jSpecies_1], [self.jSpecies_2], [self.jSpecies_3, self.jSpecies_4], []]
        self.jLob_1 = [[self.jSpecies_2], [self.jSpecies_3, self.jSpecies_4], []]
        self.jState_1 = [2, [self.jSpecies_1], []]
        self.jGameState_1 = [2, [self.jSpecies_1], [], 10, self.jLob_1]

        self.jNoFeed = False
        self.jHerbFeed = 0
        self.jFatFeed = [0, 3]
        self.jCarnFeed = [0, 0, 0]

        self.jFC = 0
        self.jGP = [1, 1]
        self.jGB_1 = [0, 1]
        self.jGB_2 = [1, 2]
        self.jBT_1 = [1]
        self.jBT_2 = [2, 2]
        self.jBT_3 = [3, 3, 3]
        self.jBT_4 = [4, 4, 4, 4]
        self.jRT = [0, 1, 2]

        self.jAct4 = [self.jFC, [self.jGP], [self.jGB_1, self.jGB_2], [self.jBT_1, self.jBT_3, self.jBT_4], [self.jRT]]

        self.jList_of_players = [self.jPlayer_1, self.jPlayer_4, self.jPlayer_3]
        self.jDeck = [self.jSpecies_card1, self.jSpecies_card2, self.jSpecies_card3,
                      self.jSpecies_card4, self.jSpecies_card5]
        self.jDealer = [self.jList_of_players, 12, self.jDeck]



    def test_json_to_trait(self):
        self.assertEqual(Convert.json_to_trait(self.jt_1).convert_to_json(), self.jt_1)
        self.assertNotEqual(Convert.json_to_trait(self.jt_1).convert_to_json(), self.jt_2)
        self.assertEqual(Convert.json_to_trait(self.jSpecies_card1).convert_to_json(), self.jSpecies_card1)

    def test_json_to_species(self):
        self.assertEqual(Convert.json_to_species(self.jSpecies_1).convert_to_json(), self.jSpecies_1)
        self.assertEqual(Convert.json_to_species(self.jSpecies_2).convert_to_json(), self.jSpecies_2)
        self.assertNotEqual(Convert.json_to_species(self.jSpecies_1).convert_to_json(), self.jSpecies_2)

    def test_json_to_player(self):
        # Player+ / PlayerState
        self.assertEqual(Convert.json_to_player(self.jPlayer_1).convert_to_player_json(), self.jPlayer_1)
        self.assertNotEqual(Convert.json_to_player(self.jPlayer_1).convert_to_player_json(), self.jPlayer_2)

        # Boards / [Species, ...]
        self.assertEqual(Convert.json_boards_to_player([self.jSpecies_3, self.jSpecies_4]).convert_to_boards_json(),
                         [self.jSpecies_3, self.jSpecies_4])

        # State / [Nat, [Species, ...], [TraitCard, ...]]
        self.assertEqual(Convert.state_json_to_player(self.jState_1).convert_to_state_json(),
                         self.jState_1)
        wh, player = Convert.json_to_wh_state([10, 2, [self.jSpecies_1], []])
        self.assertEqual(10, wh)
        self.assertEqual(player.convert_to_state_json(), self.jState_1)

        # LOB / [PlayerState, ...]
        lop = Convert.json_to_choice_lop(self.jLob)
        lob1, lob2 = Convert.players_to_all_json(lop[:2], lop[2:])
        self.assertEqual(self.jLob[:2], lob1)
        self.assertEqual(self.jLob[2:], lob2)

    def test_json_to_gamestate(self):
        player, wh, op = Convert.json_to_gamestate(self.jGameState_1)
        new_jgs = Convert.gamestate_to_json(player, wh, op)
        self.assertEqual(new_jgs, self.jGameState_1)

    def test_json_to_feeding_choice(self):
        self.assertEqual(Convert.json_to_feeding_choice(self.jNoFeed).convert_to_json(), self.jNoFeed)
        self.assertEqual(Convert.json_to_feeding_choice(self.jHerbFeed).convert_to_json(), self.jHerbFeed)
        self.assertEqual(Convert.json_to_feeding_choice(self.jCarnFeed).convert_to_json(), self.jCarnFeed)
        self.assertEqual(Convert.json_to_feeding_choice(self.jFatFeed).convert_to_json(), self.jFatFeed)

    def test_json_to_action4(self):
        self.assertEqual(Convert.json_to_action4(self.jAct4).convert_to_json(), self.jAct4)

    def test_json_to_dealer(self):
        self.assertEqual(Convert.json_to_dealer(self.jDealer).convert_to_json(), self.jDealer)


if __name__ == '__main__':
    unittest.main()
