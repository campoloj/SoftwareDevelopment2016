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


class NoFeeding(FeedingChoice):
    """
    Represents the Player choosing to abstain from feeding for the rest of ths round
    """

    def handle_feeding(self, dealer, feeding_player):
        """
        Updates dealer configuration by making this player inactive for this round
        :param dealer: the Dealer object
        :param feeding_player: the PlayerState of the Player choosing how to feed
        """
        feeding_player.is_active = False


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

    def handle_feeding(self, dealer, feeding_player):
        """
        Updates Dealer configuration by feeding an herbivore
        :param dealer: the Dealer object
        :param feeding_player: the PlayerState of the Player choosing how to feed
        """
        herbivore = feeding_player.species[self.species_index]
        assert(herbivore in feeding_player.get_hungry_species(carnivores=False))
        dealer.feed_species(herbivore, feeding_player)


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

    def handle_feeding(self, dealer, feeding_player):
        """
        Updates dealer configuration by feeding a carnivore, decrementing defender population, and
        handling the resulting auto-feedings
        :param dealer: the Dealer object
        :param feeding_player: the PlayerState of the Player choosing how to feed
        """
        attacker = feeding_player.species[self.attacker_index]
        defending_player = dealer.list_of_players[self.defending_player_index % len(dealer.list_of_players)]
        defender = defending_player.species[self.defender_index]
        assert(attacker in feeding_player.get_hungry_species(carnivores=True) and
               defender.is_attackable(attacker, defending_player.get_left_neighbor(defender),
                                      defending_player.get_right_neighbor(defender)))

        dealer.handle_attack_situation(attacker, defender, feeding_player, defending_player)
        if attacker.population >= MIN_POP:
            dealer.feed_species(attacker, feeding_player)
            dealer.handle_scavenging()