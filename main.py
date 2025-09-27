import sys

from cube import Cube, randomCube


def exit(error):
    usage = 'Usage: python3 main.py "<spin_sequence>" | random | random:<spins>'
    print(error, file=sys.stderr)
    print(usage, file=sys.stderr)
    sys.exit(1)


def main():
    argc = len(sys.argv)
    if argc < 2:
        exit("Error. Spin sequence required")
    if argc > 2:
        exit("Error. Too many arguments")

    valid_spin = [
        "U",
        "U'",
        "U2",
        "D",
        "D'",
        "D2",
        "F",
        "F'",
        "F2",
        "B",
        "B'",
        "B2",
        "L",
        "L'",
        "L2",
        "R",
        "R'",
        "R2",
    ]
    input = sys.argv[1]
    if input[:6] == "random":
        spins = 20
        random_input = input.split(":")
        if len(random_input) > 2:
            exit("Error. Too many arguments")
        elif len(random_input) == 2:
            try:
                spins = int(random_input[1])
            except Exception:
                exit("Error. Invalid number of spins")
        try:
            cube, moves = randomCube(spins)
            print("Shuffle:", " ".join(moves))
            print(f"{'-' * (len(' '.join(moves)) + 9)}")
            solve_moves = cube.solve()
            print("Solution:", " ".join(solve_moves), f"[{len(solve_moves)} spins]")
        except Exception as e:
            exit(f"Error. {e}")
    else:
        spin_sequence = input.split()
        for spin in spin_sequence:
            if spin not in valid_spin:
                exit(f"Error. Invalid spin: {spin}")

        cube = Cube()
        cube.move(spin_sequence)
        solve_sequence = cube.solve()
        print(" ".join(solve_sequence))


if __name__ == "__main__":
    main()
