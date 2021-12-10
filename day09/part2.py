from __future__ import annotations

import argparse
import pathlib
from functools import reduce

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Location:

    def __init__(self, height: int) -> None:
        self.height = height
        self.neighbours: list[Location] = []
        self.low_point = False
        self.risk_level = -1

    def add_neighbours(self, neighbours: list[Location]) -> None:
        self.neighbours = neighbours
        self.low_point = all(map(lambda e: e.height > self.height, neighbours))
        if self.low_point:
            self.risk_level = 1 + self.height
        else:
            self.risk_level = 0

    def get_basin(self) -> set[Location]:
        basin: set[Location] = {self}
        basin_cont: list[Location] = []
        for n in self.neighbours:
            if 9 > n.height > self.height:
                basin_cont.append(n)
        for b in basin_cont:
            basin = basin | b.get_basin()
        return set(basin)

    def __repr__(self) -> str:
        return f"Location({self.height})"


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    solution = 0

    board: list[list[Location]] = []
    for line in input_lines:
        current_line: list[Location] = []
        for c in line:
            current_line.append(Location(int(c)))
        board.append(current_line)

    # Add neighbours
    for j, s in enumerate(board):
        for i, x in enumerate(s):
            neighbours = []
            if i != 0:
                neighbours.append(s[i - 1])
            if i != (len(s) - 1):
                neighbours.append(s[i + 1])
            if j != 0:
                neighbours.append(board[j - 1][i])
            if j != (len(board) - 1):
                neighbours.append(board[j + 1][i])
            x.add_neighbours(neighbours)

    basins: list[set[Location]] = []  # TODO: type-hint
    for row in board:
        for cell in row:
            if cell.low_point:
                basins.append(cell.get_basin())
                solution += cell.risk_level

    basin_lens = sorted((len(b) for b in basins), reverse=True)
    return reduce(lambda a, b: a * b, basin_lens[0:3])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 1134),
    # (this_dir / "input.txt", solution),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
