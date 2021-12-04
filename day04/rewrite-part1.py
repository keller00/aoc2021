from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class BingoBoard:
    def __init__(self, numbers: list[list[int]]):
        self.numbers = numbers
        self.done: int | None = None
        self.marked: list[list[bool]] = [[False for _ in line]
                                         for line in numbers]

    def is_done(self) -> bool:
        if self.done is not None:
            # Short circuit
            return True
        for line in self.marked:
            if all(line):
                self.done = self._calculate_score()
                return True
        for row in range(len(self.marked[0])):
            row_nums = [line[row] for line in self.marked]
            if all(row_nums):
                self.done = self._calculate_score()
                return True
        return False

    def mark(self, n: int) -> None:
        if self.done is not None:
            return
        for i, line in enumerate(self.numbers):
            for j, number in enumerate(line):
                if number == n:
                    self.marked[i][j] = True

    def _calculate_score(self) -> int:
        sum = 0
        for i, line in enumerate(self.marked):
            for j, marked in enumerate(line):
                if not marked:
                    sum += self.numbers[i][j]
        return sum


def solve(_input: str) -> int:
    input_numbers = _input.splitlines()
    nums = [int(e) for e in input_numbers[0].split(',')]
    boards: list[BingoBoard] = []

    building_board: list[list[int]] = []
    board_strs = input_numbers[2:]
    for line in board_strs:
        if line == "":
            boards.append(BingoBoard(building_board))
            building_board = []
            continue
        building_board.append([int(e) for e in line.split()])
    boards.append(BingoBoard(building_board))
    for n in nums:
        for b in boards:
            b.mark(n)
        for b in boards:
            if b.is_done():
                return (b.done or -1) * n
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
