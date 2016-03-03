import os
import sys

from player_state import PlayerState
globals_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "..%s" % os.sep)
sys.path.append(globals_path)

from globals import *


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
            feeding = cls.feed_fatty(hungry_fatties, food_available)
            return [player.species.index(feeding[0]), feeding[1]]

        hungry_herbivores = player.get_hungry_species(carnivores=False)
        if hungry_herbivores:
            feeding = cls.feed_herbivores(hungry_herbivores)
            return player.species.index(feeding)

        hungry_carnivores = player.get_hungry_species(carnivores=True)
        if hungry_carnivores:
            feeding = cls.feed_carnivore(hungry_carnivores, player, list_of_players)
            if feeding:
                attacking_species_index = player.species.index(feeding[0])
                defending_player_index = list_of_players.index(feeding[1])
                defending_species_index = feeding[1].species.index(feeding[2])
                return [attacking_species_index, defending_player_index, defending_species_index]
            else:
                return feeding

    @classmethod
    def feed_fatty(cls, fat_tissue_species, food_available):
        """
        Feeds a species with the fat-tissue trait
        :param fat_tissue_species: species with a fat-tissue trait
        :param food_available: food on the watering_hole_board
        :return: list of [Species, Nat] where Species is the fat_tissue_species and Nat is the requested food
        """
        fatty = cls.largest_fatty_need(fat_tissue_species)
        food_needed = fatty.body - fatty.fat_storage
        food_requested = (food_needed if food_needed < food_available else food_available)
        return [fatty, food_requested]

    @classmethod
    def feed_herbivores(cls, hungry_herbivores):
        """
        Feeds a herbivore species
        :param hungry_herbivores: list of hungry herbivores
        :return: the Species to feed
        """
        return cls.sort_by_size(hungry_herbivores)[0]

    @classmethod
    def feed_carnivore(cls, hungry_carnivores, player_state, list_of_player):
        """
        Feeds the largest hungry carnivore
        :param hungry_carnivores: list of hungry carnivores
        :param player_state: the current player state
        :param list_of_player: list of all player states
        :return: One of:
                [Carnivore, Defending Player, Defending Species] if there is a valid target in list_of_players' species
                False, if no valid targets and Player chooses not to attack own Species
                None, if no valid targets and is unable to attack own species
        """
        sorted_carnivores = cls.sort_by_size(hungry_carnivores)
        for carnivore in sorted_carnivores:
            targets = []
            for player in list_of_player:
                if player == player_state:
                    continue
                for defender in player.species:
                    left_neighbor = player.get_left_neighbor(defender)
                    right_neighbor = player.get_right_neighbor(defender)
                    if defender.is_attackable(carnivore, left_neighbor, right_neighbor):
                        targets.append(defender)
            if targets:
                target = cls.sort_by_size(targets)[0]
                target_player = next(player for player in list_of_player if target in player.species)
                return [carnivore, target_player, target]

        for carnivore in sorted_carnivores:
            for defender in player_state.species:
                if carnivore == defender:
                    continue
                if defender.is_attackable(carnivore,
                                          player_state.get_left_neighbor(defender),
                                          player_state.get_right_neighbor(defender)):
                    return False

        return None


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
        if len(list_of_species) == 1:
            return list_of_species[0]
        else:
            max_need = max([species.population - species.food for species in list_of_species])

        highest_needers = [species for species in list_of_species
                           if species.population - species.food == max_need]
        return cls.sort_by_size(highest_needers)[0]

