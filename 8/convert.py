from feeding.player_state import PlayerState
from feeding.species import Species
from feeding.traitcard import TraitCard
from feeding.globals import *




class Convert(object):
    """
    Methods for converting between JSON input and Python objects
    """
    def __init__(self):
        pass

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
        assert(len(json_player) == PLAYER_LENGTH)
        [[globals()[ID], player_id], [globals()[SPECIES], json_los], [globals()[BAG], food_bag]] = json_player
        assert(all([player_id >= MIN_PLAYER_ID, food_bag >= MIN_FOOD_BAG,
               isinstance(player_id, int), isinstance(food_bag,int)]))
        player_species = [cls.json_to_species(json_species) for json_species in json_los]
        player_obj = PlayerState(name=player_id, food_bag=food_bag, species=player_species)
        return player_obj

    @classmethod
    def player_to_json(cls, player):
        assert(player.name >= MIN_PLAYER_ID and player.food_bag >= MIN_FOOD_BAG)
        json_species = [cls.species_to_json(species_obj) for species_obj in player.species]
        return [[ID, player.name], [SPECIES, json_species], [BAG, player.food_bag]]


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
                    MAX_POP >= species_pop >= MIN_POP]))

        species_traits = [cls.json_to_trait(trait) for trait in json_species_traits]
        species_obj = Species(species_pop, species_food, species_body, species_traits, fat_food)
        return species_obj

    @classmethod
    def species_to_json(cls, species_obj):
        assert(all([MAX_FOOD >= species_obj.food >= MIN_FOOD,
                    MAX_BODY >= species_obj.body >= MIN_BODY,
                    MAX_POP >= species_obj.population >= MIN_POP]))
        json_traits = [cls.trait_to_json(trait) for trait in species_obj.traits]

        json_species = [[FOOD, species_obj.food], [BODY, species_obj.body],
                        [POPULATION, species_obj.population], [TRAITS, json_traits]]
        if species_obj.fat_storage:
            assert(species_obj.body >= species_obj.fat_storage >= MIN_FATFOOD)
            json_species.append([FATFOOD, species_obj.fat_storage])
        return json_species

    @classmethod
    def json_to_trait(cls, json_trait):
        return TraitCard(json_trait)

    @classmethod
    def trait_to_json(cls, trait_card):
        return trait_card.trait
