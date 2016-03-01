from feeding import player_state
from feeding import species
from feeding import traitcard


class Convert(object):
    """
    Methods for converting between JSON input and Python objects
    """
    def __init__(self):
        pass

    @classmethod
    def json_to_feeding(cls, json_feeding):
        assert(len(json_feeding) == 3)
        player = cls.json_to_player(json_feeding[0])
        wh_food = json_feeding[1]
        assert(wh_food >= 1)
        other_players = []
        for op in json_feeding[2]:
            other_players.append(cls.json_to_player(op))
        return [player, wh_food, other_players]

    @classmethod
    def feeding_to_json(cls, feeding):
        if not feeding:
            return False
        elif isinstance(feeding, species.Species):
            return cls.species_to_json(feeding)
        elif len(feeding) == 2:
            return [cls.species_to_json(feeding[0]), feeding[1]]
        elif len(feeding) == 3:
            return [cls.species_to_json(feeding[0]),
                    cls.player_to_json(feeding[1]),
                    cls.species_to_json(feeding[2])]

    @classmethod
    def json_to_player(cls, json_player):
        assert(len(json_player) == 3)
        player_id = json_player[0][1]
        food_bag = json_player[2][1]
        assert(player_id >= 1 and food_bag >= 0)
        player_species = []
        for json_species in json_player[1][1]:
            player_species.append(cls.json_to_species(json_species))
        player_obj = player_state.PlayerState(name=player_id, food_bag=food_bag, species=player_species)
        return player_obj

    @classmethod
    def player_to_json(cls, player):
        assert(player.name >= 1 and player.food_bag >= 0)
        json_species = []
        for species_obj in player.species:
            json_species.append(cls.species_to_json(species_obj))
        return [["id", player.name], ["species", json_species], ["bag", player.food_bag]]


    @classmethod
    def json_to_species(cls, json_species):
        assert(len(json_species) == 4 or len(json_species) == 5)
        species_food = json_species[0][1]
        species_body = json_species[1][1]
        species_pop = json_species[2][1]
        assert(all([species_food >= 0, species_body >= 0, species_pop >= 1]))
        species_traits = []
        for trait in json_species[3][1]:
            species_traits.append(cls.json_to_trait(trait))
        species_obj = species.Species(species_pop, species_food, species_body, species_traits)
        if len(json_species) == 5:
            fat_food = json_species[4][1]
            assert(fat_food >= 0)
            species_obj.fat_storage = fat_food
        return species_obj

    @classmethod
    def species_to_json(cls, species_obj):
        assert(all([species_obj.population >= 1, species_obj.food >= 0, species_obj.body >= 0]))
        json_traits = []
        for trait in species_obj.traits:
            json_traits.append(cls.trait_to_json(trait))
        json_species = [["food", species_obj.food], ["body", species_obj.body],
                        ["population", species_obj.population], ["traits", json_traits]]
        if species_obj.fat_storage is not None:
            assert(species_obj.fat_storage >= 0)
            json_species.append(["fat-food", species_obj.fat_storage])
        return json_species

    @classmethod
    def json_to_trait(cls, json_trait):
        return traitcard.TraitCard(json_trait)

    @classmethod
    def trait_to_json(cls, trait_card):
        return trait_card.trait