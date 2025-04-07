import os
from sols.backtrack_sol import BacktrackSolution
from sols.bruteforce_sol import BruteforceSolution
from sols.pysat_sol import *
from utils import *

run_path = os.path.dirname(os.path.abspath(__file__))
def get_file_absolute_path(file_path):
	return os.path.abspath(str(os.path.join(run_path, file_path)))

def run(file_name):
	grid = read_input(file_name)

	for i in grid:
		print(i)

	cnf = generate_cnf(grid)

	print(cnf.clauses)
	print(f"[!] Clauses: {len(cnf.clauses)}")

	scoped_cells = []

	for row in range(len(grid)):
		for col in range(len(grid[0])):
			if grid[row][col] != 0:
				for r, c in get_neighbors(grid, row, col):
					if grid[r][c] == 0 and (r, c) not in scoped_cells:
						scoped_cells.append((r, c))

	def test(solution: ISolution, solution_name: str):
		print(f"[+] Solution: {solution_name}")
		elapsed_time = -time.time()
		result = solution.solve(grid, cnf)
		if result is None:
			print("No solution")
		else:
			model = result.model
			rows = len(grid)
			cols = len(grid[0])
			output_grid = [row[:] for row in grid]
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
			print(f"Elapsed time: {result.elapsed_time:.4f}ms")
			if solution_name == "Pysat":
				output_file = get_output_name_from_input_file(file_name)
				with open(output_file, 'w') as file:
					print(f"Solution being saved to {output_file}")
					for trow in output_grid:
						file.write(', '.join(map(str, trow)) + '\n')
		elapsed_time += time.time()
		print(f"Run time: {elapsed_time * 1000:.4f}ms")

	solutions = {
		"Pysat": PysatSolution(),
		"Backtrack": BacktrackSolution(),
		"Bruteforce": BruteforceSolution()
	}

	for name, sol in solutions.items():
		test(sol, name)

def main():
	input_files = [
		# "../asset/input_5.txt",
		# "./asset/input_4.txt",
		# "../asset/input_2.txt",
		# "../asset/input_1.txt",
		"../asset2/input_4.txt",
	]
	for file in input_files:
		run(file)

if __name__ == "__main__":
	main()
