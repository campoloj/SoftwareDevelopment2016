#! /usr/bin/env python

"""
A test harness for the Dealer feed1 method
"""

import json
import sys

from convert import Convert


def main():
    message = sys.stdin.readlines()
    json_config = ""
    for line in message:
        json_config += line.rstrip('\n')
    json_config = json.loads(json_config)
    try:
        dealer = Convert.json_to_dealer(json_config)
        dealer.validate()
        dealer.feed1(dealer.list_of_players[0])
        dealer = Convert.dealer_to_json(dealer)
        sys.stdout.write(json.dumps(dealer))
    except AssertionError:
        sys.exit(0)


if __name__ == "__main__":
    main()