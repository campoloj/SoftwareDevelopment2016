from feeding_choice import *

class Player(object):
    """
    A data representation of a Player in the Evolution game
    """
    def __init__(self):
        pass

    @classmethod
    def next_feeding(cls, player, food_available, list_of_players):
        """
        Determines a players next Feeding
        A Feeding is one of
            - None, meaning the Player is unable to feed this turn
            - False, meaning the Player refuses to attack own species and forgoes feeding this turn
            - Natural, meaning the index of a herbivore to feed
            - [Natural, Nat], meaning the index of a fat-tissue species and the food requested
            - [Natural, Natural, Natural], meaning the index of the carnivore to feed, the index of the defending
                                           Player, and the index of the defending Species in the defending Player's hand
        :param player: the PlayerState of the player who is feeding
        :param food_available: the amount of food on the watering hole board
        :param list_of_players: the PlayerStates of other players in the game
        :return: Feeding for the next species to feed
        """
        hungry_fatties = player.get_needy_fats()
        if hungry_fatties:
            return cls.feed_fatty(hungry_fatties, food_available, player)

        hungry_herbivores = player.get_hungry_species(carnivores=False)
        if hungry_herbivores:
            return cls.feed_herbivores(hungry_herbivores, player)

        hungry_carnivores = player.get_hungry_species(carnivores=True)
        if hungry_carnivores:
            return cls.feed_carnivore(hungry_carnivores, player, list_of_players)


    @classmethod
    def feed_fatty(cls, fat_tissue_species, food_available, player):
        """
        Feeds a species with the fat-tissue trait
        :param fat_tissue_species: species with a fat-tissue trait
        :param food_available: food on the watering_hole_board
        :return: list of [Species, Nat] where Species is the fat_tissue_species and Nat is the requested food
        """
        fatty = cls.largest_fatty_need(fat_tissue_species)
        food_needed = fatty.body - fatty.fat_storage
        food_requested = (food_needed if food_needed < food_available else food_available)
        return FatFeeding(player.species.index(fatty), food_requested)

    @classmethod
    def feed_herbivores(cls, hungry_herbivores, player):
        """
        Feeds a herbivore species
        :param hungry_herbivores: list of hungry herbivores
        :return: the Species to feed
        """
        herbivore = cls.sort_by_size(hungry_herbivores)[0]
        return HerbivoreFeeding(player.species.index(herbivore))

    @classmethod
    def feed_carnivore(cls, hungry_carnivores, player, list_of_player):
        """
        Feeds the largest hungry carnivore
        :param hungry_carnivores: list of hungry carnivores
        :param player: the current player state
        :param list_of_player: list of all player states
        :return: One of:
                [Carnivore, Defending Player, Defending Species] if there is a valid target in list_of_players' species
                False, if no valid targets and Player chooses not to attack own Species
                None, if no valid targets and is unable to attack own species
        """
        sorted_carnivores = cls.sort_by_size(hungry_carnivores)
        for carnivore in sorted_carnivores:
            targets = cls.get_targets(carnivore, player, list_of_player)
            if targets:
                return cls.attack_largest(carnivore, targets, player, list_of_player)

        if cls.any_attackable(sorted_carnivores, player):
            return NoFeeding()

    @classmethod
    def any_attackable(cls, sorted_carnivores, player):
        """
        Determine if the players species are attackable by any of the sorted_carnivores
        :param sorted_carnivores: The carnivore species that are attacking
        :param player: The player that we are looking to attack
        :return: True if any of the player's species can be attacked by any of the sorted_carnivores
        """
        for carnivore in sorted_carnivores:
            for defender in player.species:
                if carnivore == defender:
                    continue
                if defender.is_attackable(carnivore,
                                          player.get_left_neighbor(defender),
                                          player.get_right_neighbor(defender)):
                    return True

    @classmethod
    def get_targets(cls, carnivore, player, list_of_player):
        """
        Get a list of target attackable species in other players species list.
        :param carnivore: The attacking species
        :param player: The player attacking
        :param list_of_player: The total list of players in the game
        :return: List of Species that are attackable by the carnivore and not in the players species.
        """
        targets = []
        for other_player in list_of_player:
            if other_player == player:
                continue
            for defender in other_player.species:
                left_neighbor = other_player.get_left_neighbor(defender)
                right_neighbor = other_player.get_right_neighbor(defender)
                if defender.is_attackable(carnivore, left_neighbor, right_neighbor):
                    targets.append(defender)
        return targets

    @classmethod
    def attack_largest(cls, attacker, targets, player, list_of_player):
        """
        Return a CarnivoreFeeding by attacking the largest species in the targets.
        :param attacker: The attacking species
        :param targets: The target species the attacker can attack
        :param player: The player that is attacking
        :param list_of_player: The game's list of players
        :return:
        """
        target = cls.sort_by_size(targets)[0]
        target_player = next(other_player for other_player in list_of_player if target in other_player.species and
                             other_player is not player)
        return CarnivoreFeeding(player.species.index(attacker),
                                list_of_player.index(target_player),
                                target_player.species.index(target))

    @classmethod
    def sort_by_size(cls, list_of_species):
        """
        Returns the Species objects ordered largest to smallest according to the order specified
        :param list_of_species: a list of Species objects
        :return: a list of Species objects ordered by size
        """
        return sorted(list_of_species,
                      key=lambda species: (species.population, species.food,
                                           species.body, -list_of_species.index(species)),
                      reverse=True)

    @classmethod
    def largest_fatty_need(cls, list_of_species):
        """
        Determines which species has a greater need for fat-tissue food
        :param list_of_species: list of Species with the fat-tissue trait
        :return: Species with greatest fat-tissue need (highest population - food)
        """
        max_need = max([species.body - species.fat_storage for species in list_of_species])
        highest_needers = [species for species in list_of_species
                           if species.body - species.fat_storage == max_need]
        return cls.sort_by_size(highest_needers)[0]

    @classmethod
    def display(cls, player_state):
        """
        Displays the configuration of the given PlayerState for a Player in a graphical window
        :param player_state: The PlayerState object representing this Player's configuration
        """
        player_state.display()

