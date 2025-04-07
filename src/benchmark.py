import asyncio
import time

from src.sols.backtrack_sol import BacktrackSolver
from src.sols.bruteforce_sol import BruteforceSolver
from src.sols.isol import ISolver, Result
from src.sols.pysat_sol import PysatSolver
from src.utils import read_input, generate_cnf, get_neighbors, get_output_name_from_input_file

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

	rows = len(grid)
	cols = len(grid[0])
	clause_size = len(cnf.clauses)
	empty_cells = sum(grid[row][col] == 0 for row in range(rows) for col in range(cols))
	print(f"[!] Clauses: {clause_size}")
	print(f"[!] Empty cells: {empty_cells}")

	scoped_cells = set()
	for row in range(rows):
		for col in range(cols):
			if grid[row][col] != 0:
				for r, c in get_neighbors(grid, row, col):
					if 0 <= r < rows and 0 <= c < cols and 0 == grid[r][c]:
						scoped_cells.add((r, c))

	solutions: list[tuple[str: ISolver]] = [
		("Pysat", PysatSolver()),
		("Backtrack", BacktrackSolver()),
		("Brute-force", BruteforceSolver())
	]

	solution_results = {}
	for name, solution in solutions:
		print(f"\nSolver: {name} - {input_file}")
		try:
			elapsed_time = -time.time()
			result = await asyncio.wait_for(asyncio.to_thread(solution.solve, grid, cnf), timeout=timeout)
			if result is None:
				print("No solution")
			else:
				solution_results[name] = result
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
				if isinstance(solution, PysatSolver):
					output_file = get_output_name_from_input_file(input_file)
					with open(output_file, 'w') as file:
						print(f"Solution being saved to {output_file}")
						for trow in output_grid:
							file.write(', '.join(map(str, trow)) + '\n')
			elapsed_time += time.time()
			print(f"Total running time: {elapsed_time * 1000:.4f}ms")
		except asyncio.TimeoutError:
			print("TIMEOUT")
			solution_results[name] = Result(elapsed_time=-1.0)
	return solution_results, clause_size, empty_cells

async def benchmark():
	input_files = [
		"../asset/input_4.txt",
		"../asset/input_3.txt",
		"../asset/input_2.txt",
		"../asset/input_1.txt",
	]
	input_timeout = [
		60,
		20,
		10,
		2,
	]
	all_results = {}
	for i in range(len(input_files)):
		input_file = input_files[i]
		print(f"\n{'='*30} {input_file} {'='*30}\n")
		all_results[input_file] = await process_input(input_file, input_timeout[i])

	print(f"\n{'='*30} Benchmark Summary {'='*30}")
	for file, (sol_results, clause_size, empty_cells) in all_results.items():
		print(f"\n--- {file} ---")
		print(f"[!] Clauses: {clause_size}")
		print(f"[!] Empty cells: {empty_cells}")

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