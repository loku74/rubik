import json
from copy import deepcopy

from cube import Cube


def solve(cube: Cube) -> list[str]:
    pll_moves = json.loads(open("./algorithms/PLL.json").read())
    pll_moves = [pll.split() for pll in pll_moves]

    if cube.is_solved():
        return []

    # first check if it only needs rotations
    for move in ["U", "U'", "U2"]:
        saved_cube = deepcopy(cube)
        moves = saved_cube.move([move])
        if saved_cube.is_solved():
            return moves

    for pll in pll_moves:
        for y in [None, "y", "y'", "y2"]:
            saved_cube = deepcopy(cube)
            if y:
                pll_solve_moves = saved_cube.move([y] + pll)
            else:
                pll_solve_moves = saved_cube.move(pll)
            if saved_cube.is_solved():
                return pll_solve_moves
            for move in ["U", "U'", "U2"]:
                saved_cube = deepcopy(cube)
                if y:
                    pll_solve_moves = saved_cube.move([y] + pll + [move])
                else:
                    pll_solve_moves = saved_cube.move(pll + [move])
                if saved_cube.is_solved():
                    return pll_solve_moves

    return []
