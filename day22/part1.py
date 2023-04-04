from __future__ import annotations

import argparse
import pathlib
from typing import NamedTuple, Generator

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Range(NamedTuple):
    from_: int
    to: int


class Cube(NamedTuple):
    on: bool
    x: Range
    y: Range
    z: Range

    def __iter__(self) -> Generator[Coordinate, None, None]:
        for x in range(max(self.x.from_, -50), min(self.x.to + 1, 51)):
            for y in range(max(self.y.from_, -50), min(self.y.to + 1, 51)):
                for z in range(max(self.z.from_, -50), min(self.z.to + 1, 51)):
                    yield Coordinate(x, y, z)

    def __contains__(self, item: Cube | Coordinate) -> bool:
        if isinstance(item, Cube):
            return all(c in self for c in item)  # Expensive
        elif isinstance(item, Coordinate):
            return (
                self.x.from_ <= item.x <= self.x.to
                and self.y.from_ <= item.y <= self.y.to
                and self.z.from_ <= item.z <= self.z.to
            )

    def overlaps(self, item: Cube) -> bool:
        return any(c in self for c in item)


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    solution = 0

    steps: list[Cube] = []
    for n in input_lines:
        on, rest = n.split(" ", 1)
        current_cube = Cube(on.lower() == "on", *map(lambda e: Range(*sorted(map(int, e[2:].split("..")))), rest.split(",", 2)))
        # TODO: this isn't correct -60, 60 would be disregarded
        # if (
        #     abs(current_cube.x.to) > 50 and abs(current_cube.x.from_) > 50
        #     and abs(current_cube.y.to) > 50 and abs(current_cube.y.from_) > 50
        #     and abs(current_cube.z.to) > 50 and abs(current_cube.z.from_) > 50
        # ):
        #     continue
        steps.append(current_cube)
    on_cubes: set[Coordinate] = set()
    for s in steps:
        for c in s:
            if (
                abs(c.x) > 50
                or abs(c.y) > 50
                or abs(c.z) > 50
            ):
                continue
            if s.on:
                on_cubes.add(c)
            elif c in on_cubes:
                on_cubes.remove(c)

    return len(on_cubes)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "small_sample_input.txt", 39),
    (this_dir / "sample_input.txt", 590784),
    (this_dir / "input.txt", 610196),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
