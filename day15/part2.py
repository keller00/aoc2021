from __future__ import annotations

import argparse
import heapq
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def solve(_input: str) -> int:
    initial_board = _input.splitlines()

    board: list[str] = []
    for repeat_y in range(0, 5):
        for repeat_line in initial_board:
            building_board = ""
            for repeat_x in range(0, 5):
                for e in repeat_line:
                    new_num = int(e) + repeat_x + repeat_y
                    building_board += str(new_num % 10 + (1 if new_num > 9
                                                          else 0))
            board.append(building_board)

    lines = len(board)
    rows = len(board[0])
    # Build second board
    cost_to_finish: list[list[int]] = []
    for build_line in board:
        building_line = []
        for _ in build_line:
            building_line.append(0)
        cost_to_finish.append(building_line)

    heap: list[tuple[int, int, int]] = []
    current_x = rows - 1
    current_y = lines - 1
    heapq.heappush(heap, (int(board[-1][-1]), current_y, current_x))
    while True:
        cost_to_visit, current_y, current_x = heapq.heappop(heap)
        if cost_to_finish[current_y][current_x] != 0:
            continue
        cost_to_finish[current_y][current_x] = cost_to_visit
        if current_x == 0 and current_y == 0:
            break
        # right
        if (current_x != rows - 1 and cost_to_finish[current_y][current_x + 1]
                == 0):
            new_x = current_x + 1
            heapq.heappush(heap, (cost_to_visit + int(board[current_y][
                new_x]),
                current_y,
                new_x))
        # left
        if current_x != 0 and cost_to_finish[current_y][current_x - 1] == 0:
            new_x = current_x - 1
            heapq.heappush(heap, (cost_to_visit + int(board[current_y][
                new_x]),
                current_y,
                new_x))
        # down
        if (current_y != lines - 1 and cost_to_finish[current_y + 1][
                current_x] == 0):
            new_y = current_y + 1
            heapq.heappush(heap, (cost_to_visit + int(board[new_y][
                current_x]),
                new_y,
                current_x))
        # up
        if current_y != 0 and cost_to_finish[current_y - 1][current_x] == 0:
            new_y = current_y - 1
            heapq.heappush(heap, (cost_to_visit + int(board[new_y][
                current_x]),
                new_y,
                current_x))
    return cost_to_finish[0][0] - int(board[0][0])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 315),
    (this_dir / "input.txt", 2957),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
