from copy import deepcopy

from cube import Cube


def first_step(cube: Cube):
    white_side = cube.cube[Cube.WHITE]
    white_pieces = [white_side[1], white_side[3], white_side[5], white_side[7]]
    yellow_side = cube.cube[Cube.YELLOW]
    yellow_pieces = [yellow_side[1], yellow_side[3], yellow_side[5], yellow_side[7]]
    sum = 0
    for piece in white_pieces:
        if piece == "W":
            sum += 1
    for piece in yellow_pieces:
        if piece == "W":
            sum += 1
    return sum == 4


def second_step(cube: Cube):
    blue_side = cube.cube[Cube.BLUE]
    red_side = cube.cube[Cube.RED]
    green_side = cube.cube[Cube.GREEN]
    orange_side = cube.cube[Cube.ORANGE]
    white_side = cube.cube[Cube.WHITE]
    white_pieces = [white_side[1], white_side[3], white_side[5], white_side[7]]
    for piece in white_pieces:
        if piece != "W":
            return False
    if blue_side[7] != "B":
        return False
    if red_side[7] != "R":
        return False
    if green_side[7] != "G":
        return False
    if orange_side[7] != "O":
        return False
    return True


def do_step(cube: Cube, step, limit: int, cross: bool = False):
    if step(cube):
        return []

    while True:
        saved_cube = deepcopy(cube)
        k = 0
        move_list = []
        while k < limit:
            move = saved_cube.randomMove(cross=cross)
            move_list.append(move)
            k += 1
            if step(saved_cube):
                return move_list


def solve(cube: Cube):
    def optimize_moves(cube: Cube, moves: list[str]):
        i = 0
        while i < len(moves):
            saved_cube = deepcopy(cube)
            moves_copy = moves.copy()
            moves_copy.pop(i)
            saved_cube.move(moves_copy)
            if second_step(saved_cube):
                moves.pop(i)
            else:
                i += 1
        return moves

    initial_cube = deepcopy(cube)

    first_step_limit = 6
    second_step_limit = 6

    first_step_funcs = do_step(cube, first_step, first_step_limit)

    initial_cube.move(first_step_funcs)

    second_step_funcs = do_step(
        initial_cube, second_step, second_step_limit, cross=True
    )

    final_list = first_step_funcs + second_step_funcs
    cube_copy = deepcopy(cube)
    final_list = optimize_moves(cube_copy, final_list)
    return final_list
