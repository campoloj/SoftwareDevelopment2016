import os
import sys

globals_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..%s" % os.sep)
sys.path.append(globals_path)

from globals import *


class Species(object):
    """
    A data representation of a Species in the Evolution game
    """
    def __init__(self, population=1, food=0, body=0, traits=None, fat_storage=None):
        self.population = population
        self.food = food
        self.body = body
        self.traits = traits if traits else []
        if fat_storage:
            self.fat_storage = fat_storage
        else:
            self.fat_storage = (0 if FATTISSUE in self.trait_names() else None)

    def __str__(self):
        return "Species(pop=%d, food=%d, body=%d, traits=%s" \
               % (self.population, self.food, self.body, self.traits)

    def is_attackable(self, attacker, left_neighbor=False, right_neighbor=False):
        """
        Determines if this species is attackable by the attacker species, given its two neighbors
        :param attacker: the Species attacking this species
        :param left_neighbor: the Species to the left of this species (False if no left neighbor)
        :param right_neighbor: the Species to the right of this species (False if no left neighbor)
        :return: True if attackable, else false
        """
        defender_traits = self.trait_names()
        attacker_traits = attacker.trait_names()
        left_traits = left_neighbor.trait_names() if left_neighbor else []
        right_traits = right_neighbor.trait_names() if right_neighbor else []
        attacker_body = attacker.body + (attacker.population if PACKHUNTING in attacker_traits else 0)

        return not any([CARNIVORE not in attacker_traits,
                        BURROWING in defender_traits and self.food == self.population,
                        CLIMBING in defender_traits and CLIMBING not in attacker_traits,
                        HARDSHELL in defender_traits and attacker_body - self.body < HARD_SHELL_DIFF,
                        HERDING in defender_traits and attacker.population <= self.population,
                        SYMBIOSIS in defender_traits and right_neighbor and right_neighbor.body > self.body,
                        ((WARNINGCALL in right_traits) or (WARNINGCALL in left_traits))
                        and AMBUSH not in attacker_traits])

    def trait_names(self):
        """
        Gives the names of the TraitCard(s) of this species
        :return: a list of trait names
        """
        return [trait_card.trait for trait_card in self.traits]

    def equal_attributes(self, other):
        """
        Return True if this species and the given species have the same attributes.
        :param other: The other species
        :return: Boolean
        """
        return all([isinstance(other, Species),
                    self.population == other.population,
                    self.food == other.food,
                    self.body == other.body,
                    self.traits == other.traits,
                    self.fat_storage == other.fat_storage])

    def is_hungry(self):
        """
        Return True if this species is hungry
        :return: boolean
        """
        return self.population > self.food

    def reduce_population(self):
        """
        Reduces the population of this species after a carnivore attack
        """
        self.population -= KILL_QUANTITY
        self.food = min(self.population, self.food)