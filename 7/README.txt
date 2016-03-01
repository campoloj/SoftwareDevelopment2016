The purpose of this project was to update the Evolution API to return indices rather than Player
and Species objects.

Streaming/compile.py: a script to compile python files, exits with 0
Streaming/xstream.py: echo program for accepting JSON messages

feeding/player.py: the Player object with the next_feeding method and necessary helpers
feeding/player_state.py: the data representation of the player
feeding/player_tests.py: unit tests for a player object
feeding/species.py: the Species object
feeding/species_tests.py: unit tests for a species object
feeding/traitcard.py: the TraitCard object

xattack_tests/*: json input and output files to check bug fixes in xattack
xfeed_tests/*: json input and output files for xfeed

convert.py: methods to convert between json and python objects
convert_tests.py: unit tests for convert.py methods
globals.py: global variables for Evolution
xattack.py: updated attack tests for is_attackable method for regression testing
xfeed: executable for testing next_feeding method

__________________________________________________________________________________________

to run Streaming/compile:

./compile

to run Streaming/xstream:

./xstream

** xstream accepts json input from stdin and on linux machines exits with ^C

to run xfeed:

./xfeed < input.json > output.json

to run xattack:

./xattack < input.json > output.json

__________________________________________________________________________________________

Read the following files (from top to bottom) in order below:
- Streaming/xstream

- traitcard.py
- species.py
- species_tests.py
- player_state.py
- player.py
- player_tests.py
- xfeed
- xfeed_tests/*

- xattack
- xattack_tests/*

- convert.py
- convert_tests.py



