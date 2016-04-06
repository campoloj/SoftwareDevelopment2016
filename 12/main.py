import sys
from dealer.player import Player
from dealer.dealer import Dealer


def main(n):
    """
    Creates n external players, hands there references to an instance of the Dealer component, and
    asks the Dealer to run one complete game.
    :param n: Natural between 3 and 8 representing the number of Players in the Evolution game
    :effect: Displays the results of the game on stdout
    """
    try:
        loxp = [Player() for x in xrange(n)]
        dealer = Dealer.create_initial(loxp)
        results = dealer.run_game()
        print results
    except:
        sys.exit(0)

if __name__ == "__main__":
    main(int(sys.argv[1]))