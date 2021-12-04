from __future__ import annotations

import argparse
import pathlib
from copy import deepcopy

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def solve(_input: str) -> int:
    input_numbers = [e for e in _input.splitlines()]

    counters = []
    for _ in input_numbers[0]:
        counters.append(deepcopy([0, 0]))
    for n in input_numbers:
        for i, c in enumerate(n):
            counters[i][int(c)] += 1
    gamma_rate = "".join(["0" if i[0] > i[1] else "1" for i in counters])
    epsilon_rate = "".join(["0" if c == "1" else "1" for c in gamma_rate])

    return int(gamma_rate, 2) * int(epsilon_rate, 2)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 198),
    (this_dir / "input.txt", 3009600),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
