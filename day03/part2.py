from __future__ import annotations

import argparse
import pathlib
from copy import deepcopy
from typing import Sequence

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def find_most_common_bit(_input: Sequence[str], pos: int) -> str:
    counters = [0, 0]
    for i in _input:
        counters[int(i[pos])] += 1
    if counters[0] > counters[1]:
        return "0"
    return "1"


def filter_input(_input: Sequence[str], filter: str, pos: int) -> list[str]:
    return [e for e in _input if e[pos] == filter]


def find_oxygen_generator_rating(_input: Sequence[str]) -> str:
    left_over = deepcopy(_input)
    cur_pos = 0
    while len(left_over) > 1:
        mcb = find_most_common_bit(left_over, cur_pos)
        left_over = filter_input(left_over, mcb, cur_pos)
        cur_pos += 1
    return left_over[0]


def find_co2_generator_rating(_input: Sequence[str]) -> str:
    left_over = deepcopy(_input)
    cur_pos = 0
    while len(left_over) > 1:
        lcb = "1" if find_most_common_bit(left_over, cur_pos) == "0" else "0"
        left_over = filter_input(left_over, lcb, cur_pos)
        cur_pos += 1
    return left_over[0]


def solve(_input: str) -> int:
    input_numbers = [e for e in _input.splitlines()]

    counters = []
    for _ in input_numbers[0]:
        counters.append(deepcopy([0, 0]))
    # _gamma_rate = "".join(find_most_common_bit(input_numbers, i)
    #                       for i in range(len(input_numbers[0])))
    # _epsilon_rate = "".join(["0" if c == "1" else "1" for c in _gamma_rate])
    ogr = find_oxygen_generator_rating(input_numbers)
    co2gr = find_co2_generator_rating(input_numbers)

    return int(ogr, 2) * int(co2gr, 2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 230),
    (this_dir / "input.txt", 6940518),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
