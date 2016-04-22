The purpose of this project was to incorporate minor changes in the remote protocol
to our system, as well as prepare our code base for the final code walk
_____________________________________________________________________________________________

server: The server file that starts the sign up and runs a game.
remote_main: The client executable that creates a dealer_proxy and connects with the server.
player_proxy.py: The proxy that communicates with the dealers and the dealer_proxies.
dealer_proxy.py: The proxy that communicates with the player and the player_proxy.
main: To run a full game with an input of the number of players from 3 to 8.

dealer/action.py: the Action data representations for different Player actions
dealer/action4.py: the Action4 data representation for a Player's list of actions
dealer/action_tests.py: unit tests for Action / Action4 objects
dealer/cheater: a Player Object that breaks the rules of the game. For testing.
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

convert.py: methods to convert between JSON and Python objects
convert_tests.py: unit tests for convert.py methods
xsilly: exectutable to test Player choose() method

__________________________________________________________________________________________

to run server:
./server <hostname> <port>
ex: ./server localhost 9999

to run remote_main:
./remote_main <username> <hostname> <port>
ex: ./remote_main jake localhost 9999

to run main:
n = number of players
./main n

to run xsilly:

./xsilly < input.json > output.json


__________________________________________________________________________________________

Read the following files (from top to bottom) in order below:

In 14/dealer:
- dealer.py
- dealer_tests.py
- player.py
- player_tests.py
- action4.py
- action.py
- action_tests.py
- feeding_choice.py
- player_state.py
- player_state_tests.py
- species.py
- species_tests.py
- traitcard.py
- gui.py
- gui_tests.py

In 14:
- main
- server
- player_proxy.py
- dealer_proxy.py
- remote_main
- convert




