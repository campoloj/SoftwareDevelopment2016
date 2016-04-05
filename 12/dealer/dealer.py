import gui

from globals import *
from player_state import PlayerState
from species import Species
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
        players_equal = isinstance(other, Dealer) and len(self.list_of_players) == len(other.list_of_players)
        for i in range(len(self.list_of_players)):
            players_equal = players_equal and self.list_of_players[i].equal_attributes(other.list_of_players[i])
        return all([players_equal,
                    self.watering_hole == other.watering_hole,
                    self.deck == other.deck])


# ======================================  Utility Methods ===========================================

    @classmethod
    def create_initial(cls, loxp):
        """
        Creates an initial Dealer object with PlayerStates for each of the given external Players
        and a complete, shuffled deck.
        :param loxp: List of Player objects representing external players
        :return: Dealer object ready to begin a game.
        """
        return Dealer(list_of_players=cls.make_playerstates(loxp), watering_hole=0, deck=cls.make_deck())

    @classmethod
    def make_playerstates(cls, loxp):
        """
        Creates a PlayerState for each of the given external Players
        :return: List of PlayerState objects representing internal players
        """
        lop = []
        for x in range(len(loxp)):
            lop.append(PlayerState(name=x + 1, ext_player=loxp[x]))
        return lop

    @classmethod
    def make_deck(cls):
        """
        Makes a full, sorted deck of TraitCards
        :return: list of TraitCards
        """
        deck = []
        for trait in TRAITS_LIST:
            food_range = (CARN_FOOD_MAX if trait == CARNIVORE else HERB_FOOD_MAX)
            for food_val in range(-food_range, food_range + 1):
                deck.append(TraitCard(trait, food_val))
        deck = sorted(deck, key=lambda card: (card.trait, card.food_points))
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

# ======================================  Step 1 Methods ============================================

    def step1(self):
        """
        The dealer hands each external player the necessary pieces at the beginning of a turn:
        a species board (if needed) and additional cards to play the turn.
        :effect: Updates internal PlayerStates with additional TraitCards and possible Species
        """
        for player in self.list_of_players:
            self.start(player)

    def start(self, player):
        """
        Handles the start of a turn by dealing cards and a new Species (if necessary) to the given PlayerState
        :param player: the PlayerState being dealt to
        :effect: Updates given PlayerState with additional TraitCards and possible Species
        """
        new_cards = self.cards_to_deal(player)
        opt_species = (False if player.species else Species())
        player.start(opt_species, new_cards)

    def cards_to_deal(self, player):
        """
        Gives the necessary amount of cards to deal to the given PlayerState at the beginning of the turn
        and removes them from the deck.
        :param player: the PlayerState being dealt to
        :return: List of TraitCard
        """
        amount = DEAL_AMOUNT + len(player.species)
        cards_to_deal = self.deck[:amount]
        self.deck = self.deck[amount:]
        return cards_to_deal

# ======================================  Step 2/3 Methods ==========================================

    def step2n3(self):
        """
        Gathers requests from each external Player of how they wish to use the cards in their hands
        :return: List of Action4 corresponding to the current PlayerState order
        """
        return [player.choose(self.public_players(False)) for player in self.list_of_players]

