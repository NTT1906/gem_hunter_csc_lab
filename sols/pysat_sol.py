from pysat.solvers import Solver
from ._isol import *

class PysatSolution(ISolution):
	def solve(self, grid: Grid, cnf: CNF) -> Result | None:
		solver = Solver(bootstrap_with=cnf)
		if solver.solve():
			model = solver.get_model()
			return Result(model)
		return None