from __future__ import annotations

import argparse
import pathlib
from copy import deepcopy

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()

Board = list[list[str]]
cant_move_to = {3, 5, 7, 9}
cost_to_move = {"A": 1, "B": 10, "C": 100, "D": 1000}
rooms = ["A", "B", "C", "D"]
cache: dict[str, int] = {}


def is_board_done(board: Board) -> bool:
    return ("".join(board[1][1:-1]) == "..........."
            and board[2][3] == board[3][3] == "A"
            and board[2][5] == board[3][5] == "B"
            and board[2][7] == board[3][7] == "C"
            and board[2][9] == board[3][9] == "D")


def hash_board(board: Board) -> str:
    elements = [
        board[1][1],
        board[1][2],
        board[1][4],
        board[1][6],
        board[1][8],
        board[1][10],
        board[1][11],
    ]
    for hash_line in range(2, 6):
        elements.extend([
            board[hash_line][3],
            board[hash_line][5],
            board[hash_line][7],
            board[hash_line][9],
        ])

    return "".join(elements)


def create_possible_steps_costs(board: Board) -> list[tuple[Board, int]]:
    possible_moves: list[tuple[Board, int]] = []
    # Move from rooms
    for room_n in range(4):
        room_column = 2 * (room_n + 1) + 1
        top_y = -1
        for i in range(2, 6):
            top_y = i
            if board[i][room_column] != ".":
                break
        top = board[top_y][room_column]
        if top != "." and (rooms.index(top) != room_n or any(board[i][
                room_column] != top for i in range(top_y + 1, 6))):
            # if not empty room and room is not done
            out_cost = top_y - 1
            for possible_x in (1, 2, 4, 6, 8, 10, 11):
                if possible_x == room_column:
                    continue
                road = board[1][
                    min([possible_x, room_column]):
                    max([possible_x, room_column]) + 1]
                road_clear = all(c == "." for c in road)
                if road_clear:
                    new_board = deepcopy(board)
                    # new_board[1] = deepcopy(board[1])
                    # new_board[top_y] = deepcopy(board[top_y])
                    new_board[top_y][room_column] = "."
                    new_board[1][possible_x] = top
                    possible_moves.append(
                        (new_board,
                         cost_to_move[top] * (out_cost + abs(possible_x
                                                             - room_column))
                         )
                    )
    # Move from hallway
    for moving_x in (1, 2, 4, 6, 8, 10, 11):
        if board[1][moving_x] == ".":
            continue
        moving = board[1][moving_x]
        room_column = 2 * (rooms.index(moving) + 1) + 1
        top_y = -1
        for i in range(5, 1, -1):
            top_y = i
            if board[i][room_column] == ".":
                break
        if any(board[line_check][room_column] != moving for line_check in
               range(top_y + 1, 6)):
            continue
        road = board[1][
            min([moving_x, room_column]): max([moving_x, room_column]) + 1]
        if moving_x > room_column:
            road = road[:-1]
        else:
            road = road[1:]
        road_clear = all(c == "." for c in road)
        if road_clear:
            new_board = deepcopy(board)
            # new_board[1] = deepcopy(board[1])
            # new_board[top_y] = deepcopy(board[top_y])
            new_board[1][moving_x] = "."
            new_board[top_y][room_column] = moving
            possible_moves.append(
                (new_board,
                 cost_to_move[moving] * (top_y - 1 + abs(moving_x
                                                         - room_column))
                 )
            )

    if len(possible_moves) == 0:
        possible_moves = [([], 99999999)]
    return possible_moves


def get_best_solution(board: Board) -> int:
    min_cost = 99999999
    if len(board) > 0:
        board_hash = hash_board(board)
        cached_result = cache.get(board_hash)
        if cached_result is not None:
            return cached_result
        if is_board_done(board):
            return 0
        possible_moves = create_possible_steps_costs(board)
        # possible_moves.sort(key=itemgetter(1))
        for trial_board, move_cost in possible_moves:
            cost = get_best_solution(trial_board) + move_cost
            if cost < min_cost:
                min_cost = cost
        cache[board_hash] = min_cost
    return min_cost


def solve(_input: str) -> int:
    board = [list(read_line) for read_line in _input.splitlines()]
    board.insert(3, list("  #D#C#B#A#"))
    board.insert(4, list("  #D#B#A#C#"))

    return get_best_solution(board)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 44169),
    (this_dir / "input.txt", 40954),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
