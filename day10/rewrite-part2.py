from __future__ import annotations

import argparse
import pathlib
from functools import reduce

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()

correction_score = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def solve(_input: str) -> int:
    input_lines = _input.splitlines()

    left_over_stacks: list[list[str]] = []
    for line in input_lines:
        stack: list[str] = []
        for char in line:
            if char in {"(", "[", "{", "<"}:
                stack.append(char)
            else:
                if ((char == ")" and stack.pop() == "(")
                        or (char == "]" and stack.pop() == "[")
                        or (char == "}" and stack.pop() == "{")
                        or (char == ">" and stack.pop() == "<")):
                    continue
                else:
                    break
        else:
            left_over_stacks.append(stack)

    completion_scores = [reduce(lambda a, b: a * 5 + b,
                                scores[:: -1], 0) for scores in
                         [[correction_score[e] for e in s]
                          for s in left_over_stacks]]
    completion_scores.sort()
    return completion_scores[len(completion_scores) // 2]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 288957),
    (this_dir / "input.txt", 1685293086),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
