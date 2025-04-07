import time
from pysat.formula import CNF

Grid = list[list[int]]
Model = list[int]
Clause = list[int]

class Result:
	model: Model | None
	elapsed_time: float
	def __init__(self, model: Model = None, elapsed_time: float = 0.0):
		self.model = model if not None else [] # fail-safe
		self.elapsed_time = elapsed_time

class ISolver:
	def solve(self, grid: Grid, cnf: CNF) -> Result | None:
		raise NotImplementedError("Must be implemented in subclasses.")