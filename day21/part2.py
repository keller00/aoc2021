from __future__ import annotations

import argparse
import pathlib
from collections import defaultdict
from typing import NamedTuple

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


combinations = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


class Game(NamedTuple):
    pos1: int
    pos2: int
    score1: int
    score2: int
    last_played: int


def is_done(game: Game) -> bool:
    return any([game.score1 >= 21, game.score2 >= 21])


def solve(_input: str) -> int:
    positions: list[int] = [int(line.rsplit(" ", 1)[1]) - 1 for line in
                            _input.splitlines()]

    games: dict[Game, int] = defaultdict(int)
    games[Game(positions[0], positions[1], 0, 0, 1)] = 1

    while not all([is_done(game) for game in games]):
        new_games: dict[Game, int] = defaultdict(int)
        for game, starting_num in games.items():
            if is_done(game):
                new_games[game] += starting_num
                continue
            for rolls, n_combinations in combinations.items():
                new_position = ((game.pos1
                                if game.last_played == 1
                                else game.pos2) + rolls) % 10
                new_game = Game(
                    pos1=(new_position
                          if game.last_played == 1
                          else game.pos1),
                    pos2=(new_position
                          if game.last_played == 0
                          else game.pos2),
                    score1=game.score1 + ((new_position + 1)
                                          if game.last_played == 1
                                          else 0),
                    score2=game.score2 + ((new_position + 1)
                                          if game.last_played == 0
                                          else 0),
                    last_played=0 if game.last_played == 1 else 1,
                )
                new_games[new_game] += starting_num * n_combinations
        games = new_games
    wins: list[int] = [0, 0]
    for game, num in games.items():
        if game.score1 >= 21:
            wins[0] += num
        else:
            wins[1] += num
    return max(wins)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 444356092776315),
    # (this_dir / "input.txt", 752247),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
