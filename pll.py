import json
from copy import deepcopy

from cube import Cube


def is_solved(test: Cube):
    for color in test.cube[Cube.YELLOW]:
        if color != "Y":
            return False
    for color in test.cube[Cube.WHITE]:
        if color != "W":
            return False
    for color in test.cube[Cube.ORANGE]:
        if color != "O":
            return False
    for color in test.cube[Cube.GREEN]:
        if color != "G":
            return False
    for color in test.cube[Cube.BLUE]:
        if color != "B":
            return False
    for color in test.cube[Cube.RED]:
        if color != "R":
            return False
    return True


def solve(cube: Cube):
    pll_moves = json.loads(open("./algorithms/PLL.json").read())
    pll_moves = [pll.split(" ") for pll in pll_moves]

    reverse_move = {"U": "U'", "U'": "U", "U2": "U2"}

    for pll in pll_moves:
        for move in ["U", "U'", "U2"]:
            saved_cube = deepcopy(cube)
            saved_cube.move([move])
            pll_solve_moves = saved_cube.move(pll)
            if is_solved(saved_cube):
                return [move] + pll_solve_moves
            else:
                saved_cube.move([reverse_move[move]])
                if is_solved(saved_cube):
                    return [move] + pll_solve_moves + [reverse_move[move]]

    return None
