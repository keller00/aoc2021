from __future__ import annotations

import argparse
import pathlib
from collections import Counter
from operator import itemgetter

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()

rules: dict[tuple[str, str], str] = {}


def solve(_input: str) -> int:
    input_lines = _input.splitlines()

    polymer_template: list[str] = list(input_lines[0])

    for rule in input_lines[2:]:
        lhs, rhs = rule.split(" -> ", 1)
        rules[tuple(lhs)] = rhs  # type: ignore

    for _ in range(10):
        i = 0
        while i < len(polymer_template) - 1:
            key = (polymer_template[i], polymer_template[i + 1])
            if key in rules:
                polymer_template.insert(i + 1, rules[key])
                i += 2
                continue
            i += 1
    counter = Counter(polymer_template)
    sorted_elements: list[tuple[str, int]] = sorted(counter.items(),
                                                    key=itemgetter(1))

    return sorted_elements[-1][1] - sorted_elements[0][1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 1588),
    (this_dir / "input.txt", 3406),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
