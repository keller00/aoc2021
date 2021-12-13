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
    min_x = min(xs)
    min_y = min(ys)
    max_x = max(xs)
    max_y = max(ys)
    for _ in range(max_y - min_y + 1):
        building_line = []
        for _ in range(max_x - min_x + 1):
            building_line.append(".")
        board.append(building_line)
    # Mark dots
    for dot in dots:
        board[dot.y - min_y][dot.x - min_x] = "#"

    # Fold papers
    for folding_instruction in fold_instructions[:1]:
        _, _, where = folding_instruction.split()
        plane, line = where.split("=")
        line_int = int(line)
        if plane == "y":
            # Fold up
            for i, fold_line in enumerate(board[line_int + 1:]):
                for e, cell in enumerate(fold_line):
                    if cell == "#":
                        board[line_int - 1 - i - min_y][e] = "#"
            board = board[:line_int]
        else:
            # Fold left
            for i, lfold_line in enumerate(board):
                for e, cell in enumerate(lfold_line[line_int + 1:]):
                    if cell == "#":
                        board[i][line_int - 1 - int(e)] = "#"
            for j in range(len(board)):
                board[j] = board[j][:line_int]
    # Count up hastags
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
    (this_dir / "sample_input.txt", 17),
    (this_dir / "input.txt", 775),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
