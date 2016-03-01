"""
A test harness for the Species is_attackable method
"""

import sys
import json
from attack import species


def main():
    message = sys.stdin.readlines()
    json_situation = ""
    for line in message:
        json_situation += line.rstrip('\n')
    situation = json.loads(json_situation)
    situation = map(convert_species, situation)
    attackable = situation[0].is_attackable(situation[1], situation[2], situation[3])
    print json.dumps(attackable)


def convert_species(json_species):
    """
    Converts a JSON representation of a species to a Species object
    :param json_species: JSON representation of a species
    :return: A Species object, or False
    """
    if not json_species:
        return False
    species_obj = species.Species()
    species_obj.food = json_species[0][1]
    species_obj.body = json_species[1][1]
    species_obj.population = json_species[2][1]
    species_obj.traits = json_species[3][1]
    return species_obj

if __name__ == "__main__":
    main()