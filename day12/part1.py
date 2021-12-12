from __future__ import annotations

import argparse
import pathlib
from collections import defaultdict

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Cave:
    def __init__(self, name: str) -> None:
        self.name = name
        self.neighbours: list[Cave] = []
        self.big = all(map(lambda e: e < "a", self.name))

    def __repr__(self) -> str:
        return f"Cave({self.name})"


class CaveDefaultDict(defaultdict[str, Cave]):
    def __missing__(self, key: str) -> Cave:
        self[key] = Cave(key)
        return self[key]


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    caves: dict[str, Cave] = CaveDefaultDict()

    for n in input_lines:
        lhs, rhs = n.split("-", 1)
        lhs_cave = caves[lhs]
        rhs_cave = caves[rhs]
        lhs_cave.neighbours.append(rhs_cave)
        rhs_cave.neighbours.append(lhs_cave)

    def calculate_paths(
            cave: Cave,
            current_path: list[Cave],
            all_paths: list[list[Cave]],
    ) -> None:
        current_path_copy = current_path[:]
        current_path_copy.append(cave)
        if cave == caves["end"]:
            all_paths.append(current_path_copy)
        for neighbour_cave in cave.neighbours:
            if neighbour_cave.big or neighbour_cave not in current_path:
                calculate_paths(neighbour_cave, current_path_copy, all_paths)

    _all_paths: list[list[Cave]] = []
    calculate_paths(caves["start"], [], _all_paths)
    return len(_all_paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 10),
    (this_dir / "sample_input2.txt", 19),
    (this_dir / "sample_input3.txt", 226),
    (this_dir / "input.txt", 4885),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
