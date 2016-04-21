from convert import *
from time import *


class DealerProxy(object):
    """
    Filters JSON messages from the server to the client
    Uses external Player to generate responses and sends them back to server
    """
    def __init__(self, player, socket):
        """
        Creates a DealerProxy
        :param player: Player object representing an external player strategy
        :param socket: Socket on which to listen to and send messages
        :return: DealerProxy object
        """
        self.player = player
        self.socket = socket

    def wait_for_start(self):
        """
        Waits for the start message with the initial player state. Calls start on our player.
        """
        response = Convert.listen(self.socket, False)
        self.start(response)

    def start(self, json_state):
        """
        Gives the external player their state, then waits for the choice json of all the players and calls choose.
        :param json_state: JSON State representing watering hole and PlayerState attributes
        """
        [watering_hole, player_state] = Convert.json_to_state(json_state)
        self.player.start(watering_hole, player_state)
        json_all_players = Convert.listen(self.socket, False)
        self.choose(json_all_players)

    def choose(self, json_all_players):
        """
        Converts the json_all_players to two lists of Player_States. Then asks the player to chose with the
        information. Converts the Action4 results to json. Sends it. Waits for the next step.
        :param json_all_players: JSON [LOB, LOB]
        """
        left_players = Convert.json_to_choice_lop(json_all_players[0])
        right_players = Convert.json_to_choice_lop(json_all_players[1])
        action4 = self.player.choose(left_players, right_players)
        json_action4 = Convert.action4_to_json(action4)
        self.socket.sendall(json.dumps(json_action4))
        self.wait_for_next_step()

    def feed(self, json_state):
        """
        Converts the given game state to a list of the information needed to feed. Calls feed on the player with the
        information. Converts the FeedingChoice result into json and sends it. Waits for the next step.
        :param json_state: JSON GameState
        """
        [updated_player, watering_hole, all_players] = Convert.json_to_gamestate(json_state)
        feeding = self.player.next_feeding(updated_player, watering_hole, all_players)
        json_feeding = feeding.convert_to_json()
        self.socket.sendall(json.dumps(json_feeding))
        self.wait_for_next_step()

    def wait_for_next_step(self):
        """
        Waits for the response and then checks where in the game we are.
        If the response is a list of length 4 -> Choose
        If the response is a list of length five -> Feed
        """
        response = Convert.listen(self.socket)
        if len(response) == 4:
            return self.start(response)
        elif len(response) == 5:
            return self.feed(response)
