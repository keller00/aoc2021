from __future__ import annotations

import argparse
import pathlib

import pytest

input_file = pathlib.Path(__file__).parent / "input.txt"


def solve(_input: str) -> int:
    input_numbers = [int(e) for e in _input.splitlines()]
    solution = 0

    previous = input_numbers[0]
    for n in input_numbers[1:]:
        if n > previous:
            solution += 1
        previous = n

    return solution


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=str(input_file))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (pathlib.Path(__file__).parent / "sample_input.txt", 7),
    (pathlib.Path(__file__).parent / "input.txt", 1557),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
