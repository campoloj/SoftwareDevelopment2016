The purpose of this project was to create a gui that can represent the game state as well as a player state
that can be displayed from a dealer and player.

_____________________________________________________________________________________________

dealer/dealer.py: the Dealer object with the feed1 method and necessary helpers
dealer/dealer_tests.py: unit tests for a Dealer object
dealer/globals.py: global variables for Evolution rules and objects
dealer/gui.py: functions used for the display methods to show gui
dealer/gui_tests.py: the unit tests for a gui functions
dealer/player.py: the Player object with the next_feeding method and necessary helpers
dealer/player_state.py: the PlayerState object
dealer/player_tests.py: unit tests for a Player object
dealer/species.py: the Species object
dealer/species_tests.py: unit tests for a Species object
dealer/traitcard.py: the TraitCard object
dealer/feeding_choice.py: the FeedingChoice data representations

xgui_tests/*: json input and output files to check ./xgui functionality

convert.py: methods to convert between json and python objects
convert_tests.py: unit tests for convert.py methods
xgui: executable for displaying a game state and the first player's state
xgui_helper.py: the helper to display both windows at the the same time in xgui

__________________________________________________________________________________________

to run compile:

./compile

to run xgui:

./xgui < input.json > output.json

__________________________________________________________________________________________

Read the following files (from top to bottom) in order below:

In 10/gui:
- traitcard.py
- species.py
- species_tests.py
- player_state.py
- player.py
- player_tests.py
- dealer.py
- dealer_tests.py
- gui.py
- gui_tests.py

In 10:
- xgui
- xgui_helper.py
- xgui_tests/*

- convert.py
- convert_tests.py



