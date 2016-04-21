import gui
from globals import *
from feeding_choice import *
from traitcard import TraitCard
from species import Species
from copy import *


class PlayerState(object):
    """
    Represents data about the player that is kept track of by the dealer
    in order to prevent the player from modifying their data or acting out of turn
    the dealer only sends the minimum amount of data needed for the player to make
    choices
    """
    def __init__(self, name=0, food_bag=0, hand=False, species=False, active=True, ext_player=False):
        """
        Creates a PlayerState
        :param name: The players ID
        :param food_bag: The amount of food the player has.
        :param hand: A List of TraitCards the player has.
        :param species: A List of Species the player has.
        :param active: Boolean, True if the player is still feeding in the current round.
        :param extplayer: the Player that this state represents and their strategy
        :return:
        """
        self.name = name
        self.food_bag = food_bag
        self.hand = hand if hand else []
        self.species = species if species else []
        self.active = active
        self.ext_player = ext_player

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
                    self.active == other.active,
                    species_equal])

    def get_score(self):
        """
        Determine this players score. A players score is the total of:
            - (1) food tokens in the food bag,
            - (2) The population on his existing species, and
            - (3) number of trait cards associated with these species.
        :return: Nat representing this players score
        """
        score = self.food_bag
        for spec in self.species:
            score += spec.population + len(spec.traits)
        return (self.ext_player.id, score)

# ======================================  Step 1 Methods ============================================

    def start(self, watering_hole, new_species, new_cards):
        """
        :effect Updates this state by adding the new species board if it exists and adding the new trait cards
                to the hand. Then gives the new state to the external player.
        :param watering_hole: Natural representing the food currently at the watering hole
        :param new_species: the optional new_species to add to the board.
        :param new_cards: the appropriate number of cards to add to the had
        """
        if new_species:
            self.species.append(new_species)
        self.hand += new_cards
        state_copy = self
        self.ext_player.start(watering_hole, state_copy)

    def deal_amount(self):
        """
        Determines the number of cards to be dealt to this PlayerState at the start of a turn.
        :return: Natural
        """
        return DEAL_AMOUNT + max(1, len(self.species))

# ======================================  Step 2/3 Methods ==========================================

    def choose(self, public_players):
        """
        :effect Splits the public players into left and right lists of this player_state and gives it to
                their external player to make a action choice.
        :param public_players: A list of all the players without their hand or food_bag.
        :return: the ext_players Action4 for this turn
        """
        left_players = []
        right_players = []
        list_length = len(public_players)
        for i in range(0, list_length):
            if public_players[i].name is self.name:
                if i + 1 != list_length:
                    right_players = public_players[i + 1:]
                if i != 0:
                    left_players = public_players[:i]

        return self.ext_player.choose(left_players, right_players)

