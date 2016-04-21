from dealer.globals import *
from dealer.dealer import Dealer
from dealer.player_state import PlayerState
from dealer.species import Species
from dealer.traitcard import TraitCard
from dealer.action4 import Action4
from dealer.action import *
import time
from dealer.feeding_choice import *
import json


class Convert(object):
    """
    Methods for reading JSON and converting between JSON input and Python objects
    """
    def __init__(self):
        pass

# ======================================  JSON Reading ==========================================

    @classmethod
    def json_parser(cls, buffer):
        """
        Searches for full JSON messages and adds incomplete messages to a buffer
        :param buffer: the previous lines of incomplete JSON messages
        :return: a tuple of (list-of-correct_JSON_messages, current buffer)
        """
        decoder = json.JSONDecoder()
        decoded_json = []
        try:
            while True:
                (json_obj, end_index) = decoder.raw_decode(buffer)
                decoded_json.append(json_obj)
                buffer = buffer[end_index:]
        except:
            return (decoded_json, buffer)

    @classmethod
    def listen(cls, socket, time_out=TIMEOUT):
        """
        Waits for the first valid json message from the socket and returns it.
        Returns if no message is received in the min time allowed.
        :param time_out: Int representing time to wait before exiting, or False if no timeout
        :return: first complete JSON message read
        """
        buffer = ""
        decoded_json = []
        start_time = time.time()
        while not decoded_json:
            buffer += socket.recv(1024).strip()
            (decoded_json, buffer) = Convert.json_parser(buffer)
            if time_out and time.time() - start_time > TIMEOUT:
                return ""
        return decoded_json[0]

# ======================================  Dealer ==========================================

    @classmethod
    def json_to_dealer(cls, json_config):
        """
        Converts a JSON Configuration into a Dealer object
        :param json_config: A JSON Configuration as specified by the data definition at
                            http://www.ccs.neu.edu/home/matthias/4500-s16/8.html
        :return: a Dealer object
        """
        assert(len(json_config) == CONFIG_LENGTH)
        [json_lop, wh_food, json_deck] = json_config
        lop = [cls.json_to_player(json_player) for json_player in json_lop]
        deck = [cls.json_to_trait(trait_card) for trait_card in json_deck]
        dealer = Dealer(lop, wh_food, deck)
        dealer.validate_attributes()
        return dealer

    @classmethod
    def dealer_to_json(cls, dealer):
        """
        Converts a Dealer object into a JSON Configuration
        :param dealer: a Dealer object
        :return: a JSON Configuration as specified by the data definition at
                 http://www.ccs.neu.edu/home/matthias/4500-s16/8.html
        """
        dealer.validate_attributes()

        json_players = [cls.player_to_json(player) for player in dealer.list_of_players]
        json_deck = [cls.trait_to_json(trait_card) for trait_card in dealer.deck]
        return [json_players, dealer.watering_hole, json_deck]

# ======================================  Actions ==========================================

    @classmethod
    def json_to_step4(cls, json_step4):
        """
        Converts a JSON Step4 into a List of Action4 Objects.
        :param json_step4: A JSON Step4 as specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of Action4
        """
        return [cls.json_to_action4(json_action4) for json_action4 in json_step4]

    @classmethod
    def json_to_action4(cls, json_action4):
        """
        Converts a JSON action into a Action4 Object.
        :param json_action4: A JSON Action4 as specified by http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: Action4
        """
        [food_card, list_of_gp, list_of_gb, list_of_bt, list_of_rt] = json_action4
        return Action4(cls.json_to_food_action(food_card), cls.json_to_gp(list_of_gp), cls.json_to_gb(list_of_gb),
                       cls.json_to_species_action(list_of_bt), cls.json_to_replace_trait_action(list_of_rt))

    @classmethod
    def json_to_food_action(cls, json_food_card):
        """
        Converts a JSON food card into a FoodCardAction
        :param json_food_card: Nat representing JSON food card
        :return: FoodCardAction object
        """
        return FoodCardAction(json_food_card)

    @classmethod
    def json_to_gp(cls, list_of_gp):
        """
        Converts a List of JSON GP into a List of GrowAction
        :param list_of_gp: List of GP as specified by http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of GrowAction objects
        """
        return [GrowAction(POPULATION, gp[0], gp[1]) for gp in list_of_gp]

    @classmethod
    def json_to_gb(cls, list_of_gb):
        """
        Converts a List of JSON GB into a List of GrowAction
        :param list_of_gb: List of GB as specified by http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of GrowAction objects
        """
        return [GrowAction(BODY, gb[0], gb[1]) for gb in list_of_gb]

    @classmethod
    def json_to_species_action(cls, list_of_bt):
        """
        Converts a List of JSON BT into a List of AddSpeciesActions
        :param list_of_bt: a List of BT as specified by http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of AddSpeciesAction
        """
        return [AddSpeciesAction(bt[0], (bt[1:] if len(bt) > 1 else [])) for bt in list_of_bt]

    @classmethod
    def json_to_replace_trait_action(cls, list_of_rt):
        """
        Converts a List of JSON RT into a List of ReplaceTraitActions
        :param list_of_rt: a List of RT as specified by http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of ReplaceTraitActions
        """
        return [ReplaceTraitAction(rt[0], rt[1], rt[2]) for rt in list_of_rt]

