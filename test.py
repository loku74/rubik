from cube import Cube
from f2l import is_f2l_valid
from solve import solve_white_cross


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
