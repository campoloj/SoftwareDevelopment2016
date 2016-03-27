from dealer.globals import *
from dealer.dealer import Dealer
from dealer.player_state import PlayerState
from dealer.species import Species
from dealer.traitcard import TraitCard


class Convert(object):
    """
    Methods for converting between JSON input and Python objects
    """
    def __init__(self):
        pass

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
