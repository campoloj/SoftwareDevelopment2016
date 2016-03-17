#! /usr/bin/env python

"""
A test harness for the Dealer display method
"""

import sys
from gui import gui


if __name__ == "__main__":
    gui.display(sys.argv[1].replace("\\n", "\n"))