# ======================================  Feeding ==========================================

    @classmethod
    def json_to_feeding_choice(cls, json_fc):
        """
        Converts a JSON FeedingChoice to a FeedingChoice object
        :param json_fc: a JSON FeedingChoice as specified at
                        http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        :return: FeedingChoice object
        """
        if json_fc is False:
            return NoFeeding()
        elif isinstance(json_fc, int):
            return HerbivoreFeeding(json_fc)
        elif isinstance(json_fc, list):
            if len(json_fc) == 2:
                return FatFeeding(json_fc[0], json_fc[1])
            elif len(json_fc) == 3:
                return CarnivoreFeeding(json_fc[0], json_fc[1], json_fc[2])
        else:
            raise AssertionError

# ======================================  PlayerState ==========================================

    @classmethod
    def json_to_player(cls, json_player):
        """
        Converts a JSON Player+ to a PlayerState
        :param json_player: a JSON Player+ as specified by the data definition at
                            http://www.ccs.neu.edu/home/matthias/4500-s16/8.html
        :return: a PlayerState object
        """
        gdict = globals()
        if len(json_player) == PLAYER_LENGTH:
            [[gdict[ID], player_id], [gdict[SPECIES], json_los], [gdict[BAG], food_bag]] = json_player
            cards = []
        else:
            [[gdict[ID], player_id], [gdict[SPECIES], json_los],
             [gdict[BAG], food_bag], [gdict[CARDS], cards]] = json_player

        player_species = [cls.json_to_species(json_species) for json_species in json_los]
        player_hand = [cls.json_to_trait(trait_card) for trait_card in cards]
        player_obj = PlayerState(name=player_id, hand=player_hand, food_bag=food_bag, species=player_species)
        player_obj.validate_attributes()
        return player_obj

    @classmethod
    def player_to_json(cls, player):
        """
        Converts a PlayerState to a JSON Player+. Does not render empty hands.
        :param player: a PlayerState object
        :return: a JSON Player+ as specified by the data definition at
                 http://www.ccs.neu.edu/home/matthias/4500-s16/8.html
        """
        player.validate_attributes()
        json_species = [cls.species_to_json(species_obj) for species_obj in player.species]
        json_hand = [cls.trait_to_json(trait_card) for trait_card in player.hand]
        json_player = [[ID, player.name], [SPECIES, json_species], [BAG, player.food_bag]]
        if json_hand:
            json_player.append([CARDS, json_hand])
        return json_player

# ----------------------------- Players as Lists of Species Boards ----------------------------

    @classmethod
    def json_to_choice_lop(cls, json_los_list):
        """
        Converts a List of List of JSON Species to a List of PlayerStates
        :param json_los_list: the list of JSON LOS as specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/12.html
        :return: a List of PlayerState.
        """
        return [cls.json_boards_to_player(jboards) for jboards in json_los_list]

    @classmethod
    def players_to_all_json(cls, lop_left, lop_right):
        """
        Converts two lists of PlayerStates to a [LOB, LOB]
        :param lop_left: List of PlayerState to the left of the choosing player
        :param lop_right: List of PlayerState to the right of the choosing player
        :return: [LOB, LOB] as specified by
                http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        lob_left = [cls.player_to_json_boards(player) for player in lop_left]
        lob_right = [cls.player_to_json_boards(player) for player in lop_right]
        return [lob_left, lob_right]

    @classmethod
    def json_boards_to_player(cls, jboards):
        """
        Convert a JSON Boards to a List of PlayerStates
        :param jboards: a JSON Boards as specified in
                        http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        :return: a PlayerState object
        """
        species = [cls.json_to_species(jspecies) for jspecies in jboards]
        return PlayerState(species=species)

    @classmethod
    def player_to_json_boards(cls, player):
        """
        Converts a PlayerState to a JSON Boards
        :param player: a PlayerState object
        :return: a JSON Boards as specified in
                http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        return [cls.species_to_json(species_obj) for species_obj in player.species]

