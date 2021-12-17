from __future__ import annotations

import argparse
import pathlib
from typing import NamedTuple

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Position(NamedTuple):
    x: int
    y: int


class Rectangle:
    def __init__(
            self,
            x: str,
            y: str,
    ) -> None:
        self.x_min, self.x_max = map(int, x.split("..", 1))
        self.y_min, self.y_max = map(int, y.split("..", 1))

    def __contains__(self, pos: Position) -> bool:
        return self.x_min <= pos.x <= self.x_max \
            and self.y_min <= pos.y <= self.y_max


def try_trajectory(
        speed: Position,
        rectangle: Rectangle,
) -> int:
    max_height = 0
    pos = Position(0, 0)
    while speed.y >= rectangle.y_min:
        # Move
        pos = Position(pos.x + speed.x, pos.y + speed.y)
        # Save max height potentially
        max_height = max(pos.y, max_height)
        if pos in rectangle:
            return max_height
        # Calculate new speed
        if speed.x < 0:
            new_x_speed = speed.x + 1
        elif speed.x > 0:
            new_x_speed = speed.x - 1
        else:
            new_x_speed = speed.x
        speed = Position(new_x_speed, speed.y - 1)
    return 0


def solve(_input: str) -> int:
    input_line = _input.splitlines()[0][13:]
    lhs, rhs = input_line.split(", ", 1)

    rectangle = Rectangle(lhs[2:], rhs[2:])
    max_heights: list[int] = []
    for x in range(0, rectangle.x_min):
        for y in range(0, 2 * max(abs(rectangle.y_min), abs(rectangle.y_max))):
            max_height = try_trajectory(Position(x, y), rectangle)
            if max_height > 0:
                max_heights.append(max_height)

    return max(max_heights)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 45),
    (this_dir / "input.txt", 12090),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
