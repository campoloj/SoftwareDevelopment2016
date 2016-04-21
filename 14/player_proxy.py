from convert import *
from time import *


class PlayerProxy(object):
    """
    Filters JSON messages from the client to the server
    Uses Dealer to generate responses and sends them back to client
    """
    def __init__(self, id, handler):
        """
        Creates a PlayerProxy
        :param id: String representing the client's chosen username
        :param handler: Request Handler used to send messages to client
        :return: PlayerProxy object
        """
        self.id = id
        self.handler = handler

    def start(self, watering_hole, player_state):
        """
        Sends the player_state in json to the proxy dealer
        :param watering_hole: Natural representing food currently at the watering hole
        :param player_state: Player_State for the external player
        """
        json_player = player_state.convert_to_state_json()
        state = [watering_hole] + json_player
        self.handler.request.sendall(json.dumps(state))

    def choose(self, left_players, right_players):
        """
        Sends the all_players in json to the proxy dealer for the external player to make their choices.
        Recieves the JSON response and converts it to an Action4 to send to the internal Dealer.
        :param player_state: Player_State for the external player
        :return Action4 representing the players choices
        """
        json_all_players = Convert.players_to_all_json(left_players, right_players)
        self.handler.request.sendall(json.dumps(json_all_players))
        json_action4 = Convert.listen(self.handler.request)
        return Convert.json_to_action4(json_action4)

    def next_feeding(self, player_state, watering_hole, all_players):
        """
        Sends the all_players in json to the proxy dealer and recieves theyre result in json.
        Converts the json result into a Feeding and returns it to the internal Dealer.
        :param player_state: Player_State for the external player
        :param watering_hole: Nat representing the food on the watering hole
        :param all_players: List of Player_State representing all the players
        :return Feeding_Choice representing the players feeding choice
        """
        json_game_state = Convert.gamestate_to_json(player_state, watering_hole, all_players)
        self.handler.request.sendall(json.dumps(json_game_state))
        json_feeding = Convert.listen(self.handler.request)
        return Convert.json_to_feeding_choice(json_feeding)
