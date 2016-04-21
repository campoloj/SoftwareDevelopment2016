from globals import *


class FeedingChoice(object):
    """
    An abstract class for representing the possible feeding choices a player can make.
    A FeedingChoice is one of:
    - NoFeeding
    - HerbivoreFeeding
    - FatFeeding
    - CarnivoreFeeding
    """
    def __init__(self):
        pass

    def handle_feeding(self, dealer, feeding_player):
        """
        Updates the Dealer configuration according to the feeding Player's choice
        :param dealer: the Dealer object
        :param feeding_player: the PlayerState of the Player choosing how to feed
        """
        return NotImplemented

    def convert_to_json(self):
        """
        Converts this FeedingChoice to its respective JSON representation
        :return JSON FeedingChoice as specified by
                http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        return NotImplemented


class NoFeeding(FeedingChoice):
    """
    Represents the Player choosing to abstain from feeding for the rest of ths round
    """

    def __eq__(self, other):
        """
        Compare attributes for testing.
        :param other: The other object we are comparing
        :return: True if equal, else False
        """
        return isinstance(other, NoFeeding)

    def __ne__(self, other):
        """
        Compare attributes for testing.
        :param other: The other object we are comparing
        :return: True if not equal, else False
        """
        return not self.__eq__(other)

    def handle_feeding(self, dealer, feeding_player):
        """
        Updates dealer configuration by making this player inactive for this round
        :param dealer: the Dealer object
        :param feeding_player: the PlayerState of the Player choosing how to feed
        """
        feeding_player.active = False

    def convert_to_json(self):
        """
        Converts this NoFeeding to its respective JSON representation
        :return False
        """
        return False


class HerbivoreFeeding(FeedingChoice):
    """
    Represents the Player choosing to feed a single herbivore Species
    """

    def __init__(self, species_index):
        """
        Creates a HerbivoreFeeding
        :param species_index: a Natural representing the index of the Species to be fed
        :return: a HerbivoreFeeding object
        """
        super(HerbivoreFeeding, self).__init__()
        self.species_index = species_index

    def __eq__(self, other):
        """
        Compare attributes for testing.
        :param other: The other object we are comparing
        :return: True if equal, else False
        """
        if isinstance(other, HerbivoreFeeding):
            return self.species_index == other.species_index
        return False

    def __ne__(self, other):
        """
        Compare attributes for testing.
        :param other: The other object we are comparing
        :return: True if not equal, else False
        """
        return not self.__eq__(other)

    def handle_feeding(self, dealer, feeding_player):
        """
        Updates Dealer configuration by feeding an herbivore
        :param dealer: the Dealer object
        :param feeding_player: the PlayerState of the Player choosing how to feed
        """
        herbivore = feeding_player.species[self.species_index]
        assert(herbivore in feeding_player.get_hungry_species(carnivores=False))
        dealer.watering_hole = feeding_player.feed_species(herbivore, dealer.watering_hole)

    def convert_to_json(self):
        """
        Converts this HerbivoreFeeding to its respective JSON representation
        :return JSON Vegetarian as specified by
                http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        return self.species_index


