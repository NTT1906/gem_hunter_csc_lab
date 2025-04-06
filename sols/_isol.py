from pysat.formula import CNF

Grid = list[list[int]]
Model = list[int]
Clause = list[int]

class Result:
	model: Model | None
	def __init__(self, model: Model = None):
		self.model = model if not None else [] # fail-safe

class ISolution:
	def solve(self, grid: Grid, cnf: CNF) -> Result | None:
		raise NotImplementedError("Must be implemented in subclasses.")