# ======================================  Step 4 Methods ============================================

    def step4(self, action4_list):
        """
        Applies Action4s to the corresponding PlayerStates and executes the feeding cycle.
        Also reorders the PlayerStates to prepare for the next turn.
        :param action4_list: The list of actions to apply to the corresponding indicies of players
        """
        self.step4i(action4_list)
        self.feeding()

    def step4i(self, action4_list):
        """
        Applies each Action4 to the PlayerState of the Player who chose it. Handles resulting auto
        feedings.
        :param action4_list: List of Action4 corresponding to the current PlayerState order
        :effect: Updates all PlayerStates based on the Actions they choose
        """
        for i in range(len(action4_list)):
            action4_list[i].validate_hand(self.list_of_players[i])
            action4_list[i].apply_all(self, self.list_of_players[i])
        self.validate_attributes()
        self.foodcard_reveal()

    def foodcard_reveal(self):
        """
        :effect Adds population to fertile Species and feeds long-neck Species after the food cards
                on the watering hole have been revealed
        """
        self.modify_fertiles()
        self.feed_long_necks()

    def modify_fertiles(self):
        """
        :effect Adds population to all fertile Species
        """
        for player in self.list_of_players:
            for species in player.species:
                if FERTILE in species.trait_names():
                    species.population += GROW_POP_AMOUNT

    def feed_long_necks(self):
        """
        :effect Feeds all long-neck Species
        """
        for player in self.list_of_players:
            for species in player.species:
                if LONGNECK in species.trait_names():
                    self.feed_species(species, player)

    def feeding(self):
        """
        Executes a feeding cycle until the watering hole runs out or no Players can still feed
        :effect: Updates PlayerStates based on auto-feedings or the Player's FeedingChoices
        """
        next_player_id = self.list_of_players[1].name
        while self.watering_hole > MIN_WATERING_HOLE and any([player.active for player in self.list_of_players]):
            self.feed1()
        self.order_players(next_player_id)

    def feed1(self):
        """
        This Dealer handles one step in the feeding cycle by modifying its configuration according to
        an auto-feeding or the first player's FeedingChoice.
        """
        player = self.list_of_players[0]
        if player.active:
            other_players = self.public_players(feeding_player=player)
            feeding_choice = player.next_feeding(self.watering_hole, other_players)
            feeding_choice.handle_feeding(self, player)
        self.list_of_players.append(self.list_of_players.pop(0))

    def public_players(self, feeding_player):
        """
        Creates a copy of this Dealer's list of players, excluding the specified feeding player, so that
        the feeding player may choose which player to attack without having access to their private fields.
        :param feeding_player: The PlayerState of the player feeding
        :return: a list of public representations of PlayerStates
        """
        return [PlayerState(name=player.name, food_bag=False, hand=False, species=player.species)
                for player in self.list_of_players
                if player != feeding_player]

    def order_players(self, first_player_id):
        """
        :effect Reorders the PlayerStates based on the given first_player_id
        :param first_player_id: The name of the PlayerState that should be first in the list
        """
        while self.list_of_players[0].name is not first_player_id:
            self.list_of_players.append(self.list_of_players.pop(0))


# ======================================   Feeding Methods ==========================================

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

    def show_changes(self, dealer2):
        """
        Shows a string representation of the differences between this Dealer and the given Dealer.
        :param dealer2: The Dealer we are comparing to this Dealer
        :return: String
        """
        changes = []
        old_players = self.players_to_dict()
        new_players = dealer2.players_to_dict()
        for i in range(0, len(self.list_of_players)):
            name = self.list_of_players[i].name
            old_player = old_players.get(name)
            new_player = new_players.get(name)
            if not old_player.equal_attributes(new_player):
                changes.append('Player ' + str(name) + ':' + old_player.show_changes(new_player))
        if self.watering_hole != dealer2.watering_hole:
            changes.append(CHANGE_TEMPLATE % ('watering_hole', self.watering_hole, dealer2.watering_hole))
        deck_changes = TraitCard.show_all_changes(self.deck, dealer2.deck)
        if deck_changes:
            changes.append('deck :' + deck_changes)
        return ", ".join(changes)



    def players_to_dict(self):
        """
        Returns a dictionary of player ID's with their player state.
        :return: Dictionary {Nat: Player State, .... }
        """
        result = {}
        for player in self.list_of_players:
            result[player.name] = player
        return result


# ======================================   GUI Methods ===========================================

    def display(self):
        """
        Displays this Dealer's current configuration in a graphical window
        """
        text = gui.render_dealer(self)
        gui.display(text)