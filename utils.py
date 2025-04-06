import time
from itertools import combinations
from pysat.formula import CNF

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

def write_output(file_path, grid):
	"""
	Writes the grid to output file.
	"""
	with open(file_path, 'w') as f:
		for row in grid:
			f.write(', '.join(row) + '\n')

def update_grid(grid, model):
	"""
	Updates the grid according to the given model.
	:param model: a dict mapping cell with its value (True = Trap, False = Gem)
	"""
	if model is not None:
		rows = len(grid)
		for mapping, value in enumerate(model):
			row = (mapping - 1) // rows
			col = (mapping - 1) % rows
			grid[row][col] = 'T' if value else 'G'
	return grid

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
	Convert grid to CNF.
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

				for comb in combinations(neighbors, neighbors_count - trap_amount + 1):
					clauses_set.add(tuple((r * cols + c + 1) for r, c in comb))

				# At most 'trap_amount' traps
				# For each combination of (trap_amount + 1) neighbors, at least one must NOT be a trap
				if trap_amount < neighbors_count:  # Only if we need some non-traps
					for comb in combinations(neighbors, trap_amount + 1):
						clause = tuple(-(r * cols + c + 1) for r, c in comb)
						clauses_set.add(clause)
	# return CNF(from_clauses=(list(clauses_set)))
	return CNF(from_clauses=(sorted(list(clauses_set))))

def pretty_print_cnf(cnf, cols):
	for _ in cnf.clauses:
		clause_str = []
		for var in _:
			r = (abs(var) - 1) // cols
			c = (abs(var) - 1) % cols

			# T(i, j) for True (trap) and G(i, j) for False (gem)
			if var > 0:
				clause_str.append(f"T({r},{c})")  # True means the cell is a trap
			else:
				clause_str.append(f"G({r},{c})")  # False means the cell is not a trap (i.e., gem)

		print(" ∨ ".join(clause_str))

def optimize_cnf(cnf: CNF, knowledge_base) -> CNF:
	_optimized_cnf = CNF()

	for _clause in cnf.clauses:
		is_clause_satisfied = False

		# check if the clause is satisfied by any literal in the knowledge base
		for var in _clause:
			# if var is in knowledge base, and its truth value matches the clause's literal, it satisfies the clause
			if (var > 0 and knowledge_base.get(var, None) is True) or (var < 0 and knowledge_base.get(abs(var), None) is False):
				is_clause_satisfied = True
				break

		# if the clause is not satisfied, add it to the optimized CNF
		if not is_clause_satisfied:
			_optimized_cnf.append(_clause)

	return _optimized_cnf
