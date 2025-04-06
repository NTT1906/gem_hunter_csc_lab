import sys
from sols.backtrack_sol import BacktrackSolution
from sols.pysat_sol import *
from sols.bruteforce_sol import BruteforceSolution
from utils import *

grid = read_input("asset/input_2.txt")

for i in grid:
	print(i)

cnf = generate_cnf(grid)

from pprint import pprint
pprint(cnf.clauses)
print(f"Clauses: {len(cnf.clauses)}")
pysat_sol = PysatSolution()
bruteforce_sol = BruteforceSolution()
backtrack_sol = BacktrackSolution()

def test(sol: ISolution, name: str):
	print(f"Test: {name}")
	duration = -time.time()
	result = sol.solve(grid, cnf)
	if result is None:
		print("No solution")
	else:
		model = result.model
		rows = len(grid)
		cols = len(grid[0])
		for row in range(rows):
			for col in range(cols):
				if grid[row][col] == 0:
					m = row * cols + col + 1
					if m in model:
						print("T", end=' ')
					else:
						print("G", end=' ')
				else:
					print(f"{grid[row][col]}", end=' ')
			print('')
	duration += time.time()
	print(f"D: {duration * 1000:.3f}ms")

test(pysat_sol, "pysat")
test(backtrack_sol, "backtrack")
test(bruteforce_sol, "bruteforce")
