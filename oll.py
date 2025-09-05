import json
from copy import deepcopy

from cube import Cube


def solve(cube: Cube):
    def is_solved(test: Cube):
        for color in test.cube[Cube.YELLOW]:
            if color != "Y":
                return False
        return True

    oll_moves = json.loads(open("./algorithms/OLL.json").read())
    oll_moves = [oll.split(" ") for oll in oll_moves]

    for oll in oll_moves:
        for move in ["U", "U'", "U2"]:
            saved_cube = deepcopy(cube)
            saved_cube.move([move])
            oll_solve_moves = saved_cube.move(oll)
            if is_solved(saved_cube):
                return [move] + oll_solve_moves

    return None
