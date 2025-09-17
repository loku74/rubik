import json
from copy import deepcopy

from cube import Cube


def solve(cube: Cube) -> list[str]:
    def is_solved(test: Cube):
        for color in test.cube[Cube.YELLOW]:
            if color != "Y":
                return False
        return True

    if is_solved(cube):
        return []

    oll_moves = json.loads(open("./algorithms/OLL.json").read())
    oll_moves = [oll.split() for oll in oll_moves]

    for oll in oll_moves:
        saved_cube = deepcopy(cube)
        oll_solve_moves = saved_cube.move(oll)
        if is_solved(saved_cube):
            return oll_solve_moves
        for move in ["y", "y'", "y2"]:
            saved_cube = deepcopy(cube)
            oll_solve_moves = saved_cube.move([move] + oll)
            if is_solved(saved_cube):
                return oll_solve_moves

    return []
