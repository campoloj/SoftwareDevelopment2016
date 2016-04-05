The purpose of this project was to deal with the entire Step 4 in the Evolution procedure,
which meant applying Player action choices and running a full feeding cycle. Additionally,
to plan the protocol between main, Dealer, and internal / external Players.

_____________________________________________________________________________________________

api/api.txt: - Descriptions for each protocol
api/End.png - Image depicting the end game protocol interaction diagram
api/Start.png - Image depicting the start game protocol interaction diagram
api/Turn.png - Image depicting the per turn protocol interaction diagram

dealer/action.py: the Action data representations for different Player actions
dealer/action4.py: the Action4 data representation for a Player's list of actions
dealer/action_tests.py: unit tests for Action / Action4 objects
dealer/dealer.py: the Dealer object with the feed1 method and necessary helpers
dealer/dealer_tests.py: unit tests for a Dealer object
dealer/feeding_choice.py: the FeedingChoice data representations
dealer/globals.py: global variables for Evolution rules and objects
dealer/gui.py: functions used for the display methods to show gui
dealer/gui_tests.py: the unit tests for a gui functions
dealer/player.py: the Player object with the next_feeding method and necessary helpers
dealer/player_state.py: the PlayerState object
dealer/player_state_tests.py: unit tests for a PlayerState object
dealer/player_tests.py: unit tests for a Player object
dealer/species.py: the Species object
dealer/species_tests.py: unit tests for a Species object
dealer/traitcard.py: the TraitCard object

homework_10_tests/*: json input and output files to check ./xstep functionality
xstep4_tests/*: json input and output files to check ./xstep4 functionality

compile.py: executable to compile xstep4 (exits with status 0)
convert.py: methods to convert between JSON and Python objects
convert_tests.py: unit tests for convert.py methods
xstep: executable to test Dealer feed1 method
xstep4: executable to test Dealer step4() method

__________________________________________________________________________________________

to run compile:

./compile

to run xstep:

./xstep < input.json > output.json

to run xstep4:

./xstep4 < input.json > output.json


__________________________________________________________________________________________

Read the following files (from top to bottom) in order below:

In 11/dealer:
- dealer.py
- dealer_tests.py
- player.py
- player_tests.py
- action4.py
- action.py
- action_tests.py
- feeding_choice.py
- player_state.py
- palyer_state_tests.py
- species.py
- species_tests.py
- traitcard.py
- gui.py
- gui_tests.py

In 11:
- xstep4
- convert.py
- convert_tests.py



