<h1 align='center'>Sudoku Solver</h1>

![PyGame][1] ![Python][2] ![License][3]
 
This is a Sudoku solving project that uses backtracking algorithm to find the missing values in the box.
It has a standard size of nine 3x3 blocks containing 81 cells in total. The algorithhm uses recursion of solving problems by trying to build a solution incrementally. We move through the empty boxes cell by cell, and add a digit. If the current digit cannot lead to a solution, we remove it (backtrack) and try next digit. If all the (0-9) possibilities cannot be placed in that cell, we move back to the last box where the digit was placed and increment its value. 
This is better than naive approach since you are not generating all the possible combinations as it drops a set of permutations whenever it backtracks.

You can either enter your own solvable board or you can set it to random. Where you will get a random solvable board.

This project is inspired by TechwithTim.

# How To Play

If you don't have pygame[2.0.1] installed in your environment:
  Create a new environment and install the neccessary libraries from cmd
  Command: 'pip install -r requirements.txt'

Paste these files all together in desired folder and simply run the file run.py from cmd. 
Command: 'python run.py'.

## Keys
To place a number: Select a box and press the digit you please to enter and then press ENTER.

For a hint: Press H. A random box will be filed with a correct digit.

To see the visual representation of the sudoku solving: Press SPACE.

[1]: https://img.shields.io/badge/pygame-1.9.6-red
[2]: https://img.shields.io/badge/python-3.6.6-blue
[3]: https://img.shields.io/badge/license-MIT-orange
