import random
import sys
import os

player_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "..%s..%s3" % (os.sep, os.sep))
sys.path.append(player_path)

from player import Player

deck_size = 210
max_stack_cards = 6
initial_hand_size = 9
bull_range=(3, 7)

"""
Data Definitions necessary for representing the components of a 6 Nimmit! game
"""


class Card(object):
    def __init__(self, face_value, bull):
        self.face_value = face_value
        self.bull = bull


class Stack(object):
    def __init__(self, list_of_cards):
        self.list_of_cards = list_of_cards
        self.total_bull = sum([card.bull for card in self.list_of_cards])


class Dealer(object):
    def __init__(self, list_of_players, starting_player=0):
        self.list_of_players = list_of_players
        self.deck = []
        self.discards = {}
        self.list_of_stacks = []
        self.bull_range = bull_range
        self.starting_player = starting_player

    def make_deck(self):
        """
        Makes a new deck of length deck_size, each card with a unique face value
        """
        deck = []
        for x in range(1, deck_size + 1):
            bull = random.choice(self.bull_range)
            card = Card(face_value=x, bull=bull)
            deck.append(card)
        self.deck = deck

    def deal(self):
        """
        Transfers set number of cards to each player's hand from the deck
        """
        for player in self.list_of_players:
            player.hand = []
        for x in range(self.starting_player, self.starting_player + len(self.list_of_players)):
            player_index = x % len(self.list_of_players)
            cards_dealt = self.deck[0:initial_hand_size]
            self.list_of_players[player_index].hand += cards_dealt
            self.deck = self.deck[initial_hand_size:len(self.deck)]

    def create_stack(self, card):
        """
        Creates a new stack with the given card
        """
        stack = Stack([card])
        return stack

    def create_initial_stacks(self):
        """
        Creates four initial stacks with one card each from the deck at the start of a round
        """
        stack_cards = self.deck[0:4]
        for stack_card in stack_cards:
            self.list_of_stacks.append(self.create_stack(stack_card))
        self.deck = self.deck[4:len(self.deck)]

    def collect_discards(self):
        """
        Takes each players discard and adds it to a dictionary as a value corresponding to the
        players name
        """
        for player in self.list_of_players:
            discard = player.pick_discard()
            self.discards[player.name] = discard

    def add_to_stack(self, card, stack):
        """
        Adds the given card to the appropriate stack
        """
        stack.list_of_cards.append(card)
        stack.total_bull += card.bull
        return stack

    def subtract_bull(self, player, stack):
        """
        Subtracts the bull points of a replaced stack from the player's bull points
        """
        player.bull_points -= stack.total_bull
        return player

    def add_to_hand(self, player, stack):
        """
        Adds the cards from a replaced stack to the given players hand
        """
        for card in stack.list_of_cards:
            player.hand.append(card)
        return player

    def fix_stacks(self):
        """
        Checks each player's discard against each stack and performs the necessary modifications to stack and player
        """
        while self.discards:
            min_card = min(self.discards.values(), key=lambda x: x.face_value)
            player_index = self.discards.keys()[self.discards.values().index(min_card)]
            player = self.list_of_players[player_index]
            closest_stack = None
            lowest_diff = None
            for stack in self.list_of_stacks:
                stack_top_val = stack.list_of_cards[-1].face_value
                if not closest_stack:
                    closest_stack = stack
                    lowest_diff = abs(min_card.face_value - stack_top_val)
                else:
                    current_diff = abs(min_card.face_value - stack_top_val)
                    if current_diff < lowest_diff:
                        lowest_diff = current_diff
                        closest_stack = stack
            if all([min_card.face_value < stack.list_of_cards[-1].face_value for stack in self.list_of_stacks]):
                selected_stack_index = player.pick_stack(self)
                selected_stack = self.list_of_stacks[selected_stack_index]
                self.subtract_bull(player, selected_stack)
                self.add_to_hand(player, selected_stack)
                self.list_of_stacks.remove(selected_stack)
                self.list_of_stacks.append(self.create_stack(min_card))
            elif len(closest_stack.list_of_cards) == max_stack_cards:
                self.subtract_bull(player, closest_stack)
                self.list_of_stacks.remove(closest_stack)
                self.list_of_stacks.append(self.create_stack(min_card))
            else:
                self.list_of_stacks.remove(closest_stack)
                replace_stack = self.add_to_stack(min_card, closest_stack)
                self.list_of_stacks.append(replace_stack)

            self.list_of_players[player.name] = player
            self.discards.pop(player.name)

    def find_winner(self):
        """
        Returns a list of (player name, player bull points), sorted in increasing bull point order if there is a player
        whose bull points value is less than -66
        """
        any_winner = False
        for player in self.list_of_players:
            if player.bull_points < -66:
                any_winner = True
        if any_winner:
            result = sorted(self.list_of_players, key=lambda (p): p.bull_points, reverse=True)
            return [(player.name, player.bull_points) for player in result]
        else:
            return None

    def play_game(self):
        """
        The dealer initiates a 6Nimmt! game, returning a list of players sorted in increasing bull
        point order
        """
        while True:
            result = self.find_winner()
            if result:
                return result
            self.deal()
            self.list_of_stacks = []
            self.create_initial_stacks()
            self.collect_discards()
            self.fix_stacks()
            self.make_deck()
            random.shuffle(self.deck)



def main(n, starting_player=0):
    """
    Creates n players and a dealer, and has the dealer run a 6 Nimmit! game
    :param n: the number of players in the game
    :param starting_player; the index of the starting player
    :return:
    """
    n = int(n)
    starting_player = int(starting_player)
    if n > deck_size / initial_hand_size:
        raise RuntimeError("Not enough cards in deck for %d players! Select less than %d players."
                           % (n, deck_size / initial_hand_size))
    if starting_player >= n:
        raise RuntimeError("There is no player %d" % starting_player)
    players = []
    for x in range(0, n):
        player = Player(name=x)
        players.append(player)
    dealer = Dealer(list_of_players=players, starting_player=starting_player)
    dealer.make_deck()
    result = dealer.play_game()
    print result

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 3:
        raise RuntimeError("Too many args given, main only accepts number of players (n), bull point value")
    elif len(args) < 3:
        raise RuntimeError("Must supply number of players between 1 and %d, bull point range and the "
                           "starting player to main" % ((deck_size - 4) / initial_hand_size))
    elif len(args) == 3:
        main(args[1], args[2])
