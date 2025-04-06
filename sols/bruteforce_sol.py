import os, sys
from itertools import combinations
from ._isol import *

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils import get_neighbors

class BruteforceSolution(ISolution):
	def solve(self, grid: Grid, cnf: CNF) -> Result | None:
		rows, cols = len(grid), len(grid[0])
		unknown_cells = []
		# # NOTE: This code will add all including those not surrounding number... which may let to bruteforce to return
		# # false result
		# for i in range(rows):
		# 	for j in range(cols):
		# 		if grid[i][j] == 0:
		# 			unknown_cells.append((i, j))
		for i in range(rows):
			for j in range(cols):
				if grid[i][j] != 0:
					for r, c in get_neighbors(grid, i, j):
						if grid[r][c] == 0 and (r, c) not in unknown_cells:
							unknown_cells.append((r, c))
		# unknown_cells.sort(key=lambda x: x[0] * cols + x[1])

		def is_valid_model(_model):
			for row in range(rows):
				for col in range(cols):
					number = grid[row][col]
					if number == 0:
						continue
					if number != sum((trow, tcol) in _model for trow, tcol in get_neighbors(grid, row, col)):
						return False
			return True

		unknown_cells_len = len(unknown_cells)
		for trap_count in range(unknown_cells_len, -1, -1):
			for traps in combinations(unknown_cells, trap_count):
				if is_valid_model(traps):
					model = []
					for i in range(rows):
						for j in range(cols):
							# # uncomment this and place the following code to its scope to remove numbered cell
							#if grid[i][j] == 0:
							sign = 1 if (i, j) in traps else -1
							model.append(sign * (i * cols + j + 1))
					return Result(model)

					# if you only want some results and not numbered cells/non-neighboring gem cells
					# for r, c in unknown_cells:
					# 	sign = 1 if (r, c) in traps else -1
					# 	model.append(sign * (r * cols + c + 1))
					# return Result(model)
		return None