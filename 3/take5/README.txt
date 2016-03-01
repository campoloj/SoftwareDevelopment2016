File Purposes:
3/player.py - implements the previously designed player interface
fix-bugs-diff - fixed bugs in assignment_2.py main, deal, play_game and fix_stacks functions
player-git-diff - implemented player and linked to assignment 2
task_1.1-git-diff - increased max stack size to 6
task_1.2-git-diff - increased deck size to 210
task_1.3-git-diff - changed initial hand size to 9
task_1.4-git-diff - changed minimum bull point to 3
task_1.5-git-diff - player discards lowest face value from hand instead of highest

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To use this program, pull the git repository
and enter the following command from the directory the git repo is located in:
python cs4500-lidauch-jcamp/2/take5/Assignment_2.py <number of players> <starting player>
where <number of players> and <starting player> are integers
and <starting player> is between 0-<number of players>

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The player.py file should be read first followed by the player-git-diff. This git-diff shows multiple lines of
changes because we needed to implement a complete player and link the new player component from /3 into /2. This
linking took more than one line because we needed to import it and create the correct path using sys.

Next the fix-bugs-diff should be read. This shows more than one line of changes because we failed to implement a
number of rules correctly. These included: resetting the players hand each round, selecting the stack with the
lowest top card, placing the card on the stack with the closest top card, resetting the stacks each round, and parsing
args in main.

Next the task_1.1-git-diff should be read. This diff shows 2 lines of changes because we hard coded the max stack
size into the fix_stacks function and therefore needed to create a global variable before increasing the stack size.

Next the task_1.2-git-diff should be read. This diff shows a 1 line change.

Next the task_1.3-git-diff should be read. This diff shows many line changes because we hard coded hand_size into deal
and main and needed to create .

Next the task_1.4-git-diff should be read. This diff shows many line changes because we had bull_range as a
parameter to main which was a flaw in logic and needed to be created as a global variable.

Next the task_1.5-git-diff should be read. We needed to change multiple lines to reflect variable names better and
changed the comparison card to be the first card in the player hand instead of None.