from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    crabs = [int(e) for e in input_lines[0].split(",")]
    solutions = {}

    for n in range(min(crabs), max(crabs)+1):
        solutions[n] = 0
        for crab in crabs:
            solutions[n] += abs(crab - n)
    return min(solutions.values())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 37),
    (this_dir / "input.txt", 344605),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
