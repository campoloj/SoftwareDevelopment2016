from convert import *


class Player_Proxy(object):

    def __init__(self, id, handler):
        self.id = id
        self.handler = handler

    def start(self, player_state):
        json_dealer = Convert.player_to_json()
        self.handler.request.sendall(json_dealer)
        response = ""
        while response == "":


    def test(self):
        print self.id
