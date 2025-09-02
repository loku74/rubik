from copy import deepcopy

from cube import Cube
from f2l import is_f2l_valid


def randomCube():
    cube = Cube()
    k = 0
    moves = []
    max_moves = 20
    while k < max_moves:
        move = cube.randomMove()
        moves.append(move)
        k += 1
    return cube, moves


def solve_white_cross(cube: Cube):
    def first_step(cube: Cube):
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

    def second_step(cube: Cube):
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

    while not first_step(cube):
        k = 0
        cube = deepcopy(saved_cube)
        func_list = []
        test += 1
        while k < 6:
            move = cube.randomMove()
            func_list.append(move)
            k += 1
            if first_step(cube):
                break

    saved_cube = deepcopy(cube)

    while not second_step(cube):
        k = 0
        cube = deepcopy(saved_cube)
        second_func_list = []
        test += 1
        while k < 6:
            move = cube.randomMove(cross=True)
            second_func_list.append(move)
            k += 1
            if second_step(cube):
                break

    final_list = func_list + second_func_list
    return cube, final_list, test


def test_white_cross():
    cube, moves = randomCube()
    _, solved_moves, test = solve_white_cross(cube)
    print(cube)
    print("Shuffle moves:", moves)
    print("Solved moves:", solved_moves, len(solved_moves))
    print("Tests:", test)
    str = "-" * 35
    print(str)


def test_f2l():
    cube, moves = randomCube()
    solved_cube, solved_moves, _ = solve_white_cross(cube)
    print(solved_cube)
    print("Shuffle moves:", moves)
    print("Solved moves:", solved_moves, len(solved_moves))
    edge_pairs, corner_pairs = is_f2l_valid(solved_cube)
    print("Edge pairs:", edge_pairs)
    print("Corner pairs:", corner_pairs)


test_f2l()
