import os
from sols.backtrack_sol import BacktrackSolver
from sols.bruteforce_sol import BruteforceSolver
from sols.pysat_sol import *
from utils import *

run_path = os.path.dirname(os.path.abspath(__file__))
def get_file_absolute_path(file_path):
	return os.path.abspath(str(os.path.join(run_path, file_path)))

def run(file_name):
	grid = read_input(file_name)
	rows = len(grid)
	cols = len(grid[0])

	for i in grid:
		print(i)

	cnf = generate_cnf(grid)
	print(cnf.clauses)
	clause_size = len(cnf.clauses)
	empty_cells = sum(grid[row][col] == 0 for row in range(rows)for col in range(cols))
	print(f"[!] Clauses: {clause_size}")
	print(f"[!] Empty cells: {empty_cells}")

	scoped_cells = []

	for row in range(rows):
		for col in range(cols):
			if grid[row][col] != 0:
				for r, c in get_neighbors(grid, row, col):
					if grid[r][c] == 0 and (r, c) not in scoped_cells:
						scoped_cells.append((r, c))

	def test(solution: ISolver, solution_name: str):
		print(f"[+] Solver: {solution_name}")
		if isinstance(solution, BruteforceSolver) and rows > 5:
			print("TOO LONG")
			return
		elapsed_time = -time.time()
		result = solution.solve(grid, cnf)
		if result is None:
			print("No solution")
		else:
			model = result.model
			output_grid = [row_sec[:] for row_sec in grid]
			for trow in range(rows):
				for tcol in range(cols):
					if grid[trow][tcol] == 0 and (trow, tcol) in scoped_cells:
						var_index = trow * cols + tcol + 1
						if var_index in model:
							output_grid[trow][tcol] = 'T'
						else:
							output_grid[trow][tcol] = 'G'
					elif grid[trow][tcol] == 0 and (trow, tcol) not in scoped_cells:
						output_grid[trow][tcol] = '_'

			for trow in output_grid:
				print(' '.join(map(str, trow)))
			print(f"Algorithm elapsed time: {result.elapsed_time:.4f}ms")
			if solution_name == "Pysat":
				output_file = get_output_name_from_input_file(file_name)
				with open(output_file, 'w') as file:
					print(f"Solution being saved to {output_file}")
					for trow in output_grid:
						file.write(', '.join(map(str, trow)) + '\n')
		elapsed_time += time.time()
		print(f"Total running time: {elapsed_time * 1000:.4f}ms")

	solutions = {
		"Pysat": PysatSolver(),
		"Backtrack": BacktrackSolver(),
		"Bruteforce": BruteforceSolver()
	}

	for name, sol in solutions.items():
		test(sol, name)

def main():
	input_files = [
		"../asset/input_4.txt",
		"../asset/input_3.txt",
		"../asset/input_2.txt",
		"../asset/input_1.txt",
	]
	for file in input_files:
		run(file)

if __name__ == "__main__":
	main()
