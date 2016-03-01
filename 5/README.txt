The purpose of this project is to develop a data representation of an Evolution species, write a method for that
species which determines whether it is attackable, create a test harness for stdin testing of is_attackable, and
design a player interface

attack/__init__.py: Allows attack/ to be imported as a module in xattack.py
attack/species.py: A data representation of a species
attack/species_tests.py: Unit tests for the Species is_attackable() method
xattack.py: An executable script that tests is_attackable using stdin and stdout JSON messages
player-interface.txt: Describes data representations and player interface functions for Evolution

______________________________________________________________________________________________________________________

To run xattack.py, run "./xattack.py < some-json-input > some-json-output" from the command line, or for windows cd into
the 5 directory and run "xattack.py < some-json-input > some-json-output



______________________________________________________________________________________________________________________

attack/species and attack.species_tests should be read first.
xattack.py should be read next.
player-interface.txt should be read last.