from __future__ import annotations

import argparse
import pathlib

input_file = pathlib.Path(__file__).parent / "input.txt"


def solve(_input: str) -> int:
    input_numbers = [int(e) for e in _input.splitlines()]
    solution = -1

    for n in input_numbers:
        # TODO
        pass

    return solution


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=str(input_file))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
