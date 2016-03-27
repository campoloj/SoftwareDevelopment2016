from globals import *


class Species(object):
    """
    A data representation of a Species in the Evolution game
    """
    def __init__(self, population=1, food=0, body=0, traits=False, fat_storage=False):
        """
        Creates a Species
        :param population: Natural+ representing the population of the species
        :param food: Natural representing the food held by the species
        :param body: Natural representing the body size of the species
        :param traits: List of TraitCard representing the traits associated with this species
                       NOTE: Length of traits cannot exceed 3. Each TraitCard must be distinct.
        :param fat_storage: Natural representing the fat-storage of this species if it has fat-tissue trait
        :return:
        """
        self.population = population
        self.food = food
        self.body = body
        self.traits = traits if traits else []
        if fat_storage:
            self.fat_storage = fat_storage
        else:
            self.fat_storage = (0 if FATTISSUE in self.trait_names() else False)

    def equal_attributes(self, other):
        """
        Determine if this species and the given species have the same attributes for testing purposes.
        :param other: the Species to compare this Species to
        :return: True if all attributes are equal, else False
        """
        return all([isinstance(other, Species),
                    self.population == other.population,
                    self.food == other.food,
                    self.body == other.body,
                    self.traits == other.traits,
                    self.fat_storage == other.fat_storage])

    def all_attackable_species(self, list_of_players):
        """
        Find all species attackable by this carnivore species in the given list of players
        :param list_of_players: List of PlayerState representing eligible targets for an attack
        :return: List of Species objects attackable by this carnivore Species
        """
        attackable_species = []
        for player in list_of_players:
            attackable_species += self.attackable_species(player)
        return attackable_species

    def attackable_species(self, player):
        """
        Find all species belonging to the given player that are attackable by this carnivore species
        :param player: PlayerState of the defending player
        :return: List of Species objects attackable by this carnivore Species
        """
        attackable_species = []
        for defender in player.species:
            if self == defender:
                continue
            if defender.is_attackable(self, player.get_left_neighbor(defender), player.get_right_neighbor(defender)):
                attackable_species.append(defender)
        return attackable_species

    def is_attackable(self, attacker, left_neighbor=False, right_neighbor=False):
        """
        Determines if this species is attackable by an attacking species, given its two neighbors
        :param attacker: the Species attacking this species
        :param left_neighbor: the Species to the left of this species (False if no left neighbor)
        :param right_neighbor: the Species to the right of this species (False if no left neighbor)
        :return: True if this species is attackable, else False
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
        :return: List of Strings representing trait names
        """
        return [trait_card.trait for trait_card in self.traits]

    def is_hungry(self):
        """
        Determine if this species is hungry
        :return: True if hungry, else False
        """
        return self.population > self.food

    def reduce_population(self):
        """
        Reduces the population of this species after a carnivore attack
        """
        self.population -= KILL_QUANTITY
        self.food = min(self.population, self.food)