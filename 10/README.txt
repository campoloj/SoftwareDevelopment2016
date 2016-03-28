The purpose of this project was to refactor our codebase to reduce method length using
abstraction and helpers, create better unit tests and purpose statements, and pass more testfest tests.

_____________________________________________________________________________________________

dealer/dealer.py: the Dealer object with the feed1 method and necessary helpers
dealer/dealer_tests.py: unit tests for a Dealer object
dealer/feeding_choice.py: the FeedingChoice data representations
dealer/globals.py: global variables for Evolution rules and objects
dealer/gui.py: functions used for the display methods to show gui
dealer/gui_tests.py: the unit tests for a gui functions
dealer/player.py: the Player object with the next_feeding method and necessary helpers
dealer/player_state.py: the PlayerState object
dealer/player_tests.py: unit tests for a Player object
dealer/species.py: the Species object
dealer/species_tests.py: unit tests for a Species object
dealer/traitcard.py: the TraitCard object

homework_8_tests/*: json input and output files to check ./xstep functionality

convert.py: methods to convert between JSON and Python objects
convert_tests.py: unit tests for convert.py methods
xstep: executable to test Dealer feed1 method

__________________________________________________________________________________________

to run compile:

./compile

to run xstep:

./xstep < input.json > output.json

__________________________________________________________________________________________

Read the following files (from top to bottom) in order below:

In 10/gui:
- dealer.py
- dealer_tests.py
- player.py
- player_tests.py
- feeding_choice.py
- player_state.py
- species.py
- species_tests.py
- traitcard.py
- gui.py
- gui_tests.py

In 10:
- xstep
- convert.py
- convert_tests.py



