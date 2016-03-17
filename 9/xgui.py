#! /usr/bin/env python

"""
A test harness for the Dealer and PlayerState display method
"""

import json
import sys
import subprocess
from gui import gui

from convert import Convert


def main():
    json_config = json.loads(sys.stdin.read())
    try:
        dealer = Convert.json_to_dealer(json_config)
        dealer.validate()
        subprocess.Popen(["xgui_helper.py", gui.render_dealer(dealer).replace("\n", "\\n")], shell=True)
        subprocess.Popen(["xgui_helper.py", gui.render_player(dealer.list_of_players[0]).replace("\n", "\\n")],
                         shell=True)
        sys.exit(0)
    except:
        sys.exit(0)


if __name__ == "__main__":
    main()