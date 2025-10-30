import argparse
import sys

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

    if args.random is not None:
        spins = args.random
        if spins <= 0:
            parser.error("Number of spins must be positive")

        try:
            cube, moves = randomCube(spins)
            print("Shuffle:", " ".join(moves))
            print(f"{'-' * (len(' '.join(moves)) + 9)}")
            solve_moves = cube.solve()
            print("Solution:", " ".join(solve_moves), f"[{len(solve_moves)} spins]")
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.sequence:
        spin_sequence = args.sequence.split()

        for spin in spin_sequence:
            if spin not in valid_spin:
                parser.error(f"Invalid spin: {spin}")

        cube = Cube()
        cube.move(spin_sequence)
        solve_sequence = cube.solve()
        print(" ".join(solve_sequence), f"[{len(solve_sequence)} spins]")


if __name__ == "__main__":
    main()
