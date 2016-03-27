import random
import gui

from globals import *
from player import Player
from player_state import PlayerState
from traitcard import TraitCard


class Dealer(object):
    """
    Represents the Dealer in a game of Evolution.
    """

    def __init__(self, list_of_players, watering_hole, deck):
        """
        Creates a Dealer
        :param list_of_players: list of PlayerStates for each player involved in the game
        :param watering_hole: Natural representing the amount of food available at the watering hole
        :param deck: list of TraitCards held by the dealer
        :return: a Dealer object
        """
        self.list_of_players = list_of_players
        self.watering_hole = watering_hole
        self.deck = deck

    def equal_attributes(self, other):
        """
        Determines if this Dealer and another dealer have the same attributes for the purpose of testing.
        :param other: the Dealer to compare this Dealer to
        :return: True if all attributes are the same, else False
        """
        return all([isinstance(other, Dealer),
                    self.list_of_players == other.list_of_players,
                    self.watering_hole == other.watering_hole,
                    self.deck == other.deck])


# ======================================  Utility Methods ===========================================

    @classmethod
    def make_deck(cls):
        """
        Makes a full, shuffled deck of TraitCards
        :return: list of TraitCards
        """
        deck = []
        for trait in TRAITS_LIST:
            food_range = (CARN_FOOD_MAX if trait == CARNIVORE else HERB_FOOD_MAX)
            for food_val in range(-food_range, food_range):
                deck.append(TraitCard(trait, food_val))
        random.shuffle(deck)
        return deck

    def deal_cards(self, player, amount):
        """
        Deals the given amount of TraitCards from the deck to the given player
        Stops short if the deck runs out of cards.
        :param player: the PlayerState of the player being dealt cards
        :param amount: Natural specifying how many cards to deal
        """
        while amount and self.deck:
            player.hand.append(self.deck.pop(0))
            amount -= 1


# ======================================   Feeding Methods ===========================================

    def feed1(self, player):
        """
        This Dealer handles one step in the feeding cycle by modifying its configuration according to
        an auto-feeding or the given player's FeedingChoice.
        :param player: the PlayerState of the feeding player
        """
        if self.watering_hole == MIN_WATERING_HOLE:
            return
        feeding_choice = player.attempt_auto_feed(self.list_of_players)
        if not feeding_choice:
            other_players = self.public_players(feeding_player=player)
            feeding_choice = Player.next_feeding(player, self.watering_hole, other_players)

        feeding_choice.handle_feeding(self, player)

    def public_players(self, feeding_player):
        """
        Creates a copy of this Dealer's list of players, excluding the specified feeding player, so that
        the feeding player may choose which player to attack without having access to their private fields.
        :param feeding_player: The PlayerState of the player feeding
        :return: a list of public representations of PlayerStates
        """
        return [PlayerState(name=player.name, food_bag=False, hand=False, species=player.species)
                for player in self.list_of_players if player != feeding_player]

    def feed_species(self, species, player, allow_forage=True):
        """
        Feeds the given species, and any others if necessary due to its traits.
        :param species: The Species being fed
        :param player: the PlayerState of the player who owns the species
        :param allow_forage: True if this Species has not yet eaten its forage food, else False
        """
        if not species.is_hungry() or self.watering_hole <= MIN_WATERING_HOLE:
            return

        species.food += FEED_QUANTITY
        self.watering_hole -= FEED_QUANTITY

        if FORAGING in species.trait_names() and allow_forage:
            self.feed_species(species, player, allow_forage=False)

        if COOPERATION in species.trait_names():
            right_neighbor = player.get_right_neighbor(species)
            if right_neighbor:
                self.feed_species(right_neighbor, player)


# -----------------------------------   Carnivore Feed Methods --------------------------------------

    def handle_attack_situation(self, attacker, defender, feeding_player, defending_player):
        """
        Resolves an attack between a carnivorous species and a target species.
        :param attacker: attacking Species
        :param defender: defending Species
        :param feeding_player: PlayerState of attacking player
        :param defending_player: PlayerState of defending player
        """
        self.handle_attacked_species(defender, defending_player)
        if HORNS in defender.trait_names():
            self.handle_attacked_species(attacker, feeding_player)

    def handle_attacked_species(self, species, player):
        """
        Resolves an attack on a target species by modifying their population and checking for extinction
        :param species: a Species harmed in an attack
        :param player: the PlayerState of the player owning the given Species
        """
        species.reduce_population()
        self.handle_extinction(species, player)

    def handle_extinction(self, species, player):
        """
        Removes the given species from the player in exchange for TraitCards if the species went extinct in an attack.
        :param species: a Species harmed in an attack
        :param player: the PlayerState of the player owning the given Species
        """
        if species.population < MIN_POP:
            player.species.remove(species)
            self.deal_cards(player, EXTINCTION_CARD_AMOUNT)

    def handle_scavenging(self):
        """
        Feeds any species with the Scavenger trait after a carnivore attack
        """
        for player in self.list_of_players:
            self.feed_scavengers(player)

    def feed_scavengers(self, player):
        """
        Feeds all of the given player's scavenger species after a carnivore attack
        :param player: the PlayerState of the player to feed scavenger species
        """
        for species in player.species:
            if SCAVENGER in species.trait_names():
                self.feed_species(species, player)


# ======================================   Validation Methods ===========================================

    def validate_cards(self):
        """
        Validates that all cards known by this dealer are valid possibilities and unique
        :raise: ValueError if duplicate or invalid cards exist
        """
        total_deck = Dealer.make_deck()
        TraitCard.validate_all_unique(self.deck, total_deck)
        PlayerState.validate_all_cards(self.list_of_players, total_deck)

    def validate_attributes(self):
        """
        Validates the attributes of this Dealer
        :raise AssertionError if any attributes are out of bounds
        """
        assert(isinstance(self.list_of_players, list) and LOP_MAX >= len(self.list_of_players) >= LOP_MIN)
        PlayerState.validate_all_attributes(self.list_of_players)
        assert(isinstance(self.watering_hole, int) and self.watering_hole >= MIN_WATERING_HOLE)
        assert(isinstance(self.deck, list) and LOC_MAX >= len(self.deck))
        TraitCard.validate_all_attributes(self.deck)


# ======================================   GUI Methods ===========================================

    def display(self):
        """
        Displays this Dealer's current configuration in a graphical window
        """
        text = gui.render_dealer(self)
        gui.display(text)
