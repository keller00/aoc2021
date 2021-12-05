from __future__ import annotations

import argparse
import pathlib
from typing import NamedTuple

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Coordinate(NamedTuple):
    x: int
    y: int


class Line(NamedTuple):
    start: Coordinate
    end: Coordinate

    def all_points_covered(self) -> list[Coordinate]:
        # direction = TODO
        if self.start.x == self.end.x:
            return [Coordinate(self.start.x, i) for i in
                    range(min(self.start.y, self.end.y),
                          max(self.start.y, self.end.y) + 1)]
        return [Coordinate(i, self.start.y) for i in
                range(min(self.start.x, self.end.x),
                      max(self.start.x, self.end.x) + 1)]


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    solution = 0
    lines: list[Line] = []

    for line in input_lines:
        lhs, rhs = line.split(" -> ")
        lines.append(
            Line(Coordinate(*map(int, lhs.split(","))),
                 Coordinate(*map(int, rhs.split(","))))
        )

    filtered_lines = [line for line in lines if line.start.x ==
                      line.end.x or line.start.y == line.end.y]
    xs = [line.start.x for line in filtered_lines] + \
        [line.end.x for line in filtered_lines]
    ys = [line.start.y for line in filtered_lines] + \
        [line.end.y for line in filtered_lines]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)
    # Create Board
    board: list[list[int]] = []
    width = max_x - min_x
    height = max_y - min_y
    for _ in range(height + 1):
        building_line = []
        for _ in range(width + 1):
            building_line.append(0)
        board.append(building_line)
    # Draw lines
    for drawing_line in filtered_lines:
        for x, y in drawing_line.all_points_covered():
            board[y - min_y][x - min_x] += 1

    for counting_line in board:
        for num in counting_line:
            if num > 1:
                solution += 1

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
    (this_dir / "sample_input.txt", 5),
    (this_dir / "input.txt", 6267),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
