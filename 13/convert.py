from dealer.globals import *
from dealer.dealer import Dealer
from dealer.player_state import PlayerState
from dealer.species import Species
from dealer.traitcard import TraitCard
from dealer.action4 import Action4
from dealer.action import *
import json


class Convert(object):
    """
    Methods for converting between JSON input and Python objects
    """
    def __init__(self):
        pass

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

    @classmethod
    def json_to_step4(cls, json_step4):
        """
        Converts a JSON step 4 into a List of Action4 Objects.
        :param json_step4: A JSON Step4 as specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of Action4
        """
        result = []
        for json_action4 in json_step4:
            result.append(cls.json_to_action4(json_action4))
        return result

    @classmethod
    def json_to_action4(cls, json_action4):
        """
        Converts a JSON action into a Action4 Object.
        :param json_action4: A JSON Action4 as specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: Action4
        """
        food_card_action = FoodCardAction(json_action4[0])
        list_of_gp = json_action4[1]
        list_of_gb = json_action4[2]
        list_of_bt = json_action4[3]
        list_of_rt = json_action4[4]
        return Action4(food_card_action, cls.json_to_grow_action(list_of_gp), cls.json_to_grow_action(list_of_gb),
                       cls.json_to_species_action(list_of_bt), cls.json_to_replace_trait_action(list_of_rt))

    @classmethod
    def action4_to_json(cls, action4):
        """
        Converts an Action4 into a JsonAction4 Object.
        :param action4: an Action4
        :return: A JSON Action4 as specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        """
        return [action4.food_card.trade_card_index,
                cls.grow_actions_to_json(action4.grow_pop),
                cls.grow_actions_to_json(action4.grow_body),
                cls.add_species_to_json(action4.add_species),
                cls.replace_trait_to_json(action4.replace_trait)]

    @classmethod
    def json_to_choice_lop(cls, json_los_list):
        """
        Converts a List of List of JSON Species to a List of Player_States
        :param json_los_list: the list of JSON LOS as specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/12.html
        :return: a List of Player_State.
        """
        result = []
        for json_los in json_los_list:
            species_list = []
            for json_spec in json_los:
                species_list.append(cls.json_to_species(json_spec))
            result.append(PlayerState(species=species_list))
        return result

    @classmethod
    def json_to_grow_action(cls, list_of_json_grow):
        """
        Converts a List of JSON grow actions to a List of GrowActions
        :param list_of_json_grow: a List of GP or GB specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of GrowAction
        """
        result = []
        for json_grow in list_of_json_grow:
            result.append(GrowAction(json_grow[0], json_grow[1], json_grow[2]))
        return result


    @classmethod
    def grow_actions_to_json(cls, list_of_grow_actions):
        """
        Converts a List of JSON grow actions to a List of GrowActions
        :param list_of_grow_actions: a List of GrowActions
        :return: a List of GP or GB specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        """
        result = []
        for grow_action in list_of_grow_actions:
            result += [grow_action.attribute, grow_action.species_board_index, grow_action.trade_card_index]
        return result

    @classmethod
    def json_to_species_action(cls, list_of_bt):
        """
        Converts a List of JSON bt to a List of AddSpeciesActions
        :param list_of_bt: a List of BT specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of AddSpeciesAction
        """
        result = []
        for bt in list_of_bt:
            traits = []
            for i in range(1, len(bt)):
                traits.append(bt[i])
            result.append(AddSpeciesAction(bt[0], traits))
        return result

    @classmethod
    def add_species_to_json(cls, list_of_species_actions):
        """
        Converts a list of AddSpeciesActions to List of Json BT
        :param list_of_species_actions: List of AddSpeciesAction
        :return: list_of_bt: a List of BT specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        """
        result = []
        for species_action in list_of_species_actions:
            result += [species_action.trade_card_index] + species_action.add_card_list
        return result

    @classmethod
    def json_to_replace_trait_action(cls, list_of_rt):
        """
        Converts a List of JSON RT actions to a List of ReplaceTraitActions
        :param list_of_rt: a List of RT specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        :return: List of ReplaceTraitActions
        """
        result = []
        for rt in list_of_rt:
            result.append(ReplaceTraitAction(rt[0], rt[1], rt[2]))
        return result

    @classmethod
    def replace_trait_to_json(cls, list_of_replace_actions):
        """
        Converts a List of ReplaceTraitActions to a JSON List of RT
        :param list_of_replace_actions:
        :return: List of RT specified by the data definition at
                           http://www.ccs.neu.edu/home/matthias/4500-s16/11.html
        """
        result = []
        for replace_action in list_of_replace_actions:
            result += [replace_action.species_board_index,
                       replace_action.card_to_replace_index,
                       replace_action.replacement_card_index]
        return result


    @classmethod
    def json_to_feeding(cls, json_feeding):
        """
        Converts a JSON Feeding into a Python representation of a Feeding
        :param json_feeding: a Feeding as specified by the data definition at
                             http://www.ccs.neu.edu/home/matthias/4500-s16/6.html
        :return: [PlayerState, Natural+, [PlayerState,...]] representing the attacking PlayerState,
                the available watering hole food, and the PlayerStates of other players in the game
        """
        assert(len(json_feeding) == FEEDING_LENGTH)
        [json_player, wh_food, json_lop] = json_feeding
        assert(wh_food > MIN_WATERING_HOLE)
        player = cls.json_to_player(json_player)
        other_players = [cls.json_to_player(op) for op in json_lop]
        return [player, wh_food, other_players]

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
