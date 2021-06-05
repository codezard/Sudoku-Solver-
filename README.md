<h1 align='center'>Sudoku Solver</h1>

This is a Sudoku solving project that uses backtracking algorithm to find the missing values in the box.
It has a standard size of nine 3x3 blocks containing 81 cells in total. The algorithhm uses recursion of solving problems by trying to build a solution incrementally. We move through the empty boxes cell by cell, and add a digit. If the current digit cannot lead to a solution, we remove it (backtrack) and try next digit. If all the (0-9) possibilities cannot be placed in that cell, we move back to the last box where the digit was placed and increment its value. 
This is better than naive approach since you are not generating all the possible combinations as it drops a set of permutations whenever it backtracks.
