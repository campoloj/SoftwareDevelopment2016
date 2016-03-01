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
    def __init__(self, population=1, food=0, body=0, traits=[], fat_storage=None):
        self.population = population
        self.food = food
        self.body = body
        self.traits = traits
        self.fat_storage = fat_storage

    def __str__(self):
        return "Species(pop=%d, food=%d, body=%d, traits=%s" \
               % (self.population, self.food, self.body, self.traits)

    def __eq__(self, other):
        return all([isinstance(other, Species),
                    self.population == other.population,
                    self.food == other.food,
                    self.body == other.body,
                    self.traits == other.traits,
                    self.fat_storage == other.fat_storage])

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
        attacker_body = attacker.body + (attacker.population if "pack-hunting" in attacker_traits else 0)

        return not any(["carnivore" not in attacker_traits,
                        "burrowing" in defender_traits and self.food == self.population,
                        "climbing" in defender_traits and "climbing" not in attacker_traits,
                        "hard-shell" in defender_traits and attacker_body - self.body < HARD_SHELL_DIFF,
                        "herding" in defender_traits and attacker.population <= self.population,
                        "symbiosis" in defender_traits and right_neighbor and right_neighbor.body > self.body,
                        (("warning-call" in right_traits) or ("warning-call" in left_traits))
                        and "ambush" not in attacker_traits])

    def trait_names(self):
        """
        Gives the names of the TraitCard(s) of this species
        :return: a list of trait names
        """
        return map(lambda (x): x.trait, self.traits)

    @classmethod
    def largest_tied_species(cls, list_of_species):
        """
        Returns the largest tied species of a Player's species, in terms of lexicographical order
        :param list_of_species: a Player's species boards
        :return: list of largest Species
        """
        sorted_species = cls.sort_lex(list_of_species)
        largest = sorted_species[0]
        largest_species = [species for species in sorted_species
                           if species.population == largest.population
                           and species.food == largest.food
                           and species.body == largest.body]
        return largest_species

    @classmethod
    def sort_lex(cls, list_of_species):
        """
        Returns the largest species in a list based on a lexicographic manner
        :param list_of_species: a list of Species
        :return: the largest Species
        """
        return sorted(list_of_species, cmp=cls.is_larger, reverse=True)


    @classmethod
    def is_larger(cls, species_1, species_2):
        """
        Determines which of the two given species are larger based on a lexicographic manner
        :param species_1: first species to compare
        :param species_2: second species to compare
        :return: 1 if the first species is larger, -1 if the second is larger, 0 if they are equal
        """
        if species_1.population > species_2.population:
            return 1
        elif species_1.population == species_2.population:
            if species_1.food > species_2.food:
                return 1
            elif species_1.food == species_2.food:
                if species_1.body > species_2.body:
                    return 1
                elif species_1.body == species_2.body:
                    return 0
        return -1

    @classmethod
    def largest_fatty_need(cls, list_of_species):
        """
        Determines which species has a greater need for fat-tissue food
        :param list_of_species: list of Species with the fat-tissue trait
        :return: Species with greatest fat-tissue need
        """
        if len(list_of_species) == 1:
            return list_of_species[0]
        else:
            max_need = max([species.population - species.food for species in list_of_species])

        highest_needers = [species for species in list_of_species
                           if species.population - species.food == max_need]
        largest_needers = cls.largest_tied_species(highest_needers)
        if len(largest_needers) > 1:
            positions = [list_of_species.index(species) for species in largest_needers]
            return largest_needers[positions.index(min(positions))]
        else:
            return largest_needers[0]


