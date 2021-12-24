from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class DeterministicDie:

    def __init__(self) -> None:
        self.roll_count = 0

    def roll(self) -> int:
        previous_value = self.roll_count
        self.roll_count += 1
        return previous_value % 100 + 1


def solve(_input: str) -> int:
    positions: list[int] = [int(line.rsplit(" ", 1)[1]) - 1 for line in
                            _input.splitlines()]

    score = [0, 0]
    d = DeterministicDie()
    while True:
        for i in range(2):
            if max(score) >= 1000:
                return score[0 if score[0] < score[1] else 1] * d.roll_count
            positions[i] = (positions[i] + d.roll() + d.roll() + d.roll()) % 10
            score[i] += positions[i] + 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 739785),
    (this_dir / "input.txt", 752247),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
