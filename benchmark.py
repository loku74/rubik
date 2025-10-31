#!/usr/bin/env python3

import datetime
from copy import deepcopy

from cube import randomCube

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

print("Number of rubiks cube solved:", count)
print(f"Average time per solve: {avg:.2f} seconds")
print(f"Average number of solve moves: {avg_solve_moves:.2f}")
