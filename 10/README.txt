The purpose of this project was to create a gui that can represent the game state as well as a player state
that can be displayed from a dealer and player.

_____________________________________________________________________________________________

gui/dealer.py: the Dealer object with the feed1 method and necessary helpers
gui/dealer_tests.py: unit tests for a Dealer object
gui/globals.py: global variables for Evolution rules and objects
gui/gui.py: functions used for the display methods to show gui
gui/gui_tests.py: the unit tests for a gui functions
gui/player.py: the Player object with the next_feeding method and necessary helpers
gui/player_state.py: the PlayerState object
gui/player_tests.py: unit tests for a Player object
gui/species.py: the Species object
gui/species_tests.py: unit tests for a Species object
gui/traitcard.py: the TraitCard object

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



