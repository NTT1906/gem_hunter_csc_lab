from itertools import combinations
from pysat.formula import CNF
from pathlib import Path

def read_input(file_path):
	"""
	Reads the grid from input file.
	Numbers represent the amount of traps around that cell.
	'_' represents an unknown cell.
	:param file_path: input file path (unix)
	"""
	_grid = []
	with open(file_path, 'r') as f:
		for line in f:
			cells = [cell.strip() for cell in line.strip().split(', ')]
			processed = [int(cell) if cell.isdigit() and 0 < int(cell) < 9 else 0 for cell in cells]
			_grid.append(processed)
	return _grid

def get_output_name_from_input_file(input_path):
	input_path = Path(input_path)
	return input_path.with_name('output_' + input_path.stem[6:] + input_path.suffix)

def get_neighbors(grid, i, j):
	"""
	Get all neighbors of cell at (i, j). Excluding cell outside of grid and number cells.
	"""
	rows, cols = len(grid), len(grid[0])
	neighbors = []
	for r, c in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1), (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)]:
		if 0 <= r < rows and 0 <= c < cols and 0 == grid[r][c]: # check if neighbor is inside the grid and not a number cell
			neighbors.append((r, c))
	return neighbors

def generate_cnf(grid) -> CNF:
	"""
	Convert grid to CNF, removing duplicate clauses regardless of order.
	"""
	clauses_set = set()
	rows, cols = len(grid), len(grid[0])

	for i in range(rows):
		for j in range(cols):
			if grid[i][j] != 0:
				clauses_set.add(tuple([-(i * cols + j + 1)]))
				trap_amount = grid[i][j]
				neighbors = get_neighbors(grid, i, j)
				neighbors_count = len(neighbors)
				if neighbors_count == 0:
					continue

				# at least trap_amount of traps -> at most 'neighbors_count - trap_amount' non-trap
				# -> at least 'neighbors_count - trap_amount + 1' non-traps
				for comb in combinations(neighbors, neighbors_count - trap_amount + 1):
					clause = tuple(sorted((r * cols + c + 1) for r, c in comb))
					clauses_set.add(clause)

				# at most 'trap_amount' traps -> not (at least 'trap_amount + 1' traps)
				# for each combination of (trap_amount + 1) neighbors, at least one must NOT be a trap
				if trap_amount < neighbors_count:
					for comb in combinations(neighbors, trap_amount + 1):
						clause = tuple(sorted(-(r * cols + c + 1) for r, c in comb))
						clauses_set.add(clause)

	return CNF(from_clauses=list(clauses_set))
	# return CNF(from_clauses=(sorted(list(clauses_set))))

# def pretty_print_cnf(cnf, cols):
# 	for _ in cnf.clauses:
# 		clause_str = []
# 		for var in _:
# 			r = (abs(var) - 1) // cols
# 			c = (abs(var) - 1) % cols
#
# 			# T(i, j) for True (trap) and G(i, j) for False (gem)
# 			if var > 0:
# 				clause_str.append(f"T({r},{c})")  # True means the cell is a trap
# 			else:
# 				clause_str.append(f"G({r},{c})")  # False means the cell is not a trap (i.e., gem)
#
# 		print(" ∨ ".join(clause_str))