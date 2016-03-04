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
        assert(len(json_config) == CONFIG_LENGTH)
        [json_lop, wh_food, json_deck] = json_config
        assert(all([LOP_MIN <= len(json_lop) <= LOP_MAX, wh_food >= MIN_WATERING_HOLE, len(json_deck) <= LOC_MAX]))
        lop = [cls.json_to_player(json_player) for json_player in json_lop]
        deck = [cls.json_to_trait(trait_card) for trait_card in json_deck]
        dealer = Dealer(lop, wh_food, deck)
        return dealer

    @classmethod
    def dealer_to_json(cls, dealer):
        assert(all([LOP_MIN <= len(dealer.list_of_players) <= LOP_MAX,
                    dealer.watering_hole >= MIN_WATERING_HOLE,
                    len(dealer.deck) <= LOC_MAX]))
        json_players = [cls.player_to_json(player) for player in dealer.list_of_players]
        json_deck = [cls.trait_to_json(trait_card) for trait_card in dealer.deck]
        return [json_players, dealer.watering_hole, json_deck]

    @classmethod
    def json_to_feeding(cls, json_feeding):
        assert(len(json_feeding) == FEEDING_LENGTH)
        [json_player, wh_food, json_lop] = json_feeding
        assert(wh_food > MIN_WATERING_HOLE)
        player = cls.json_to_player(json_player)
        other_players = [cls.json_to_player(op) for op in json_lop]
        return [player, wh_food, other_players]

    @classmethod
    def json_to_player(cls, json_player):
        if len(json_player) == PLAYER_LENGTH:
            [[globals()[ID], player_id], [globals()[SPECIES], json_los], [globals()[BAG], food_bag]] = json_player
            cards = []
        elif len(json_player) == PLAYER_PLUS_LENGTH:
            [[globals()[ID], player_id], [globals()[SPECIES], json_los], [globals()[BAG], food_bag], globals()[CARDS], cards] = json_player
        else:
            raise AssertionError

        assert(all([player_id >= MIN_PLAYER_ID, food_bag >= MIN_FOOD_BAG,
                    isinstance(player_id, int), isinstance(food_bag, int),
                    isinstance(json_los, list), isinstance(cards, list)]))

        player_species = [cls.json_to_species(json_species) for json_species in json_los]
        if cards:
            cards = [cls.json_to_trait(trait_card) for trait_card in cards]
        player_obj = PlayerState(name=player_id, hand=cards, food_bag=food_bag, species=player_species)
        return player_obj

    @classmethod
    def player_to_json(cls, player):
        assert(all([player.name >= MIN_PLAYER_ID, player.food_bag >= MIN_FOOD_BAG,
                    isinstance(player.name, int), isinstance(player.food_bag, int),
                    isinstance(player.species, list), isinstance(player.hand, list)]))
        json_species = [cls.species_to_json(species_obj) for species_obj in player.species]
        json_hand = [cls.trait_to_json(trait_card) for trait_card in player.hand]
        json_player = [[ID, player.name], [SPECIES, json_species], [BAG, player.food_bag]]
        if json_hand:
            json_player.append([CARDS, json_hand])
        return json_player


    @classmethod
    def json_to_species(cls, json_species):
        if len(json_species) == SPECIES_LENGTH:
            [[globals()[FOOD], species_food], [globals()[BODY], species_body],
             [globals()[POPULATION], species_pop], [globals()[TRAITS], json_species_traits]] = json_species
            fat_food = None
        elif len(json_species) == SPECIES_FAT_LENGTH:
            [[globals()[FOOD], species_food], [globals()[BODY], species_body],
             [globals()[POPULATION], species_pop], [globals()[TRAITS], json_species_traits],
             [globals()[FATFOOD], fat_food]] = json_species
            assert(species_body >= fat_food >= MIN_FATFOOD)
        else:
            raise AssertionError

        assert(all([MAX_FOOD >= species_food >= MIN_FOOD,
                    MAX_BODY >= species_body >= MIN_BODY,
                    MAX_POP >= species_pop >= MIN_POP,
                    MAX_TRAITS >= len(json_species_traits)]))

        species_traits = [cls.json_to_trait(trait) for trait in json_species_traits]
        species_obj = Species(species_pop, species_food, species_body, species_traits, fat_food)
        return species_obj

    @classmethod
    def species_to_json(cls, species_obj):
        assert(all([MAX_FOOD >= species_obj.food >= MIN_FOOD,
                    MAX_BODY >= species_obj.body >= MIN_BODY,
                    MAX_POP >= species_obj.population >= MIN_POP,
                    MAX_TRAITS >= len(species_obj.traits)]))
        json_traits = [cls.trait_to_json(trait) for trait in species_obj.traits]

        json_species = [[FOOD, species_obj.food], [BODY, species_obj.body],
                        [POPULATION, species_obj.population], [TRAITS, json_traits]]
        if species_obj.fat_storage:
            assert(species_obj.body >= species_obj.fat_storage >= MIN_FATFOOD)
            json_species.append([FATFOOD, species_obj.fat_storage])
        return json_species

    @classmethod
    def json_to_trait(cls, json_trait):
        if isinstance(json_trait, basestring):
            trait = json_trait
            food = None
        elif isinstance(json_trait, list) and len(json_trait) == SPECIES_CARD_LENGTH:
            [food, trait] = json_trait
            assert(CARN_FOOD_MIN <= food <= CARN_FOOD_MAX if trait == CARNIVORE
                   else HERB_FOOD_MIN <= food <= HERB_FOOD_MAX)
        else:
            raise AssertionError
        assert(trait in TRAITS_LIST)
        return TraitCard(trait, food)

    @classmethod
    def trait_to_json(cls, trait_card):
        assert(trait_card.trait in TRAITS_LIST)
        if trait_card.food_points is None:
            return trait_card.trait
        assert(CARN_FOOD_MIN <= trait_card.food_points <= CARN_FOOD_MAX if trait_card.trait == CARNIVORE
               else HERB_FOOD_MIN <= trait_card.food_points <= HERB_FOOD_MAX)
        return [trait_card.food_points, trait_card.trait]
