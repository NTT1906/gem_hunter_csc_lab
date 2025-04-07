import os
import sys
from .isol import *
from itertools import combinations

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.utils import get_neighbors

class BruteforceSolver(ISolver):
    def solve(self, grid: Grid, cnf: CNF) -> Result | None:
        elapsed_time = -time.time()
        rows, cols = len(grid), len(grid[0])
        unknown_cells = set()

        # cached neighbors as bruteforce might call to get_neighbors quite a lot!
        # neighbors_cache = {(i, j): get_neighbors(grid, i, j) for i in range(rows) for j in range(cols) if grid[i][j] == 0}
        neighbors_cache = {(i, j): get_neighbors(grid, i, j) for i in range(rows) for j in range(cols)}

        for i in range(rows):
            for j in range(cols):
                # # NOTE: This code will add all including those not surrounding number... which may let to bruteforce
                # # to return false result
                # if grid[i][j] == 0:
                #     unknown_cells.add((i, j))
                if grid[i][j] != 0:
                    for r, c in neighbors_cache[(i, j)]:
                        if grid[r][c] == 0:
                            unknown_cells.add((r, c))

        def is_model_satisfied(_model):
            trap_set = set(_model)
            for row in range(rows):
                for col in range(cols):
                    number = grid[row][col]
                    if number == 0:
                        continue
                    if number != sum((r, c) in trap_set for r, c in neighbors_cache[(row, col)]):
                        return False
            return True

        for trap_count in range(len(unknown_cells), -1, -1):
            for traps in combinations(unknown_cells, trap_count):
                if is_model_satisfied(traps):
                    elapsed_time += time.time()
                    return Result([r * cols + c + 1 for r, c in traps], elapsed_time * 1000)
                    # model = []
                    # for i in range(rows):
                    #     for j in range(cols):
                    #         uncomment this and place the following code to its scope to remove numbered cell
                            # if grid[i][j] == 0:
                            # sign = 1 if (i, j) in traps else -1
                            # model.append(sign * (i * cols + j + 1))
                    # return Result(model)
                    # # if you only want some results and not numbered cells/non-neighboring gem cells
                    # for r, c in unknown_cells:
                    # 	sign = 1 if (r, c) in traps else -1
                    # 	model.append(sign * (r * cols + c + 1))
                    # return Result(model)

        return None
