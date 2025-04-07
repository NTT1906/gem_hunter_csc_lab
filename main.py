from sols.backtrack_sol import BacktrackSolution
from sols.bruteforce_sol import BruteforceSolution
from sols.pysat_sol import *
from utils import *

def run(file_name):
	grid = read_input(file_name)

	for i in grid:
		print(i)

	cnf = generate_cnf(grid)

	print(cnf.clauses)
	print(f"Clauses: {len(cnf.clauses)}")

	scoped_cells = []

	for row in range(len(grid)):
		for col in range(len(grid[0])):
			if grid[row][col] != 0:
				for r, c in get_neighbors(grid, row, col):
					if grid[r][c] == 0 and (r, c) not in scoped_cells:
						scoped_cells.append((r, c))

	def test(sol: ISolution, name: str):
		print(f"Solution: {name}")
		elapsed_time = -time.time()
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
						if (row, col) not in scoped_cells:
							print('_', end=' ')
							continue
						m = row * cols + col + 1
						if m in model:
							print("T", end=' ')
						else:
							print("G", end=' ')
					else:
						print(f"{grid[row][col]}", end=' ')
				print('')
		elapsed_time += time.time()
		print(f"Real time: {elapsed_time * 1000:.3f}ms")

	solutions = {
		"pysat": PysatSolution(),
		"backtrack": BacktrackSolution(),
		"bruteforce": BruteforceSolution()
	}

	for name, sol in solutions.items():
		test(sol, name)

def main():
	input_files = [
		# "asset/input_5.txt",
		# "asset/input_4.txt",
		# "asset/input_2.txt",
		# "asset/input_3.txt",
		# "asset/input_1.txt",
		"asset/input_6.txt",
	]
	for file in input_files:
		run(file)

if __name__ == "__main__":
	main()