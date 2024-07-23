from __future__ import annotations

import argparse
import pathlib
from typing import Generator
from typing import NamedTuple

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

    def iter(self) -> Generator[Coordinate, None, None]:
        for x in range(self.x.from_, self.x.to + 1):
            for y in range(self.y.from_, self.y.to + 1):
                for z in range(self.z.from_, self.z.to + 1):
                    yield Coordinate(x, y, z)

    def corners(self) -> Generator[Coordinate, None, None]:
        for x in (self.x.from_, self.x.to):
            for y in (self.y.from_, self.y.to):
                for z in (self.z.from_, self.z.to):
                    yield Coordinate(x, y, z)

    def __contains__(self, item: object) -> bool:
        if isinstance(item, Cube):
            for c in item.corners():
                if c not in self:
                    return False
            return True
        elif isinstance(item, Coordinate):
            return (
                self.x.from_ <= item.x <= self.x.to
                and self.y.from_ <= item.y <= self.y.to
                and self.z.from_ <= item.z <= self.z.to
            )
        else:
            raise TypeError("unsupported type")

    # def overlaps(self, item: Cube) -> int:
    #     return any(c in self for c in item)

    def volume(self) -> int:
        return (
            (self.x.to + 1 - self.x.from_)
            * (self.y.to + 1 - self.y.from_)
            * (self.z.to + 1 - self.z.from_)
        )


class Coordinate(NamedTuple):
    x: int
    y: int
    z: int


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    # solution = 0

    steps: list[Cube] = []
    for n in input_lines:
        on, rest = n.split(" ", 1)
        current_cube = Cube(
            on.lower() == "on",
            *map(
                lambda e: Range(
                    *sorted(map(int, e[2:].split("..")))
                ),
                rest.split(",", 2)
            )
        )
        steps.append(current_cube)
    seen_cubes: set[Coordinate] = set()
    on_cubes = 0
    for s in reversed(steps):
        for c in s.iter():
            if c not in seen_cubes:
                seen_cubes.add(c)
                if s.on:
                    on_cubes += 1

    return on_cubes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "part2_sample_input.txt", 2758514936282235),
    # (this_dir / "input.txt", 610196),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
