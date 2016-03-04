from globals import *
from player import Player
from player_state import PlayerState


class Dealer(object):

    def __init__(self, list_of_players, watering_hole, deck):
        self.list_of_players = list_of_players
        self.watering_hole = watering_hole
        self.deck = deck

    def feed1(self, player):
        """
        Deals with one step in the feeding cycle.
        - Decides whether it can transfer a token of food (or several) from the watering hole to the current player
        automatically or whether it is necessary to query the next player;

        - Transfers food, by interpreting the answer from a player if necessary;

        - Removes the player from the sequence or rotate the sequence of players, as needed.

        Will be called  as long as there is food in the watering hole and species that may wish to take additional food.
        :param player: The player who is feeding
        :returns: self: and updated self
        """
        if self.watering_hole == MIN_WATERING_HOLE:
            return

        hungry_herbivores = player.get_hungry_species(carnivores=False)
        hungry_carnivores = player.get_hungry_species(carnivores=True)
        needy_fats = player.get_needy_fats()
        carnivores_can_attack = self.any_attackers(hungry_carnivores)
        if not hungry_herbivores and not needy_fats and not carnivores_can_attack:
            return

        feed_result = None
        if len(hungry_herbivores) == 1 and not carnivores_can_attack and not needy_fats:
            feed_result = player.species.index(hungry_herbivores[0])

        if feed_result is None:
            public_players = self.get_public_players(player_id=player.name)
            feed_result = Player.next_feeding(player, self.watering_hole, public_players)

        tracked_player = self.list_of_players[self.list_of_players.index(player)]
        self.handle_feed_result(feed_result, tracked_player)

    def handle_feed_result(self, feed_result, feeding_player):
        """
        Updates dealer configuration based on feeding result.
        :param feed_result: The result from the feeding_players feeding
        :param feeding_player: The player feeding
        """
        if feed_result is False:
            feeding_player.active = False
            return

        if isinstance(feed_result, int):
            self.handle_herbivore_feeding(feed_result, feeding_player)

        elif isinstance(feed_result, list) and len(feed_result) == 2:
            self.handle_fat_feeding(feed_result, feeding_player)

        elif isinstance(feed_result, list) and len(feed_result) == 3:
            self.handle_carnivore_feeding(feed_result, feeding_player)

    def handle_herbivore_feeding(self, feed_result, feeding_player):
        """
        Updates dealer configuration by feeding an herbivore
        :param feed_result: Nat, the index of the herbivore to feed
        :param feeding_player: The player feeding
        """
        herbivore = feeding_player.species[feed_result]
        assert(herbivore in feeding_player.get_hungry_species(carnivores=False))
        self.feed_species(herbivore, feeding_player)

    def handle_fat_feeding(self, feed_result, feeding_player):
        """
        Updates dealer configuration by storing fat on a fat-tissue Species
        :param feed_result: [Nat, Nat] where the first Nat is the index of the fat-tissue Species and
                                       the second is the amount of food requested
        :param feeding_player: The player feeding
        """
        fat_index = feed_result[0]
        fat_tokens = feed_result[1]
        fat_species = feeding_player.species[fat_index]
        assert(fat_species in feeding_player.get_needy_fats() and
               fat_tokens <= min(fat_species.body - fat_species.fat_storage, self.watering_hole))
        fat_species.fat_storage += fat_tokens
        self.watering_hole -= fat_tokens

    def handle_carnivore_feeding(self, feed_result, feeding_player):
        """
        Updates dealer configuration by feeding a carnivore and decrementing the defender's population
        :param feed_result: [Nat, Nat, Nat] where the first Nat is the index of the carnivore,
                                            the second is the index of the defending player,
                                            and the third is the index of the defending Species
        :param feeding_player: The player feeding
        """
        public_players = self.get_public_players(feeding_player.name)
        defending_player_id = public_players[feed_result[1]].name
        attacker = feeding_player.species[feed_result[0]]
        defending_player = next(player for player in self.list_of_players if player.name == defending_player_id)
        defender = defending_player.species[feed_result[2]]
        assert(attacker in feeding_player.get_hungry_species(carnivores=True) and
               defender.is_attackable(attacker, defending_player.get_left_neighbor(defender),
                                      defending_player.get_right_neighbor(defender)))
        defender.population -= 1
        if defender.population == 0:
            defending_player.species.remove(defender)
        if HORNS in defender.trait_names():
            attacker.population -= 1
            if attacker.population == 0:
                feeding_player.species.remove(attacker)
                return
        self.feed_species(attacker, feeding_player)
        self.handle_scavenging()

    def handle_scavenging(self):
        """
        Feeds any Species with the Scavenger trait after a Carnivore attack
        """
        for player in self.list_of_players:
            for species in player.species:
                if SCAVENGER in species.trait_names() and species.is_hungry() and self.watering_hole > 0:
                    self.feed_species(species, player)

    def feed_species(self, species, player):
        """
        Feed given species and handle auto-feeding
        :param species: The Species being fed
        :param player: The PlayerState who owns the Species
        """
        species.food += 1
        self.watering_hole -= 1
        forage = (FORAGING in species.trait_names() and species.is_hungry())
        if forage and self.watering_hole > 0:
            species.food += 1
            self.watering_hole -= 1
        if COOPERATION in species.trait_names() and self.watering_hole > 0:
            right_neighbor = player.get_right_neighbor(species)
            if right_neighbor and right_neighbor.is_hungry():
                self.feed_species(right_neighbor, player)

    def any_attackers(self, hungry_carnivores):
        """
        Returns true of any of the give carnivores and attack any species on the board.
        :param hungry_carnivores: A list of hungry sprecies with the Carnivore trait
        :return: True if any can attack else False
        """
        for attacker in hungry_carnivores:
            for player in self.list_of_players:
                for defender in player.species:
                    if defender == attacker:
                        continue
                    if defender.is_attackable(attacker, player.get_left_neighbor(defender),
                                              player.get_right_neighbor(defender)):
                        return True
        return False

    def get_public_players(self, player_id=0):
        """
        Produce a copy of the list of players. Each copies player in the list (except for the choosing player)
        will have no food_bag and no hand so that when given for a feeding the player
        feeding won't have that information
        :param player_id: Id of player to maintain private fields
        :return: List of Player_States
        """
        result = []
        for player in self.list_of_players:
            if player_id == player.name:
                result.append(player)
            else:
                result.append(PlayerState(name=player.name, food_bag=None, species=player.species))
        return result

    def equal_attributes(self, other):
        """
        Return True if this dealer and the given dealer have the same attributes.
        :param other: The other species
        :return: Boolean
        """
        return all([isinstance(other, Dealer),
                    self.list_of_players == other.list_of_players,
                    self.watering_hole == other.watering_hole,
                    self.deck == other.deck])
