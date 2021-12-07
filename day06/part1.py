from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class LanternFish:

    def __init__(self, lifetime: int):
        self.lifetime = lifetime

    def __int__(self) -> int:
        return self.lifetime

    def __repr__(self) -> str:
        return f"LanternFish({self.lifetime})"

    def tick(self, fishes: list[LanternFish]) -> None:
        if self.lifetime == 0:
            fishes.append(LanternFish(8))
            self.lifetime = 6
        else:
            self.lifetime -= 1


def solve(_input: str, days: int = 80) -> int:
    input_lines = [e for e in _input.splitlines()]
    fish_lifetimes = [int(e) for e in input_lines[0].split(",")]

    fishes: list[LanternFish] = []

    # Spawn fishes
    for n in fish_lifetimes:
        fishes.append(LanternFish(n))

    for d in range(days):
        for fish in fishes[:]:
            fish.tick(fishes)

    return len(fishes)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 5934),
    (this_dir / "input.txt", 358214),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
