from __future__ import annotations

import argparse
import pathlib
from collections import Counter

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


digit_segments = (
    ('a', 'b', 'c', 'e', 'f', 'g'),  # 0
    ('c', 'f'),  # 1
    ('a', 'c', 'd', 'e', 'g'),  # 2
    ('a', 'c', 'd', 'f', 'g'),  # 3
    ('b', 'c', 'd', 'f'),  # 4
    ('a', 'b', 'd', 'f', 'g'),  # 5
    ('a', 'b', 'd', 'e', 'f', 'g'),  # 6
    ('a', 'c', 'f'),  # 7
    ('a', 'b', 'c', 'd', 'e', 'f', 'g'),  # 8
    ('a', 'b', 'c', 'd', 'f', 'g'),  # 9
)


# Notes:
# * 1 is the only number that uses 2 segments
# * 4 is the only number that uses 4 segments
# * 7 is the only number that uses 3 segments
# * 8 is the only number that uses 7 segments

def solve(_input: str) -> int:
    input_lines = _input.splitlines()  # TODO: put this line in template
    puzzle_input = []
    solution = 0
    for line in input_lines:
        lhs, rhs = line.split(' | ')
        puzzle_input.append((lhs.split(), rhs.split()))

    for _, output_values in puzzle_input:
        c = Counter(map(len, output_values))
        solution += sum([c[2], c[4], c[3], c[7]])

    return solution


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 26),
    (this_dir / "input.txt", 554),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