class FatFeeding(FeedingChoice):
    """
    Represents the Player choosing to feed a fat-tissue Species
    """
    def __init__(self, species_index, fat_request):
        """
        Creates a FatFeeding
        :param species_index: a Natural representing the index of the Species to be fed
        :param fat_request: a Natural representing the amount of fat-food requested
        :return: a FatFeeding object
        """
        super(FatFeeding, self).__init__()
        self.species_index = species_index
        self.fat_request = fat_request

    def __eq__(self, other):
        """
        Compare attributes for testing.
        :param other: The other object we are comparing
        :return: True if equal, else False
        """
        if isinstance(other, FatFeeding):
            return all([self.species_index == other.species_index,
                        self.fat_request == other.fat_request])
        return False

    def __ne__(self, other):
        """
        Compare attributes for testing.
        :param other: The other object we are comparing
        :return: True if not equal, else False
        """
        return not self.__eq__(other)

    def handle_feeding(self, dealer, feeding_player):
        """
        Updates dealer configuration by storing fat-food on a fat-tissue Species
        :param dealer: the Dealer object
        :param feeding_player: the PlayerState of the Player choosing how to feed
        """
        fat_species = feeding_player.species[self.species_index]
        assert(fat_species in feeding_player.get_needy_fats() and
               self.fat_request <= min(fat_species.body - fat_species.fat_storage, dealer.watering_hole))

        fat_species.fat_storage += self.fat_request
        dealer.watering_hole -= self.fat_request

    def convert_to_json(self):
        """
        Converts this FatFeeding to its respective JSON representation
        :return JSON FatTissueChoice as specified by
                http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        return [self.species_index, self.fat_request]


class CarnivoreFeeding(FeedingChoice):
    """
    Represents the Player choosing to feed a carnivore Species
    """

    def __init__(self, attacker_index, defending_player_index, defender_index):
        """
        Creates a CarnivoreFeeding
        :param attacker_index: a Natural representing the index of the Species to be fed
        :param defending_player_index: a Natural representing the index of the PlayerState to be attacked
        :param defender_index: a Natural representing the index of the Species on the defending player to be attacked
        :return: a CarnivoreFeeding object
        """
        super(CarnivoreFeeding, self).__init__()
        self.attacker_index = attacker_index
        self.defending_player_index = defending_player_index
        self.defender_index = defender_index

    def __eq__(self, other):
        """
        Compare attributes for testing.
        :param other: The other object we are comparing
        :return: True if equal, else False
        """
        if isinstance(other, CarnivoreFeeding):
            return all([self.attacker_index == other.attacker_index,
                        self.defending_player_index == other.defending_player_index,
                        self.defender_index == other.defender_index])
        return False

    def __ne__(self, other):
        """
        Compare attributes for testing.
        :param other: The other object we are comparing
        :return: True if not equal, else False
        """
        return not self.__eq__(other)

    def handle_feeding(self, dealer, feeding_player):
        """
        Updates dealer configuration by feeding a carnivore, decrementing defender population, and
        handling the resulting auto-feedings
        :param dealer: the Dealer object
        :param feeding_player: the PlayerState of the Player choosing how to feed
        """
        attacker = feeding_player.species[self.attacker_index]
        defending_player = dealer.list_of_players[self.defending_player_index + 1 % len(dealer.list_of_players)]
        defender = defending_player.species[self.defender_index]
        assert(attacker in feeding_player.get_hungry_species(carnivores=True) and
               defender.is_attackable(attacker, defending_player.get_left_neighbor(defender),
                                      defending_player.get_right_neighbor(defender)))

        self.handle_attack_situation(attacker, defender, feeding_player, defending_player, dealer)
        if attacker.population >= MIN_POP:
            dealer.watering_hole = feeding_player.feed_species(attacker, dealer.watering_hole)
            dealer.feed_trait(SCAVENGER)

    def handle_attack_situation(self, attacker, defender, feeding_player, defending_player, dealer):
        """
        Resolves an attack between a carnivorous species and a target species.
        :param attacker: attacking Species
        :param defender: defending Species
        :param feeding_player: PlayerState of attacking player
        :param defending_player: PlayerState of defending player
        :param dealer: Dealer running this game
        """
        self.handle_attacked_species(defender, defending_player, dealer)
        if HORNS in defender.trait_names():
            self.handle_attacked_species(attacker, feeding_player, dealer)

    def handle_attacked_species(self, species, player, dealer):
        """
        Resolves an attack on a target species by modifying their population and checking for extinction
        :param species: a Species harmed in an attack
        :param player: the PlayerState of the player owning the given Species
        """
        species.reduce_population()
        self.handle_extinction(species, player, dealer)

    def handle_extinction(self, species, player, dealer):
        """
        Removes the given species from the player in exchange for TraitCards if the species went extinct in an attack.
        :param species: a Species harmed in an attack
        :param player: the PlayerState of the player owning the given Species
        """
        if species.population < MIN_POP:
            player.species.remove(species)
            dealer.deal_cards(player, EXTINCTION_CARD_AMOUNT)

    def convert_to_json(self):
        """
        Converts this CarnivoreFeeding to its respective JSON representation
        :return JSON CarnivoreChoice as specified by
                http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        return [self.attacker_index, self.defending_player_index, self.defender_index]