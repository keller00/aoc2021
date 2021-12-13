from __future__ import annotations

import argparse
import pathlib
from typing import NamedTuple

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Dot(NamedTuple):
    x: int
    y: int


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    solution = 0

    dots: list[Dot] = []
    board: list[list[str]] = []
    for i, read_line in enumerate(input_lines):
        if read_line == "":
            fold_instructions: list[str] = input_lines[i + 1:]
            break
        dots.append(Dot(*map(int, read_line.split(",", 1))))
    else:
        raise Exception("OOps")
    # Build board
    xs = [e.x for e in dots]
    ys = [e.y for e in dots]
    max_x = max(xs)
    max_y = max(ys)
    for _ in range(max_y + 1):
        building_line = []
        for _ in range(max_x + 1):
            building_line.append(".")
        board.append(building_line)
    # Mark dots
    for dot in dots:
        board[dot.y][dot.x] = "#"

    # Fold papers
    for folding_instruction in fold_instructions:
        _, _, where = folding_instruction.split()
        plane, line = where.split("=")
        line_int = int(line)
        if plane == "y":
            # Fold up
            for i, fold_line in enumerate(board[line_int + 1:]):
                for e, cell in enumerate(fold_line):
                    if cell == "#":
                        board[line_int - 1 - i][e] = "#"
            board = board[:line_int]
        else:
            # Fold left
            for lfold_y, lfold_line in enumerate(board):
                for lfold_x, cell in enumerate(lfold_line[line_int + 1:]):
                    if cell == "#":
                        board[lfold_y][line_int - 1 - lfold_x] = "#"
                board[lfold_y] = board[lfold_y][:line_int]

    # Count up hashtags
    for count_line in board:
        for cell in count_line:
            if cell == "#":
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
    (this_dir / "sample_input.txt", 16),
    (this_dir / "input.txt", 102),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
