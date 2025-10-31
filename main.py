#!/usr/bin/env python3

import argparse

from cube import Cube, randomCube


def main():
    parser = argparse.ArgumentParser(
        description="Rubik's Cube solver - Apply spin sequences or generate random cubes",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 main.py "U R U' L'"
  python3 main.py --random
  python3 main.py --random 30
  python3 main.py -r 50

Valid spins: U, U', U2, D, D', D2, F, F', F2, B, B', B2, L, L', L2, R, R', R2
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "sequence",
        type=str,
        nargs="?",
        help="Spin sequence (e.g., \"U R U' L'\")",
    )

    group.add_argument(
        "-r",
        "--random",
        type=int,
        nargs="?",
        const=20,
        metavar="SPINS",
        help="Generate a random cube with optional number of spins (default: 20)",
    )

    parser.add_argument(
        "-d",
        "--display",
        action="store_true",
        help="Display the cube",
    )

    args = parser.parse_args()

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

    if args.random:
        spins = args.random
        if spins <= 0:
            parser.error("Number of spins must be positive")

        cube, moves = randomCube(spins)
        print("Shuffle:", " ".join(moves))
        print(f"{'-' * (len(' '.join(moves)) + 9)}")
    else:
        spin_sequence = args.sequence.split()
        for spin in spin_sequence:
            if spin not in valid_spin:
                parser.error(f"Invalid spin: {spin}")

        cube = Cube()
        cube.move(spin_sequence)

    if args.display:
        print(cube)

    solve_moves = cube.solve()
    print("Solution:", " ".join(solve_moves), f"[{len(solve_moves)} spins]")

    if args.display:
        print(cube)


if __name__ == "__main__":
    main()