# ======================================  Step 4 Methods ============================================

    def next_feeding(self, watering_hole, other_players):
        """
        :effect Returns the feeding of this player_state's external player
        :param watering_hole: Nat the food on the watering_hole
        :param other_players: List_of_players that have the food_bag and hand wiped out.
        :return: Feeding_Choice that the external player chooses
        """
        feeding = self.attempt_auto_feed(watering_hole, other_players)
        if not feeding:
            state_copy = self
            feeding = self.ext_player.next_feeding(state_copy, watering_hole, other_players)
        return feeding

    def attempt_auto_feed(self, watering_hole, other_players):
        """
        Automatically creates a FeedingChoice for this player
        It will automatically feed
            -- a single species with a non-full fat-food trait card
               (to the max possible)
            -- a single vegetarian
            -- a single carnivore that can attack only one species
               from a different player (no self-attack is allowed).
        :param other_players: List of PlayerStates for other, attackable Players
        :return: a FeedingChoice if player is able to be auto-fed, else False
        """
        fatties = self.get_needy_fats()
        herbivores = self.get_hungry_species(carnivores=False)
        carnivores = self.get_hungry_species(carnivores=True)
        if not (fatties or herbivores or carnivores):
            return NoFeeding()
        elif len(fatties) == 1 and not (herbivores or carnivores):
            fatty = fatties[0]
            return FatFeeding(self.species.index(fatty),
                              min(fatty.body - fatty.fat_storage, watering_hole))
        elif len(herbivores) == 1 and not (carnivores or fatties):
            return HerbivoreFeeding(self.species.index(herbivores[0]))
        elif len(carnivores) == 1 and not (fatties or herbivores):
            return self.carnivore_auto_feeding(carnivores[0], other_players)
        return False

    def carnivore_auto_feeding(self, carnivore, other_players):
        """
        Determines the auto-feeding for this PlayerState's single carnivore, if possible
        :param carnivore: Species with carnivore trait attempting to auto-feed
        :param other_players: List of PlayerStates for other, attackable Players
        :return: a FeedingChoice if Carnivore an auto-feed, else False
        """
        targets = carnivore.all_attackable_species(other_players)
        if not targets:
            return NoFeeding()
        elif len(targets) == 1:
            def_player = next(player for player in other_players if targets[0] in player.species)
            return CarnivoreFeeding(self.species.index(carnivore),
                                    other_players.index(def_player),
                                    def_player.species.index(targets[0]))
        return False

    def get_attackable_species(self, attacker):
        """
        Find all species belonging to the given player that are attackable by this carnivore species
        :param attacker: the attacking species
        :return: List of Species objects attackable by the given attacker
        """
        attackable_species = []
        for defender in self.species:
            if self == defender:
                continue
            if defender.is_attackable(attacker, self.get_left_neighbor(defender), self.get_right_neighbor(defender)):
                attackable_species.append(defender)
        return attackable_species

    def end_turn(self):
        """
        Adjust species populations, remove extinct species, move food from species to food bag of this PlayerState
        :return: Natural representing amount of cards to be dealt due to extinct species
        """
        for species in self.species:
            self.food_bag += species.consolidate_food()
        return self.remove_extinct()

    def remove_extinct(self):
        """
        Removes extinct species from this PlayerState
        :return: Natural representing amount of cards to be dealt due to extinct species
        """
        card_amount, survivors = 0, []
        for species in self.species:
            if species.population == 0:
                card_amount += EXTINCTION_CARD_AMOUNT
            else:
                survivors.append(species)
        self.species = survivors
        return card_amount

    def move_fat(self):
        """
        Effect: Moves the fat from the fat-storage to food for species that it applies.
        """
        for species in self.species:
            species.move_fat()

    def modify_fertiles(self):
        """
        :effect Adds population to all fertile Species in this player
        """
        for species in self.species:
            species.modify_if_fertile()

    def feed_trait(self, watering_hole, trait):
        """
        :effect Feeds all Species with the given trait
        :param watering_hole: The food left in the watering hole
        :param trait: The trait we are looking for in the species list
        :return Nat representing the remaining food on the watering hole
        """

        for species in self.species:
            if species.has_trait(trait):
                watering_hole = self.feed_species(species, watering_hole)
        return watering_hole

    def feed_species(self, species, watering_hole, allow_forage=True):
        """
        Feed the species and set off foraging and cooperation.
        :param species: The species being fed
        :param watering_hole: The food remaining on the watering hole
        :param allow_forage: True if the given species has not foraged yet
        :return: Nat representing the remaining food on the watering hole
        """
        feed = species.feed(watering_hole)
        if feed == watering_hole:
            return watering_hole

        watering_hole = feed

        if species.has_trait(FORAGING) and allow_forage:
            watering_hole = self.feed_species(species, watering_hole, allow_forage=False)

        if species.has_trait(COOPERATION):
            right_neighbor = self.get_right_neighbor(species)
            if right_neighbor:
                watering_hole = self.feed_species(right_neighbor, watering_hole)

        return watering_hole


# ======================================  Species Methods ============================================

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
                if (species.has_trait(CARNIVORE) if carnivores else not species.has_trait(CARNIVORE)) and
                species.is_hungry()]

    def get_needy_fats(self):
        """
        Gets any needy species that have a Fat-tissue trait.
        :return: List of Species, Where species fat-tissue is not full
        """
        return [species for species in self.species
                if species.has_trait(FATTISSUE) and
                species.fat_storage < species.body]

# ======================================  Action Methods ============================================

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

# ====================================  Validation Methods ==========================================

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
            changes.append(CHANGE_TEMPLATE % ("name", str(self.name), str(other_player.name)))
        if self.food_bag != other_player.food_bag:
            changes.append(CHANGE_TEMPLATE % ("food_bag", str(self.food_bag), str(other_player.food_bag)))
        hand_changes = TraitCard.show_all_changes(self.hand, other_player.hand)
        if hand_changes:
            changes.append(hand_changes)
        species_changes = Species.show_all_changes(self.species, other_player.species)
        if species_changes:
            changes.append(species_changes)
        if self.active != other_player.active:
            changes.append(CHANGE_TEMPLATE % ("active", self.active, other_player.active))
        return ", ".join(changes)

    def display(self):
        """
        Displays this PlayerState configuration in a graphical window
        """
        text = gui.render_player(self)
        gui.display(text)



