"""
A data representation of a Species in the Evolution game
"""


class Species(object):
    def __init__(self):
        self.food = 0
        self.body = 0
        self.population = 1
        self.traits = []

    def is_attackable(self, attacker, left_neighbor=False, right_neighbor=False):
        """
        Determines if this species is attackable by the attacker species, given its two neighbors
        :param attacker: the Species attacking this species
        :param left_neighbor: the Species to the left of this species (False if no left neighbor)
        :param right_neighbor: the Species to the right of this species (False if no left neighbor)
        :return: True if attackable, else false
        """
        return not any(["carnivore" not in attacker.traits,
                        "burrowing" in self.traits and self.food == self.population,
                        "climbing" in self.traits and "climbing" not in attacker.traits,
                        "hard-shell" in self.traits and attacker.body - self.body < 4,
                        "herding" in self.traits and attacker.population <= self.population,
                        "symbiosis" in self.traits and right_neighbor and right_neighbor.body > self.body,
                        ((right_neighbor and "warning-call" in right_neighbor.traits) or
                         (left_neighbor and "warning-call" in left_neighbor.traits))
                        and "ambush" not in attacker.traits])