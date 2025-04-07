from pysat.solvers import Solver
from .isol import *

class PysatSolution(ISolution):
	def solve(self, grid: Grid, cnf: CNF) -> Result | None:
		elapsed_time = -time.time()
		solver = Solver(bootstrap_with=cnf)
		if solver.solve():
			model = solver.get_model()
			elapsed_time += time.time()
			return Result(model, elapsed_time * 1000)
		return None