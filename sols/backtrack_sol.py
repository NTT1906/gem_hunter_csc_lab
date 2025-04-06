from ._isol import *

class BacktrackSolution(ISolution):
	@staticmethod
	def dpll(clauses: list[Clause], symbols: list[int], model: Model = []) -> Model | None:
		# print(f"Model: {model}")
		def is_clause_true(clause: Clause) -> bool:
			return any(literal in model for literal in clause)
		def is_clause_false(clause: Clause) -> bool:
			return all(-literal in model for literal in clause)
		def find_pure_symbol() -> int:
			literals = {}
			for clause in clauses:
				for literal in clause:
					if literal in model or -literal in model:
						continue
					if -literal in literals:
						literals[-literal] = False
					elif literal not in literals or literals[literal]:
						literals[literal] = True
			for literal in literals:
				if literals[literal]: # if literal is pure (unchanged in all clauses)
					return literal
			return 0
		def find_unit_clause() -> int:
			assigned = set(abs(literal) for literal in model)
			for clause in clauses:
				unassigned = [literal for literal in clause if abs(literal) not in assigned]
				if len(unassigned) == 1:
					unit_literal = unassigned[0]
					return unit_literal
			return 0

		if all(is_clause_true(clause) for clause in clauses):
			# print("Early exit 1")
			return model
		if any(is_clause_false(clause) for clause in clauses):
			# print("Early exit 2")
			return None

		pure_symbol = find_pure_symbol()
		if pure_symbol != 0:
			# print("PURE SYMBOL", pure_symbol)
			# print(f"Symbols: {symbols}")
			new_symbol = symbols.copy()
			new_symbol.remove(abs(pure_symbol))
			# print(f"New Symbols: {new_symbol}")
			return BacktrackSolution.dpll(clauses, new_symbol, model + [pure_symbol])
		unit_clause = find_unit_clause()
		if unit_clause != 0:
			# print("UNIT SYMBOL", unit_clause)
			new_symbol = symbols.copy()
			new_symbol.remove(abs(unit_clause))
			return BacktrackSolution.dpll(clauses, new_symbol, model + [unit_clause])
		# print("FIRST?", symbols)
		new_symbol = symbols[1:]
		return BacktrackSolution.dpll(clauses, new_symbol, model + [symbols[0]]) or BacktrackSolution.dpll(clauses, new_symbol, model + [-symbols[0]])

	def solve(self, grid: Grid, cnf: CNF) -> Result | None:
		try:
			model = self.dpll(cnf.clauses, list(range(1, len(grid) * len(grid[0]) + 1)), [])
			print(model)
			return Result(model) if model else None
		except RecursionError:
			print("Cringe")
			return None