# ----------------------------- Players as States ----------------------------

    @classmethod
    def player_to_rp_json(cls, player):
        """
        Converts a PlayerState to a remote protocol JSON state
        :param player: a PlayerState object
        :return: a remote protocol JSON state as specified in
                http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        player.validate_attributes()
        json_species = [cls.species_to_json(species_obj) for species_obj in player.species]
        json_hand = [cls.trait_to_json(trait_card) for trait_card in player.hand]
        return [player.food_bag, json_species, json_hand]

    @classmethod
    def rp_json_to_player(cls, rp_json):
        """
        Converts a remote protocol JSON player state to a PlayerState
        :param rp_json: a remote protocol JSON state as specified in
                        http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        :return: a PlayerState object
        """
        [food_bag, json_species, json_hand] = rp_json
        assert(isinstance(food_bag, int) and food_bag >= MIN_FOOD_BAG)
        species = [cls.json_to_species(jspecies) for jspecies in json_species]
        hand = [cls.json_to_trait(jtrait) for jtrait in json_hand]
        return PlayerState(food_bag=food_bag, hand=hand, species=species)

    @classmethod
    def json_to_state(cls, json_state):
        """
        Converts a watering hole and remote protocol JSON player state to a Integer and PlayerState
        :param json_state: a remote protocol JSON state with watering hole as specified in
                            http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        :return: [Integer, PlayerState object]
        """
        watering_hole = json_state.pop(0)
        player = cls.rp_json_to_player(json_state)
        assert(isinstance(watering_hole, int) and watering_hole >= MIN_WATERING_HOLE)
        return [watering_hole, player]

    @classmethod
    def json_to_gamestate(cls, jgamestate):
        """
        Converts a JSON State to a game state
        :param jgamestate: a JSON State as specified in
                        http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        :return: [PlayerState, Natural, List of PlayerState]
        """
        player = cls.rp_json_to_player(jgamestate[:3])
        watering_hole, jboards = jgamestate[3:]
        assert(isinstance(watering_hole, int) and watering_hole > MIN_WATERING_HOLE)
        other_players = cls.json_to_choice_lop(jboards)
        return [player, watering_hole, other_players]

    @classmethod
    def gamestate_to_json(cls, player, watering_hole, other_players):
        """
        Converts a public representation of the game state to a JSON State for feeding
        :param player: feeding PlayerState
        :param watering_hole: Natural+ representing food available
        :param other_players: List of PlayerState representing other players in game
        :return: a JSON State as specified in
                 http://www.ccs.neu.edu/home/matthias/4500-s16/r_remote.html
        """
        assert(isinstance(watering_hole, int) and watering_hole > MIN_WATERING_HOLE)
        state = cls.player_to_rp_json(player)
        other_players = [cls.player_to_json_boards(op) for op in other_players]
        state += [watering_hole, other_players]
        return state

# ======================================  Species ==========================================

    @classmethod
    def json_to_species(cls, json_species):
        """
        Converts a JSON Species+ into a Species.
        :param json_species: a JSON Species+ as specified by the data definition at
                             http://www.ccs.neu.edu/home/matthias/4500-s16/6.html
        :return: a Species object
        """
        gdict = globals()
        if len(json_species) == SPECIES_LENGTH:
            [[gdict[FOOD], species_food], [gdict[BODY], species_body], [gdict[POPULATION], species_pop],
             [gdict[TRAITS], json_species_traits]] = json_species
            fat_food = False
        else:
            [[gdict[FOOD], species_food], [gdict[BODY], species_body], [gdict[POPULATION], species_pop],
             [gdict[TRAITS], json_species_traits], [gdict[FATFOOD], fat_food]] = json_species

        species_traits = [cls.json_to_trait(trait) for trait in json_species_traits]
        species_obj = Species(species_pop, species_food, species_body, species_traits, fat_food)
        species_obj.validate_attributes()
        return species_obj

    @classmethod
    def species_to_json(cls, species_obj):
        """
        Converts a Species object into a JSON Species+. Does not render empty fat-food.
        :param species_obj: a Species object
        :return: a JSON Species+ as specified by the data definition at
                 http://www.ccs.neu.edu/home/matthias/4500-s16/6.html
        """
        species_obj.validate_attributes()
        json_traits = [cls.trait_to_json(trait) for trait in species_obj.traits]
        json_species = [[FOOD, species_obj.food], [BODY, species_obj.body],
                        [POPULATION, species_obj.population], [TRAITS, json_traits]]
        if species_obj.fat_storage:
            json_species.append([FATFOOD, species_obj.fat_storage])
        return json_species

# ======================================  TraitCard ==========================================

    @classmethod
    def json_to_trait(cls, json_trait):
        """
        Converts a JSON Trait or SpeciesCard into a TraitCard
        :param json_trait: a JSON Trait or SpeciesCard as specified by the data definitions at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/5.html and
                           http://www.ccs.neu.edu/home/matthias/4500-s16/8.html, respectively.
        :return: a TraitCard object
        """
        if isinstance(json_trait, basestring):
            [food, trait] = [False, json_trait]
        else:
            [food, trait] = json_trait
        trait_card = TraitCard(trait, food)
        trait_card.validate_attributes()
        return trait_card

    @classmethod
    def trait_to_json(cls, trait_card):
        """
        Converts a TraitCard into a JSON Trait or SpeciesCard
        :param trait_card: a TraitCard object
        :return: a JSON Trait or SpeciesCard as specified by the data definitions at
                 http://www.ccs.neu.edu/home/matthias/4500-s16/5.html and
                 http://www.ccs.neu.edu/home/matthias/4500-s16/8.html, respectively.
        """
        trait_card.validate_attributes()
        return trait_card.trait if trait_card.food_points is False else [trait_card.food_points, trait_card.trait]
