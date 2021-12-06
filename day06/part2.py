from __future__ import annotations

import argparse
import pathlib
from collections import deque

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def solve(_input: str, days: int = 256) -> int:
    input_lines = [e for e in _input.splitlines()]
    fish_lifetimes = [int(e) for e in input_lines[0].split(",")]

    fishes: deque[int] = deque(maxlen=9)
    for i in range(0, 9):
        fishes.append(fish_lifetimes.count(i))

    for d in range(days):
        breeding = fishes.popleft()
        fishes[6] += breeding
        fishes.append(breeding)

    return sum(fishes)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 26984457539),
    (this_dir / "input.txt", 1622533344325),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
