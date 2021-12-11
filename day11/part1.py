from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Octopus:

    def __init__(self, energy: int, neighbours: list[Octopus] | None = None):
        self.energy = energy
        self.flashed = False
        self.neighbours = neighbours if neighbours is not None else []

    def __repr__(self) -> str:
        return f"({self.energy})"

    def increase_energy(self) -> None:
        self.energy += 1
        if not self.flashed and self.energy > 9:
            self.flashed = True
            for neighbour in self.neighbours:
                neighbour.increase_energy()


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    solution = 0

    board: list[list[Octopus]] = []
    for line in input_lines:
        board.append([Octopus(int(c)) for c in line])
    for n, neighbour_line in enumerate(board):
        for m, neighbour_octopus in enumerate(neighbour_line):
            neighbours: list[Octopus] = []
            if m != 0:
                # left
                neighbours.append(neighbour_line[m-1])
                if n != 0:
                    # above left
                    neighbours.append(board[n - 1][m - 1])
                if n != len(board) - 1:
                    # under left
                    neighbours.append(board[n + 1][m - 1])
            if m != len(neighbour_line) - 1:
                # right
                neighbours.append(neighbour_line[m+1])
                if n != 0:
                    # above right
                    neighbours.append(board[n - 1][m + 1])
                if n != len(board) - 1:
                    # under right
                    neighbours.append(board[n + 1][m + 1])
            if n != 0:
                # above
                neighbours.append(board[n - 1][m])
            if n != len(board) - 1:
                # under
                neighbours.append(board[n + 1][m])
            neighbour_octopus.neighbours = neighbours

    for _ in range(100):
        for step_line in board:
            for increase_octopus in step_line:
                increase_octopus.increase_energy()

        for reset_line in board:
            for reset_octopus in reset_line:
                if reset_octopus.flashed:
                    solution += 1
                    reset_octopus.energy = 0
                    reset_octopus.flashed = False

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
    (this_dir / "sample_input.txt", 1656),
    (this_dir / "input.txt", 1603),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
