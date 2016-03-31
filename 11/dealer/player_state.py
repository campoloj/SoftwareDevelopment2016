import gui
from globals import *
from feeding_choice import HerbivoreFeeding, NoFeeding
from traitcard import TraitCard
from species import Species


class PlayerState(object):
    """
    Represents data about the player that is kept track of by the dealer
    in order to prevent the player from modifying their data or acting out of turn
    the dealer only sends the minimum amount of data needed for the player to make
    choices
    """
    def __init__(self, name=0, food_bag=0, hand=False, species=False, active=True):
        """
        Creates a PlayerState
        :param name: The players ID
        :param food_bag: The amount of food the player has.
        :param hand: A List of TraitCards the player has.
        :param species: A List of Species the player has.
        :param active: Boolean, True if the player is still feeding in the current round.
        :return:
        """
        self.name = name
        self.food_bag = food_bag
        self.hand = hand if hand else []
        self.species = species if species else []
        self.active = active

    def equal_attributes(self, other):
        """
        Determine if this PlayerState and the given PlayerState have the same attributes for testing purposes.
        :param other: the PlayerState to compare this PlayerState to
        :return: True if all attributes are equal, else False
        """
        species_equal = isinstance(other, PlayerState) and len(self.species) == len(other.species)
        for i in range(len(self.species)):
            species_equal = species_equal and self.species[i].equal_attributes(other.species[i])
        return all([self.name == other.name,
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

    def grow_attribute(self, grow_action):
        """
        :effect Grow the specified attribute in the given GrowAction and removes the card from the players hand.
        :param grow_action: GrowAction to apply to this player_state
        """
        species_to_grow = self.species[grow_action.species_board_index]
        if grow_action.attribute == POPULATION:
            species_to_grow.population += GROW_POP_AMOUNT
        elif grow_action.attribute == BODY:
            species_to_grow.body += GROW_BODY_AMOUNT

    def add_species(self, add_card_list):
        """
        :effect Adds a new species to the right of this Player State's current species
        :param add_card_list: List of Nat representing indicies of Trait Cards in this Player State's hand to add to the
                              new species.
        """
        trait_list = [self.hand[i] for i in add_card_list]
        self.species.append(Species(traits=trait_list))

    def replace_trait(self, replace_action):
        """
        :effect Replaces the trait on one of this PlayerState's species according to the given ReplaceTraitAction
        :param replace_action: a ReplaceTraitAction specifying which TraitCards to replace on which Species
        """
        species = self.species[replace_action.species_board_index]
        replacement_card = self.hand[replace_action.replacement_card_index]
        species.replace_trait(replace_action.card_to_replace_index, replacement_card)

    def discard_all(self, remove_card_list):
        """
        :effect Removes each card simultaneously in the list of indecies given
        :param remove_card_list: List of Nat representing the indicies of the Trait Cards to remove in
                                 this Player State's Hand.
        """
        for i in remove_card_list:
            self.hand[i] = False
        self.hand = [card for card in self.hand if card]

    @classmethod
    def validate_all_cards(cls, list_of_players, total_deck):
        """
        Validates the TraitCards of all PlayerStates in the given list
        :param list_of_players: a list of PlayerState objects to be validated
        :param total_deck: a list of TraitCards representing all valid card possibilities
        :raise ValueError if duplicate cards or invalid cards exist on any player
        """
        for player in list_of_players:
            player.validate_cards(total_deck)

    def validate_cards(self, total_deck):
        """
        Validates that the TraitCards in this PlayerState's hand and on its Species boards are all possible
        and unique
        :param total_deck: a list of TraitCards representing all valid card possibilities
        :raise ValueError if duplicate or invalid cards exist on this player
        """
        TraitCard.validate_all_unique(self.hand, total_deck)
        Species.validate_all_cards(self.species, total_deck)

    @classmethod
    def validate_all_attributes(cls, list_of_players):
        """
        Validates the attributes of all PlayerStates in the given list
        :param list_of_players: list of PlayerState objects to be validated
        :raise AssertionError if any PlayerState has invalid attributes
        """
        for player in list_of_players:
            player.validate_attributes()

    def validate_attributes(self):
        """
        Validates the attributes of this PlayerState
        :raise AssertionError if any attributes are out of bounds
        """
        assert(isinstance(self.name, int) and self.name >= MIN_PLAYER_ID)
        assert(isinstance(self.food_bag, int) and self.food_bag >= MIN_FOOD_BAG)
        assert(isinstance(self.hand, list))
        TraitCard.validate_all_attributes(self.hand)
        assert(isinstance(self.species, list))
        Species.validate_all_attributes(self.species)

    def show_changes(self, other_player):
        """
        Creates a string representation of the changed attributes between a PlayerState before and after
        an imperative function is called on it.
        :param other_player: The PlayerState after it has been modified
        :return: String of attribute changes, or "" if unchanged.
        """
        changes = []
        if self.name != other_player.name:
            changes += CHANGE_TEMPLATE % ("name", str(self.name), str(other_player.name))
        if self.food_bag != other_player.food_bag:
            changes += CHANGE_TEMPLATE % ("food_bag", str(self.food_bag), str(other_player.food_bag))
        changes += "hand: %s" % TraitCard.show_all_changes(self.hand, other_player.hand)

        if self.active != other_player.active:
            changes += CHANGE_TEMPLATE % ("active", self.active, other_player.active)

    def display(self):
        """
        Displays this PlayerState configuration in a graphical window
        """
        text = gui.render_player(self)
        gui.display(text)



