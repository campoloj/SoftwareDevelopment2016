from feeding_choice import *
from action import *
from action4 import Action4


class Player(object):
    """
    A data representation of a Player in the Evolution game
    """
    def __init__(self, id=0, player_state=False):
        self.id = id
        self.player_state = player_state

    def start(self, watering_hole, state):
        """
        :effect adds the given state to this players player_state
        :param watering_hole: Natural representing the current food at the watering hole
        :param state: A copy of the current state of the playet
        """
        self.player_state = state

    def choose(self, left_players, right_players):
        """
        Determines the actions the this player wants to perform for this turn.
        :param left_players: the players to the left of this player.
        :param right_players: the players to the right of this player.
        :return: Action4 for the actions they want to perform
        """
        hand = self.player_state.hand
        cards_in_order = sorted(hand, key=lambda card: (card.trait, card.food_points))
        food_action = FoodCardAction(hand.index(cards_in_order[0]))
        add_species_actions = [AddSpeciesAction(hand.index(cards_in_order[1]), [hand.index(cards_in_order[2])])]
        grow_pop_actions = []
        grow_body_actions = []
        replace_trait_actions = []
        new_spec_index = len(self.player_state.species)
        if len(hand) > 3:
            grow_pop_actions.append(GrowAction(POPULATION, new_spec_index, hand.index(cards_in_order[3])))
        if len(hand) > 4:
            grow_body_actions.append(GrowAction(BODY, new_spec_index, hand.index(cards_in_order[4])))
        if len(hand) > 5:
            replace_trait_actions.append(ReplaceTraitAction(new_spec_index, 0, hand.index(cards_in_order[5])))

        return Action4(food_action, grow_pop_actions, grow_body_actions, add_species_actions, replace_trait_actions)

    def next_feeding(self, updated_player, food_available, list_of_players):
        """
        Determines a players next FeedingChoice
        :param updated_player: the PlayerState that needs to be updated for this player.
        :param food_available: the amount of food on the watering hole board
        :param list_of_players: the PlayerStates of other players in the game
        :return: FeedingChoice for the next species to feed
        """
        self.player_state = updated_player
        hungry_fatties = self.player_state.get_needy_fats()
        if hungry_fatties:
            return self.feed_fatty(hungry_fatties, food_available)

        hungry_herbivores = self.player_state.get_hungry_species(carnivores=False)
        if hungry_herbivores:
            return self.feed_herbivores(hungry_herbivores)

        hungry_carnivores = self.player_state.get_hungry_species(carnivores=True)
        if hungry_carnivores:
            return self.feed_carnivore(hungry_carnivores, list_of_players)

    def feed_fatty(self, fat_tissue_species, food_available):
        """
        Feeds a species with the fat-tissue trait
        :param fat_tissue_species: species with a fat-tissue trait
        :param food_available: food on the watering_hole_board
        :return: list of [Species, Nat] where Species is the fat_tissue_species and Nat is the requested food
        """
        fatty = self.largest_fatty_need(fat_tissue_species)
        food_needed = fatty.body - fatty.fat_storage
        food_requested = (food_needed if food_needed < food_available else food_available)
        return FatFeeding(self.player_state.species.index(fatty), food_requested)

    def feed_herbivores(self, hungry_herbivores):
        """
        Feeds a herbivore species
        :param hungry_herbivores: list of hungry herbivores
        :return: the Species to feed
        """
        herbivore = self.sort_by_size(hungry_herbivores)[0]
        return HerbivoreFeeding(self.player_state.species.index(herbivore))

    def feed_carnivore(self, hungry_carnivores, list_of_players):
        """
        Feeds the largest hungry carnivore
        :param hungry_carnivores: list of hungry carnivores
        :param list_of_players: list of all player states
        :return: One of:
                [Carnivore, Defending Player, Defending Species] if there is a valid target in list_of_players' species
                False, if no valid targets and Player chooses not to attack own Species
                None, if no valid targets and is unable to attack own species
        """
        sorted_carnivores = self.sort_by_size(hungry_carnivores)
        for carnivore in sorted_carnivores:
            targets = carnivore.all_attackable_species(list_of_players)
            if targets:
                return self.attack_largest(carnivore, targets, list_of_players)

    def attack_largest(self, attacker, targets, list_of_player):
        """
        Return a CarnivoreFeeding by attacking the largest species in the targets.
        :param attacker: The attacking species
        :param targets: The target species the attacker can attack
        :param list_of_player: The game's list of players
        :return:
        """
        target = self.sort_by_size(targets)[0]
        target_player = next(other_player for other_player in list_of_player if target in other_player.species and
                             other_player is not self.player_state)
        return CarnivoreFeeding(self.player_state.species.index(attacker),
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
