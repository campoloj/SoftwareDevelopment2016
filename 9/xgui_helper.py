#! /usr/bin/env python

"""
A helper executable for xgui; creates one GUI display window
"""

import sys
from gui import gui


if __name__ == "__main__":
    gui.display(sys.argv[1])