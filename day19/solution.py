from __future__ import annotations

import argparse
import pathlib
import re

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()

SCANNER_LINE_RE = re.compile(r"--- scanner (\d+) ---")


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    solution = 0
    detected_beacons: dict[int, list[tuple[int, int, int]]] = dict()
    current_scanner: int | None = None

    for i, n in enumerate(input_lines):
        if n == "":
            continue
        new_scanner = SCANNER_LINE_RE.fullmatch(n)
        if new_scanner:
            current_scanner = int(new_scanner.group(1))
            detected_beacons[current_scanner] = list()
            continue
        if current_scanner is None:
            raise Exception(f"this should never have happened line {i} '{n}'")
        detected_beacons[current_scanner].append(tuple(n.split(",")))

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
    (this_dir / "sample_input.txt", 79),
    # (this_dir / "input.txt", solution),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
