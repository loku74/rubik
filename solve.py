from copy import deepcopy

from cube import Cube


def solve_white_cross(cube: Cube):
    def first_step():
        white_side = cube.cube[cube.WHITE]
        white_pieces = [white_side[1], white_side[3], white_side[5], white_side[7]]
        yellow_side = cube.cube[cube.YELLOW]
        yellow_pieces = [yellow_side[1], yellow_side[3], yellow_side[5], yellow_side[7]]
        sum = 0
        for piece in white_pieces:
            if piece == "W":
                sum += 1
        for piece in yellow_pieces:
            if piece == "W":
                sum += 1
        return sum == 4

    def second_step():
        blue_side = cube.cube[cube.BLUE]
        red_side = cube.cube[cube.RED]
        green_side = cube.cube[cube.GREEN]
        orange_side = cube.cube[cube.ORANGE]
        white_side = cube.cube[cube.WHITE]
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

    saved_cube = deepcopy(cube)

    func_list = []
    second_func_list = []
    test = 0

    while not first_step():
        k = 0
        cube = deepcopy(saved_cube)
        func_list = []
        test += 1
        while k < 6:
            move = cube.randomMove()
            func_list.append(move)
            k += 1
            if first_step():
                break

    saved_cube = deepcopy(cube)

    while not second_step():
        k = 0
        cube = deepcopy(saved_cube)
        second_func_list = []
        test += 1
        while k < 6:
            move = cube.randomMove(cross=True)
            second_func_list.append(move)
            k += 1
            if second_step():
                break

    final_list = func_list + second_func_list
    return cube, final_list, test
