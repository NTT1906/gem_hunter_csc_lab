from .isol import *

class BacktrackSolution(ISolution):
	@staticmethod
	def dpll(clauses: list[Clause], symbols: list[int], model: set[int]) -> set[int] | None:
		if model is None:
			model = set()

		def is_clause_true(clause: Clause) -> bool:
			return any(literal in model for literal in clause)
		def is_clause_false(clause: Clause) -> bool:
			return all(-literal in model for literal in clause)
		def find_pure_symbol() -> int:
			literals = {}
			for clause in clauses:
				for literal in clause:
					if literal in model or -literal in model:
					# if abs(literal) not in symbols:
						continue
					if -literal in literals:
						literals[-literal] = False
					elif literal not in literals:
						literals[literal] = True
			for literal in literals:
				if literals[literal]:
					return literal
			return 0
		def find_unit_clause() -> int:
			for clause in clauses:
				if any(literal in model for literal in clause):
					continue  # Clause is already true
				# unassigned_literals = [literal for literal in clause if abs(literal) in symbols]
				unassigned_literals = [literal for literal in clause if literal not in model and not -literal in model]
				if len(unassigned_literals) == 1:
					return unassigned_literals[0]
			return 0

		# early termination
		if all(is_clause_true(clause) for clause in clauses): # faster as they used c++ :D
			return model
		if any(is_clause_false(clause) for clause in clauses):
			return None

		# pure symbol heuristic
		pure_symbol = find_pure_symbol()
		if pure_symbol != 0:
			new_symbols = [s for s in symbols if s != abs(pure_symbol)]
			return BacktrackSolution.dpll(clauses, new_symbols, model | {pure_symbol})

		# unit clause heuristic
		unit_clause = find_unit_clause()
		if unit_clause != 0:
			new_symbols = [s for s in symbols if s != abs(unit_clause)]
			return BacktrackSolution.dpll(clauses, new_symbols, model | {unit_clause})
		new_symbol = symbols[1:]
		return BacktrackSolution.dpll(clauses, new_symbol, model | {symbols[0]}) or BacktrackSolution.dpll(clauses, new_symbol, model | {-symbols[0]})

	def solve(self, grid: Grid, cnf: CNF) -> Result | None:
		elapsed_time = -time.time()
		try:
			# model = self.dpll(cnf.clauses, list(range(1, len(grid) * len(grid[0]) + 1)), set())
			model: set[int] = set()
			symbols = list(range(1, len(grid) * len(grid[0]) + 1))
			rows = len(grid)
			cols = len(grid[0])
			for row in range(rows):
				for col in range(cols):
					if grid[row][col] != 0:
						m = row * cols + col + 1
						model.add(-m)
						symbols.remove(m)

			model = self.dpll(cnf.clauses, symbols, model)
			elapsed_time += time.time()
			return Result(list(model), elapsed_time * 1000) if model else None
		except RecursionError:
			print("Recursion limit reached in BacktrackSolution.solve")
			return None
