import random
import gui

from globals import *
from player import Player
from player_state import PlayerState
from traitcard import TraitCard
from feeding_choice import HerbivoreFeeding, NoFeeding


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

    def feed1(self, player):
        """
        This Dealer handles one step in the feeding cycle by modifying its configuration according to
        an auto-feeding or the given player's FeedingChoice.
        :param player: the PlayerState of the feeding player
        """
        if self.watering_hole == MIN_WATERING_HOLE:
            return
        feeding_choice = self.attempt_auto_feed(player)
        if not feeding_choice:
            other_players = self.public_players(feeding_player=player)
            feeding_choice = Player.next_feeding(player, self.watering_hole, other_players)

        feeding_choice.handle_feeding(self, player)

    def attempt_auto_feed(self, player):
        """
        Automatically creates a FeedingChoice for a player if they have no needy fat-tissue species, no
        carnivores that are able to attack, and only one vegetarian.
        :param player: the PlayerState of the feeding player
        :return: a FeedingChoice if player is able to be auto-fed, else False
        """
        if not (player.get_needy_fats() or self.any_attackers(player)):
            hungry_herbivores = player.get_hungry_species(carnivores=False)
            if not hungry_herbivores:
                return NoFeeding()
            elif len(hungry_herbivores) == 1:
                return HerbivoreFeeding(species_index=player.species.index(hungry_herbivores[0]))
            else:
                return False

    def any_attackers(self, player):
        """
        Determines if the given Player has any hungry carnivores able to attack another species,
        implying that they must make a decision rather than be auto-fed.
        :param player: The PlayerState of the player feeding
        :return: True if the Player has a carnivore able to attack, else False
        """
        hungry_carnivores = player.get_hungry_species(carnivores=True)
        for attacker in hungry_carnivores:
            for player in self.list_of_players:
                for defender in player.species:
                    if defender == attacker:
                        continue
                    if defender.is_attackable(attacker, player.get_left_neighbor(defender),
                                              player.get_right_neighbor(defender)):
                        return True
        return False

    def public_players(self, feeding_player):
        """
        Creates a copy of this Dealer's list of players, excluding the specified feeding player, so that
        the feeding player may choose which player to attack without having access to their private fields.
        :param feeding_player: The PlayerState of the player feeding
        :return: a list of public representations of PlayerStates
        """
        return [PlayerState(name=player.name, food_bag=False, hand=False, species=player.species)
                for player in self.list_of_players if player != feeding_player]

    def handle_attack(self, attacker, defender, feeding_player, defending_player):
        """
        Resolves an attack between a carnivorous species and a target species.
        :param attacker: attacking Species
        :param defender: defending Species
        :param feeding_player: PlayerState of attacking player
        :param defending_player: PlayerState of defending player
        """
        self.reduce_population(defender, defending_player)
        if HORNS in defender.trait_names():
            self.reduce_population(attacker, feeding_player)

    def reduce_population(self, species, player):
        """
        Reduces the population of a species harmed in an attack and removes them from the player in exchange for
        TraitCards if the given species goes extinct.
        :param species: a Species harmed in an attack
        :param player: the PlayerState of the player owning the given Species
        """
        species.population -= KILL_QUANTITY
        if species.population < MIN_POP:
            player.species.remove(species)
            self.deal_cards(player, EXTINCTION_CARD_AMOUNT)

    def deal_cards(self, player, amount):
        """
        Deals the given amount of TraitCards from the deck to the given player
        :param player: the PlayerState of the player being dealt cards
        :param amount: Natural specifying how many cards to deal
        """
        for i in range(amount):
            player.hand.append(self.deck.pop(0))

    def handle_scavenging(self, feeding_player):
        """
        Feeds any Species with the Scavenger trait after a carnivore attack, starting from the feeding player
        :param feeding_player: the PlayerState of the feeding player
        """
        feeding_player_index = self.list_of_players.index(feeding_player)
        for x in range(feeding_player_index, feeding_player_index + len(self.list_of_players)):
            player = self.list_of_players[x % len(self.list_of_players)]
            for species in player.species:
                if SCAVENGER in species.trait_names():
                    self.feed_species(species, player)

    def feed_species(self, species, player, allow_forage=True):
        """
        Feeds the given species and any others according to its traits.
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

    def validate(self):
        """
        Validates game constraints for Dealer and PlayerStates
        :raise ValueError if duplicate cards exist, AssertionError if species have duplicate traits
        """
        total_deck = Dealer.make_deck()
        for card in self.deck:
            total_deck.remove(card)

        for player in self.list_of_players:
            for card in player.hand:
                total_deck.remove(card)

            for species in player.species:
                assert(len(species.trait_names()) == len(set(species.trait_names())))
                for card in species.traits:
                    if card.food_points is None:
                        continue
                    total_deck.remove(card)

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

    def display(self):
        """
        Displays this Dealer's current configuration in a graphical window
        """
        text = gui.render_dealer(self)
        gui.display(text)
