from isol import *
from pysat.solvers import Solver

class PysatSolution(ISolution):
	def __init__(self):
		super(PysatSolution, self).__init__()

	def solve(self, grid, cnf: CNF):
		rows, cols = len(grid), len(grid[0])
		solver = Solver(bootstrap_with=cnf)
		if solver.solve():
			model = solver.get_model()
			return Result(model)
		return None