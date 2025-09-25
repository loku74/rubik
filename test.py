import datetime
from copy import deepcopy

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
solve_moves_count = 0

now = datetime.datetime.now().timestamp()
while True and count < 1_000:
    cube, shuffle_moves = randomCube()
    initial_cube = deepcopy(cube)
    solve_moves = cube.solve()
    if not cube.is_solved():
        print("shuffle moves:", shuffle_moves)
        print(initial_cube)
        print("solve moves:", solve_moves)
        print(cube)
        break
    initial_cube.move(solve_moves)
    if not initial_cube.is_solved():
        print("solve optimization failed")
        break
    count += 1
    solve_moves_count += len(solve_moves)
    print(count)

after = datetime.datetime.now().timestamp()
time_taken = after - now
avg = time_taken / count
avg_solve_moves = solve_moves_count / count

print(f"Average time taken: {avg:.2f} seconds")
print(f"Average number of solve moves: {avg_solve_moves:.2f}")

# shuffle = [
#     "U2",
#     "L2",
#     "U",
#     "F'",
#     "U",
#     "R'",
#     "L",
#     "B",
#     "L'",
#     "R'",
#     "D2",
#     "R'",
#     "B'",
#     "L2",
#     "U",
#     "F",
#     "D'",
#     "F2",
#     "U2",
#     "D'",
# ]

# moves = [
#     "R",
#     "L'",
#     "F2",
#     "D'",
#     "L2",
#     "D",
#     "L2",
#     "U'",
#     "B",
#     "U2",
#     "B'",
#     "U",
#     "R'",
#     "U'",
#     "R",
# ]

# cube = Cube()
# cube.move(shuffle)
# cube.move(moves)
# print(cube)
# solve_moves = cube.solve()
# print(cube)
# print(" ".join(solve_moves), len(solve_moves) + len(moves))
