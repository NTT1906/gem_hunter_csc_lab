import asyncio
import os
import time

from sols.backtrack_sol import BacktrackSolution
from sols.bruteforce_sol import BruteforceSolution
from sols.isol import ISolution, Result
from sols.pysat_sol import PysatSolution
from utils import read_input, generate_cnf, get_neighbors, get_output_name_from_input_file

async def process_input(input_file: str, timeout: float = 2):
	try:
		print(f"Starting {input_file}")
		grid = read_input(input_file)
		cnf = generate_cnf(grid)
	except Exception as e:
		print(f"Failed to process {input_file}: {e}")
		return input_file, {"Pysat": ("ERROR", 0), "Backtrack": ("ERROR", 0), "Brute-force": ("ERROR", 0)}

	print("CNF Clauses:")
	for clause in cnf.clauses[:5]:  # Print first 5 clauses for brevity
		print(clause)
	print(f"Total Clauses: {len(cnf.clauses)}")

	scoped_cells = set()
	rows = len(grid)
	cols = len(grid[0])
	for row in range(rows):
		for col in range(cols):
			if grid[row][col] != 0:
				for r, c in get_neighbors(grid, row, col):
					if 0 <= r < rows and 0 <= c < cols and 0 == grid[r][c]:
						scoped_cells.add((r, c))

	solutions: list[tuple[str: ISolution]] = [
		("Pysat", PysatSolution()),
		("Backtrack", BacktrackSolution()),
		("Brute-force", BruteforceSolution())
	]

	solution_results = {}
	for name, solution in solutions:
		print(f"\nSolution: {name} - {input_file}")
		local_start_time = time.time()
		try:
			result = await asyncio.wait_for(asyncio.to_thread(solution.solve, grid, cnf), timeout=timeout)
			real_elapsed_time = (time.time() - local_start_time) * 1000
			print("REAL Time: ", real_elapsed_time)
			solution_results[name] = result
			if result is None:
				print("NO SOLUTION")
			else:
				elapsed_time = result.elapsed_time
				model = result.model
				output_grid = [row[:] for row in grid]
				for r in range(rows):
					for c in range(cols):
						if grid[r][c] == 0 and (r, c) in scoped_cells:
							var_index = r * cols + c + 1
							if var_index in model:
								output_grid[r][c] = 'T'
							else:
								output_grid[r][c] = 'G'
						elif grid[r][c] == 0 and (r, c) not in scoped_cells:
							output_grid[r][c] = '_'

				for row in output_grid:
					print(' '.join(map(str, row)))
				print(f"Time: {elapsed_time:.3f}ms")
		except asyncio.TimeoutError:
			print("TIMEOUT")
			solution_results[name] = Result(elapsed_time=-1.0)

	output_file = get_output_name_from_input_file(input_file)
	with open(output_file, 'w') as file:
		print(f"Solution being saved to {output_file}")
		result = solution_results["Pysat"]
		model = set(result.model) if result is not None and result.elapsed_time != -1 else set()
		output_grid = [row[:] for row in grid]
		for r in range(rows):
			for c in range(cols):
				if grid[r][c] == 0 and (r, c) in scoped_cells:
					var_index = r * cols + c + 1
					if var_index in model:
						output_grid[r][c] = 'T'
					else:
						output_grid[r][c] = 'G'
				elif grid[r][c] == 0 and (r, c) not in scoped_cells:
					output_grid[r][c] = '_'

		for row in output_grid:
			file.write(', '.join(map(str, row)) + '\n')
		# file.write("Input: " + input_file + '\n')
		# file.write("")
	return solution_results

async def benchmark():
	input_files = [
		"asset/input_2.txt",
		"asset/input_5.txt",
		"asset/input_4.txt",
		"asset/input_3.txt",
		"asset/input_1.txt",
		"asset/input_6.txt"
	]
	input_timeout = [
		2,
		2,
		2,
		5,
		15,
		60,
	]
	all_results = {}
	for i in range(len(input_files)):
		input_file = input_files[i]
		all_results[input_file] = await process_input(input_file, input_timeout[i])
		print(f"\n{'='*30} Finished {input_file} {'='*30}\n")

	print("\n\nBenchmark Summary:")
	for file, sol_results in all_results.items():
		print(f"\n--- {file} ---")
		for sol_name, result in sol_results.items():
			print(f"{sol_name}: ", end='')
			if result is None:
				print("NO SOLUTION")
			else:
				if result.elapsed_time == -1.0:
					print("TIME OUT")
				else:
					print(f"SOLVED - {result.elapsed_time:.4f}ms")

if __name__ == "__main__":
	asyncio.run(benchmark())