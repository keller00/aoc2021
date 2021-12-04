from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def solve(_input: str) -> int:
    input_numbers = [
        e.split(" ", 1) for e in _input.splitlines()]

    depth = 0
    position = 0
    aim = 0
    for command, m in input_numbers:
        n = int(m)
        if command == "forward":
            position += n
            depth += aim * n
        elif command == "up":
            aim -= n
        elif command == "down":
            aim += n
        else:
            raise Exception(f"what is {command}")

    return position * depth


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 900),
    (this_dir / "input.txt", 1857958050),
])
def test_sample_data(
        input_file: pathlib.Path,
        expected_result: tuple[int, int],
) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
