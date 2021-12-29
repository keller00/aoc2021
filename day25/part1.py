from __future__ import annotations

import argparse
import pathlib
from itertools import count

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()

Board = list[list[str]]


def do_east_move(
        board: Board,
        new_board: Board | None = None,
) -> tuple[Board, int]:
    moved = 0
    if new_board is None:
        new_board = [["." for _ in recreate_line]
                     for recreate_line in board]
    width = len(board[0])
    for y, move_line in enumerate(board):
        for x, cell in enumerate(move_line):
            if cell == ">":
                new_x = x + 1
                if new_x == width:
                    new_x = 0
                if board[y][new_x] == ".":
                    new_board[y][new_x] = ">"
                    moved += 1
                else:
                    new_board[y][x] = cell
            elif cell != ".":
                new_board[y][x] = cell
    return new_board, moved


def do_south_move(
        board: Board,
        new_board: Board | None = None
) -> tuple[Board, int]:
    moved = 0
    if new_board is None:
        new_board = [["." for _ in recreate_line]
                     for recreate_line in board]
    height = len(board)
    for y, move_line in enumerate(board):
        for x, cell in enumerate(move_line):
            if cell == "v":
                new_y = y + 1
                if new_y == height:
                    new_y = 0
                if board[new_y][x] == ".":
                    new_board[new_y][x] = "v"
                    moved += 1
                else:
                    new_board[y][x] = cell
            elif cell != ".":
                new_board[y][x] = cell

    return new_board, moved


def do_one_move(board: Board) -> tuple[Board, int]:
    board, moved_east = do_east_move(board)
    board, moved_south = do_south_move(board)
    return board, moved_east + moved_south


def solve(_input: str) -> int:
    board: Board = [list(read_line) for read_line in _input.splitlines()]

    for i in count(1):
        board, moved = do_one_move(board)
        if moved == 0:
            return i
    raise Exception("Should never reach this")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 58),
    (this_dir / "input.txt", 568),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
