import f2l
import oll
import pll
import white_cross
from cube import Cube


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


def test_f2l():
    cube, moves = randomCube()
    white_cross_moves = white_cross.solve(cube)
    cube.move(white_cross_moves)
    print(cube)
    print("Shuffle moves:", moves)
    print("Solved moves:", white_cross_moves, len(white_cross_moves))
    f2l_moves = f2l.solve(cube)
    if f2l_moves:
        print("F2L moves:", f2l_moves, len(f2l_moves))
        print(cube)
    # PRENDRE EN COMPTE QUE LES OLL / PLL PEUVENT ETRE SKIP
    # VERIFIER AVANT POUR FAIRE UNE OLL QUE LA FACE JAUNE EST VIDE
    # IDEM POUR PLL VERIFIER QUE LE CUBE N'EST PAS RESOLU (AVEC U U' ET U2 AUSSI!!)
    oll_moves = oll.solve(cube)
    if oll_moves:
        print("OLL moves:", oll_moves)
        cube.move(oll_moves)
        print(cube)
    pll_moves = pll.solve(cube)
    if pll_moves:
        print("PLL moves:", pll_moves)
        cube.move(pll_moves)
        print(cube)
        print(
            "total spins:",
            len(pll_moves) + len(oll_moves) + len(f2l_moves),
        )


test_f2l()
