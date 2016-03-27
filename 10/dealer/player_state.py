import gui
from globals import *
from feeding_choice import HerbivoreFeeding, NoFeeding


class PlayerState(object):
    """
    Represents data about the player that is kept track of by the dealer
    in order to prevent the player from modifying their data or acting out of turn
    the dealer only sends the minimum amount of data needed for the player to make
    choices
    """
    def __init__(self, name=0, food_bag=0, hand=None, species=None, active=True):
        self.name = name
        self.food_bag = food_bag
        self.hand = hand if hand else []
        self.species = species if species else []
        self.active = active

    def __str__(self):
        return "PlayerState(Food=%d, Hand=%s, Species=%s" % (self.food_bag, self.hand, self.species)

    def __eq__(self, other):
        species_equal = True
        for spec in self.species:
            if len(self.species) != len(other.species):
                return False
            elif not other.species[self.species.index(spec)].equal_attributes(spec):
                species_equal = False
        return all([isinstance(other, PlayerState),
                    self.name == other.name,
                    self.food_bag == other.food_bag,
                    self.hand == other.hand,
                    species_equal])

    def attempt_auto_feed(self, list_of_players):
        """
        Automatically creates a FeedingChoice for this player if they have no needy fat-tissue species, no
        carnivores that are able to attack, and only one vegetarian.
        :param list_of_players: List of PlayerStates for all game players
        :return: a FeedingChoice if player is able to be auto-fed, else False
        """
        if self.get_needy_fats() or self.any_attackers(list_of_players):
            return False
        else:
            hungry_herbivores = self.get_hungry_species(carnivores=False)
            if not hungry_herbivores:
                return NoFeeding()
            elif len(hungry_herbivores) == 1:
                return HerbivoreFeeding(species_index=self.species.index(hungry_herbivores[0]))
            else:
                return False

    def any_attackers(self, list_of_players):
        """
        Determines if this player has any hungry carnivores able to attack another species,
        implying that they must make a decision rather than be auto-fed.
        :param list_of_players: List of PlayerState representing eligible targets for an attack
        :return: True if the Player has a carnivore able to attack, else False
        """
        hungry_carnivores = self.get_hungry_species(carnivores=True)
        for attacker in hungry_carnivores:
            if attacker.all_attackable_species(list_of_players):
                return True
        return False

    def get_left_neighbor(self, species):
        """
        Gets the left neighbor of the given Species in the list of species for this player
        :param species: Species of which to find neighbor
        :return: The Species to the left of the given Species
        """
        species_index = self.species.index(species)
        return False if species_index == 0 else self.species[species_index - 1]

    def get_right_neighbor(self, species):
        """
        Gets the right neighbor of the given Species in the list of species for this player
        :param species: Species of which to find neighbor
        :return: The Species to the right of the given Species
        """
        species_index = self.species.index(species)
        return False if species_index == len(self.species) - 1 else self.species[species_index + 1]

    def get_hungry_species(self, carnivores=False):
        """
        Gets any hungry species in this player's species in the desired group.
        :param carnivores: True if only carnivores are desired,
                            else False if only herbivores are desired
        :return: List of Species, Where species are hungry herbivores.
        """
        return [species for species in self.species
                if (CARNIVORE in species.trait_names() if carnivores else CARNIVORE not in species.trait_names()) and
                species.food < species.population]

    def get_needy_fats(self):
        """
        Gets any needy species that have a Fat-tissue trait.
        :return: List of Species, Where species fat-tissue is not full
        """
        return [species for species in self.species
                if FATTISSUE in species.trait_names() and
                species.fat_storage < species.body]

    @classmethod
    def validate_all(cls, list_of_players, total_deck):
        """
        Validates all players in the given list.
        :param list_of_players: a list of PlayerState objects to be validated
        :param total_deck: a list of TraitCards representing all valid card possibilities
        :raise: ValueError if duplicate cards or invalid cards exist on any player
                AssertionError if duplicate traits exist on any player's species boards
        """
        for player in list_of_players:
            player.validate(total_deck)

    def validate(self, total_deck):
        """
        Validates this player by checking that each card in its hand and on its species boards is unique and valid
        by removing them from the given deck of possible cards
        :param total_deck: a list of TraitCards representing all valid card possibilities
        :raise: ValueError if duplicate cards or invalid cards exist on this player
                AssertionError if duplicate traits exist on any of this player's species boards
        """
        TraitCard.validate_all(self.hand, total_deck)
        Species.validate_all(self.species, total_deck)

    def display(self):
        """
        Displays this PlayerState configuration in a graphical window
        """
        text = gui.render_player(self)
        gui.display(text)

