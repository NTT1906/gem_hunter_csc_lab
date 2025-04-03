from pysat.formula import CNF

class Result:
	model: list[int] | None
	def __init__(self, model: list[int] = None):
		self.model = model

class ISolution:
	def solve(self, grid, cnf: CNF) -> Result | None:
		raise NotImplementedError("Must be implemented in subclasses.")