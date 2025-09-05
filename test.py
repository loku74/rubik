import f2l
import oll
from cube import Cube
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
    f2l_moves = f2l.solve(solved_cube)
    print("F2L moves:", f2l_moves)
    print(solved_cube)
    oll_moves = oll.solve(solved_cube)
    print("OLL moves:", oll_moves)
    solved_cube.move(oll_moves)
    print(solved_cube)


test_f2l()
