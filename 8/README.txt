The purpose of this project was to complete the feeding phase of Evolution by implementing
the dealer and a feed1 method which updates the game state after one player chooses a feeding.

_____________________________________________________________________________________________

dealer/dealer.py: the Dealer object with the feed1 method and necessary helpers
dealer_tests.py: unit tests for a Dealer object
dealer/globals.py: global variables for Evolution rules and objects
dealer/player.py: the Player object with the next_feeding method and necessary helpers
dealer/player_state.py: the PlayerState object
dealer/player_tests.py: unit tests for a Player object
dealer/species.py: the Species object
dealer/species_tests.py: unit tests for a Species object
dealer/traitcard.py: the TraitCard object

xattack_tests/*: json input and output files to check bug fixes in xattack
xfeed_tests/*: json input and output files for xfeed
xstep_tests/*: json input and output files for xstep

compile: executable to "compile" xstep (just exits with status 0 because Python)
convert.py: methods to convert between json and python objects
convert_tests.py: unit tests for convert.py methods
xattack: executable for testing is_attackable method and regression testing
xfeed: executable for testing next_feeding method and regression testing
xstep: executable for testing feed1 method
rest.txt: wishlist for the rest of the player to complete the game.

__________________________________________________________________________________________

to run compile:

./compile

to run xattack:

./xattack < input.json > output.json

to run xfeed:

./xfeed < input.json > output.json

to run xstep:

./xstep < input.json > output.json

__________________________________________________________________________________________

Read the following files (from top to bottom) in order below:

In 8/dealer:
- traitcard.py
- species.py
- species_tests.py
- player_state.py
- player.py
- player_tests.py
- dealer.py
- dealer_tests.py

In 8:
- xattack
- xattack_tests/*

- xfeed
- xfeed_tests/*

- xstep
- xstep_tests/*

- convert.py
- convert_tests.py



