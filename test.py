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


count = 0
while True:
    cube, shuffle_moves = randomCube()
    solve_moves = cube.solve()
    if not cube.is_solved():
        print(cube)
        print("solve moves:", solve_moves)
        print("shuffle moves:", shuffle_moves)
        break
    count += 1
    print(count)
