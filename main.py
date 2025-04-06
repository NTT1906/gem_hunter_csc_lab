from sols.backtrack_sol import BacktrackSolution
from sols.pysat_sol import *
from sols.bruteforce_sol import BruteforceSolution
from utils import *

grid = read_input("asset/input1.txt")

# # Example grid
# grid = [[2, 0],
# 		[0, 0]]

# grid = [[0, 0, 0, 5, 0, 0],
# 		[4, 0, 0, 0, 0, 0],
# 		[0, 0, 6, 0, 0, 0],
# 		[2, 2, 0, 0, 0, 2],
# 		[0, 3, 4, 5, 4, 2],
# 		[2, 0, 0, 0, 0, 0]]

for i in grid:
	print(i)

# Generate CNF constraints
cnf_clauses = generate_cnf(grid)
# print("Generated CNF Clauses:")
# for clause in sorted(cnf_clauses.clauses):
# 	print(f"{clause}")
# print("Pretty Printed CNF Clauses:")
# pretty_print_cnf(cnf_clauses, len(grid))

# KB = {
# 	1: False,  # Cell (0, 0) is a gem
# 	4: True,   # Cell (1, 0) is a trap
# 	6: False,  # Cell (1, 1) is a gem
# 	9: True,   # Cell (2, 1) is a trap
# }

# optimize CNF using the knowledge base
# optimized_cnf = optimize_cnf(cnf_clauses, KB)
# print("Optimized CNF Clauses:")
# for clause in sorted(optimized_cnf.clauses):
# 	print(f"{clause}")
	# print(f"{sorted(clause)}")

# print("Pretty Printed optimized CNF Clauses:")
# pretty_print_cnf(optimized_cnf, len(grid[0]))

print(cnf_clauses.clauses)

pysat_sol = PysatSolution()
bf_sol = BruteforceSolution()
bt_sol = BacktrackSolution()

duration = -time.time()
print(pysat_sol.solve(grid, cnf_clauses).model)
duration += time.time()
print(f"D: {duration * 1000:.3f}ms")

duration = -time.time()
print(bf_sol.solve(grid, cnf_clauses).model)
duration += time.time()
print(f"D: {duration * 1000:.3f}ms")

duration = -time.time()
print(bt_sol.solve(grid, cnf_clauses).model)
duration += time.time()
print(f"D: {duration * 1000:.3f}ms")