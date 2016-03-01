The purpose of this project is to develop a player and the method next_feeding along with the
necessary testing files and to think about the players usage in the rest of Evolution.

feeding/player.py: the Player object with the next_feeding method and necessary helpers
feeding/player_state.py: the data representation of the player
feeding/player_tests.py: unit tests for a player object
feeding/species.py: the Species object
feeding/species_tests.py: unit tests for a species object
feeding/traitcard.py: the TraitCard object

test/*: json input and output files for testing xfeed

compile: a script to compile python files, exits with 0
convert.py: methods to convert between json and python objects
convert_tests.py: unit tests for convert.py methods
feed.pdf: a memo detailing how the dealer calls next_feeding
globals.py: global variables for Evolution
xattack.py: updated attack tests for is_attackable method for regression testing
xfeed: executable for testing next_feeding method

__________________________________________________________________________________________

to run compile:

./compile

to run xfeed:

./xfeed < input.json > output.json

__________________________________________________________________________________________

Read the following files (from top to bottom) in order below:
- traitcard.py
- species.py
- species_tests.py
- player_state.py
- player.py
- player_tests.py
- xfeed
- convert.py
- convert_tests.py
- test/*
- feed.pdf

