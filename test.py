import f2l
import oll
import pll
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
    if f2l_moves:
        print("F2L moves:", f2l_moves)
        print(solved_cube)
    oll_moves = oll.solve(solved_cube)
    if oll_moves:
        print("OLL moves:", oll_moves)
        solved_cube.move(oll_moves)
        print(solved_cube)
    pll_moves = pll.solve(solved_cube)
    if pll_moves:
        print("PLL moves:", pll_moves)
        solved_cube.move(pll_moves)
        print(solved_cube)


test_f2l()
