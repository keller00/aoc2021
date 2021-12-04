from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def mark_all_n(boards: list[list[list[list[int | bool]]]], num: int) -> None:
    for b in boards:
        for line in b:
            for n in line:
                if n[0] == num:
                    n[1] = True


def calculate_score(board: list[list[list[int | bool]]]) -> int:
    sum = 0
    for line in board:
        for n, marked in line:
            if not marked:
                sum += n
    return sum


def has_board_won(board: list[list[list[int | bool]]]) -> bool:
    for line in board:
        won = True
        for n, marked in line:
            if not marked:
                won = False
        if won:
            return True
    for r in range(len(board[0])):
        won = True
        for line in board:
            n, marked = line[r]
            if not marked:
                won = False
        if won:
            return True

    return False


def solve(_input: str) -> int:
    input_numbers = _input.splitlines()
    nums = [int(e) for e in input_numbers[0].split(',')]
    boards: list[list[list[list[int | bool]]]] = []

    building_board: list[list[list[int | bool]]] = []
    board_strs = input_numbers[2:]
    for line in board_strs:
        if line == "":
            boards.append(building_board)
            building_board = []
            continue
        building_board.append([[int(e), False] for e in line.split()])
    boards.append(building_board)
    for n in nums:
        mark_all_n(boards, n)
        for b in boards:
            if has_board_won(b):
                return calculate_score(b) * n
    raise Exception("We should never reach this")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 4512),
    (this_dir / "input.txt", 8580),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
