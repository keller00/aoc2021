from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def solve(_input: str) -> int:
    board = _input.splitlines()

    lines = len(board)
    rows = len(board[0])
    cost_to_finish: list[list[int]] = []
    for build_line in board:
        building_line = []
        for _ in build_line:
            building_line.append(0)
        cost_to_finish.append(building_line)

    for y in range(lines - 1, -1, -1):
        for x in range(rows - 1, -1, -1):
            if y == lines - 1 and x == rows - 1:
                cost_to_finish[y][x] = int(board[y][x])
                continue
            to_consider: list[int] = []
            # right
            if x != rows - 1:
                to_consider.append(cost_to_finish[y][x + 1])
            # bottom
            if y != lines - 1:
                to_consider.append(cost_to_finish[y + 1][x])
            cost_to_finish[y][x] = min(to_consider) + (
                0 if x == 0 and y == 0 else int(board[y][x]))

    return cost_to_finish[0][0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 40),
    (this_dir / "input.txt", 687),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
