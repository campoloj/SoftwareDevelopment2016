import unittest
from species import Species
from traitcard import TraitCard
from player import Player
from player_state import PlayerState


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

    def test_feed_fatty(self):
        self.species_4.traits = [TraitCard("fat-tissue")]
        self.species_1.traits = [TraitCard("fat-tissue")]
        self.species_5.traits = [TraitCard("fat-tissue")]
        self.assertEqual(Player.feed_fatty([self.species_4, self.species_1, self.species_5], 10),
                         [self.species_5, 3])
        self.assertEqual(Player.feed_fatty([self.species_4, self.species_1, self.species_5], 1),
                         [self.species_5, 1])
        self.assertEqual(Player.feed_fatty([self.species_4, self.species_1], 10),
                         [self.species_4, 3])

    def test_feed_herbivore(self):
        self.assertEqual(Player.feed_herbivores([self.species_4, self.species_5]), self.species_4)

    def test_feed_carnivore(self):
        self.species_4.traits = [TraitCard("carnivore", 4)]
        self.species_5.traits = [TraitCard("carnivore")]
        self.species_6.traits = [TraitCard("carnivore")]

        # Test tie in largest carnivore in attacking player's hand => first species chosen
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_2, self.player_3]),
                         [self.species_4, self.player_2, self.species_1])

        # Repeat to test first is chosen again when order is changed
        self.player_1.species = [self.species_6, self.species_5, self.species_4]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_2, self.player_3]),
                         [self.species_6, self.player_2, self.species_1])

        # Test tie in largest target between defending players' hands => first given player chosen
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         [self.species_6, self.player_3, self.species_2])

        # Test tie in largest target within defending player's hand => first species chosen
        self.player_3.species = [self.species_7, self.species_3, self.species_2]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         [self.species_6, self.player_3, self.species_7])

        # Retest tie, but with first species unattackable => second largest chosen
        self.species_7.traits = [TraitCard("climbing")]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         [self.species_6, self.player_3, self.species_2])

        # Repeat again, but since both largest in first player's hand are unattackable => second player w/ largest
        self.species_2.traits = [TraitCard("burrowing")]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         [self.species_6, self.player_2, self.species_1])

        # Test that if all largest species are unattackable, a smaller species is chosen
        self.species_1.traits = [TraitCard("climbing")]
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         [self.species_6, self.player_3, self.species_3])

        # Test that a carnivore with overriding traits attacks the largest species attackable
        self.species_3.traits = [TraitCard("climbing")]
        self.species_4.traits.append(TraitCard("climbing"))
        self.assertEqual(Player.feed_carnivore(self.player_1.species, self.player_1, [self.player_3, self.player_2]),
                         [self.species_4, self.player_3, self.species_7])

    def test_next_feeding(self):
        self.species_4.traits = [TraitCard("carnivore")]
        self.species_5.traits = [TraitCard("fat-tissue")]
        # Test if fat_tissue_species
        self.assertEqual(Player.next_feeding(self.player_1, 10, [self.player_2, self.player_3]), [1, 3])
        # Test if hungry_herbivores
        self.species_5.traits = []
        self.assertEqual(Player.next_feeding(self.player_1, 10, [self.player_2]), 2)
        # Test if hungry_carnivore
        self.species_5.traits = [TraitCard("carnivore")]
        self.species_6.traits = [TraitCard("carnivore")]
        self.assertEqual(Player.next_feeding(self.player_1, 10, [self.player_2, self.player_3]), [0, 0, 0])
        # Test no attackable species
        self.assertEqual(Player.next_feeding(self.player_1, 10, [self.player_1]), False)
        # Test exception
        with self.assertRaises(Exception):
            Player.next_feeding(self.player_2, 10, [self.player_1])


if __name__ == '__main__':
    unittest.main()
