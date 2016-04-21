
from globals import *
from traitcard import TraitCard


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
            attackable_species += player.get_attackable_species(self)
        return attackable_species

    def is_attackable(self, attacker, left_neighbor=False, right_neighbor=False):
        """
        Determines if this species is attackable by an attacking species, given its two neighbors
        :param attacker: the Species attacking this species
        :param left_neighbor: the Species to the left of this species (False if no left neighbor)
        :param right_neighbor: the Species to the right of this species (False if no left neighbor)
        :return: True if this species is attackable, else False
        """
        warning_call = ((left_neighbor.has_trait(WARNINGCALL) if left_neighbor else False) or
                        (right_neighbor.has_trait(WARNINGCALL) if right_neighbor else False))
        attacker_body = attacker.body + (attacker.population if attacker.has_trait(PACKHUNTING) else 0)
        return not any([attacker.has_trait(CARNIVORE),
                        self.has_trait(BURROWING) and self.food == self.population,
                        self.has_trait(CLIMBING) and not attacker.has_trait(CLIMBING),
                        self.has_trait(HARDSHELL) and attacker_body - self.body < HARD_SHELL_DIFF,
                        self.has_trait(HERDING) and attacker.population <= self.population,
                        self.has_trait(SYMBIOSIS) and right_neighbor and right_neighbor.body > self.body,
                        warning_call and not attacker.has_trait(AMBUSH)])

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

    def consolidate_food(self):
        """
        Reduces this Species's population based on its food and returns its food value for the PlayerState
        :effect Population is reduced if necessary, food is reset to 0
        :return: Natural representing food for the PlayerState's food bag
        """
        food = self.food
        self.population = food
        self.food = MIN_FOOD
        return food

    def replace_trait(self, traitcard_index, replacement_card):
        """
        :effect Replaces the TraitCard at the specified index into this Species's traits with the given
                replacement TraitCard
        :param traitcard_index: Nat representing index of TraitCard to replace
        :param replacement_card: TraitCard to put on this Species
        """
        self.traits[traitcard_index] = replacement_card

    def move_fat(self):
        """
        Effect: Moves the fat from the fat-storage to food if it applies.
        """
        if self.fat_storage:
            transfer = min(self.population, self.fat_storage)
            self.fat_storage -= transfer
            self.food += transfer

    def modify_if_fertile(self):
        """
        :effect Adds population to Species if it contains the fertile trait
        """
        if self.has_trait(FERTILE):
            self.population += GROW_POP_AMOUNT

    def has_trait(self, trait):
        """
        :param trait the trait we are looking for in this species' traits
        :return True if this species has the given trait
        """
        return trait in self.trait_names()

    def feed(self, watering_hole):
        """
        :effect feed this species if it can be fed
        :param watering_hole: The food on the watering hole
        :return: Nat food remaining on the watering hole
        """
        if not self.is_hungry() or watering_hole <= MIN_WATERING_HOLE:
            return watering_hole
        self.food += FEED_QUANTITY
        return watering_hole - FEED_QUANTITY

    @classmethod
    def validate_all_cards(cls, list_of_species, total_deck):
        """
        Validates the TraitCards of all Species in the given list.
        :param list_of_species: a list of Species objects to be validated
        :param total_deck: a list of TraitCards representing all valid card possibilities
        :raise ValueError if invalid TraitCards exist on any Species
        """
        for species in list_of_species:
            species.validate_cards(total_deck)

    def validate_cards(self, total_deck):
        """
        Validates this species by checking that each of its TraitCards is unique and possible
        :param total_deck: a list of TraitCards representing all valid card possibilities
        :raise ValueError if invalid cards exist on any species
        """
        TraitCard.validate_all_unique(self.traits, total_deck)

    @classmethod
    def validate_all_attributes(cls, list_of_species):
        """
        Validates the attributes of all Species in the given list
        :param list_of_species: a list of Species objects to be validated
        :raise AssertionError if any Species attributes are out of bounds
        """
        for species in list_of_species:
            species.validate_attributes()

    def validate_attributes(self):
        """
        Validates the attributes of this Species
        :raise AssertionError if any attributes are out of bounds
        """
        assert(isinstance(self.population, int) and MAX_POP >= self.population >= MIN_POP)
        assert(isinstance(self.food, int) and MAX_FOOD >= self.food >= MIN_FOOD)
        assert(isinstance(self.body, int) and MAX_BODY >= self.body >= MIN_BODY)
        assert(all([isinstance(self.traits, list), MAX_TRAITS >= len(self.traits),
                    len(self.trait_names()) == len(set(self.trait_names()))]))
        TraitCard.validate_all_attributes(self.traits)
        if self.fat_storage is not False:
            assert(isinstance(self.body, int) and self.body >= self.fat_storage >= MIN_FATFOOD)

    def species_to_json(self):
        """
        Converts a Species object into a JSON Species+. Does not render empty fat-food.
        :return: a JSON Species+ as specified by the data definition at
                 http://www.ccs.neu.edu/home/matthias/4500-s16/6.html
        """
        json_traits = '['
        for trait in self.traits:
            json_traits += trait.trait_to_json()
            if trait != self.traits[-1]:
                json_traits += ", "
        json_traits += ']'
        json_species_template = '[[%s, %d], [%s, %d], [%s, %d], [%s, %s]]'
        json_species = json_species_template % (FOOD, self.food, BODY, self.body, POPULATION,
                                                self.population, TRAITS, json_traits)
        if self.fat_storage:
            json_species[:-1] += '[%s, %d]]' % (FATFOOD, self.fat_storage)
        return json_species

    @classmethod
    def show_all_changes(cls, before_species, after_species):
        changes = []
        for i in range(max(len(before_species), len(after_species))):
            if i >= len(before_species):
                species_change = "New Species: %s" % after_species[i].species_to_json()
            elif i >= len(after_species):
                species_change = "Species removed"
            else:
                species_change = before_species[i].show_changes(after_species[i])
            if species_change:
                changes.append("Species %d: %s" % (i, species_change))
        return ", ".join(changes)

    def show_changes(self, species2):
        """
        Shows a string representation of the differences between this Species and the given Species.
        :param species2: The Species we are comparing to this Species
        :return: String representing the differences
        """

        changes = []
        if self.population != species2.population:
            changes.append(CHANGE_TEMPLATE % (POPULATION, self.population, species2.population))
        if self.food != species2.food:
            changes.append(CHANGE_TEMPLATE % (FOOD, self.food, species2.food))
        if self.body != species2.body:
            changes.append(CHANGE_TEMPLATE % (BODY, self.body, species2.body))
        trait_changes = TraitCard.show_all_changes(self.traits, species2.traits)
        if trait_changes:
            changes.append('[traits: ' + trait_changes + ']')
        if self.fat_storage != species2.fat_storage:
            changes.append(CHANGE_TEMPLATE % (FATTISSUE, self.fat_storage, species2.fat_storage))
        return '[' + ", ".join(changes) + ']' if changes else ''



