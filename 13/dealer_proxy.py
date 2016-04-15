from convert import *
from time import *


class Dealer_Proxy(object):

    def __init__(self, player, socket):
        self.player = player
        self.socket = socket

    def run(self):
        response = ""
        while not response:
            response = Convert.listen(self.socket, -1)

        player_state = Convert.json_to_player(json.loads(response))
        self.start(player_state)



    def start(self, player_state):
        """
        Sends the player_state in json to the proxy dealer
        :param player_state: Player_State for the external player
        """
        json_player = Convert.player_to_rp_json()
        self.handler.request.sendall(json.dumps(json_player))

    def choose(self, left_players, right_players):
        """
        Sends the all_players in json to the proxy dealer for the external player to make their choices.
        Recieves the JSON response and converts it to an Action4 to send to the internal Dealer.
        :param player_state: Player_State for the external player
        :return Action4 representing the players choices
        """
        json_all_players = Convert.players_to_all_json(left_players, right_players)
        self.handler.request.sendall(json.dumps(json_all_players))
        response = Convert.listen(self.handler.request)
        json_action4 = json.loads(response)
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
        json_game_state = Convert.game_state_to_json(player_state, watering_hole, all_players)
        self.handler.request.sendall(json.dumps(json_game_state))
        response = Convert.listen(self.handler.request)
        json_feeding = json.loads(response)
        return Convert.json_to_feeding(json_feeding)