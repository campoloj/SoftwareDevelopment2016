#! /usr/bin/env python

"""
A test harness for the Dealer display method
"""

import sys
from gui import gui


if __name__ == "__main__":
    gui.display(str(sys.argv[1]))