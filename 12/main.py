import sys
from player import Player
from dealer.dealer import Dealer


def main(n):
    """
    Creates n external players, hands there references to an instance of the Dealer component, and
    asks the Dealer to run one complete game.
    :param n: Natural between 3 and 8 representing the number of Players in the Evolution game
    :effect: Displays the results of the game on stdout
    """
    loxp = [Player() for x in xrange(n)]
    dealer = Dealer.create_initial(loxp)
    results = dealer.run_game()
    print results

if __name__ == "__main__":
    main(sys.argv[1])