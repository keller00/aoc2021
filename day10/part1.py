from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()

illegal_score = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    solution = 0

    for line in input_lines:
        stack: list[str] = []
        for char in line:
            if char in {"(", "[", "{", "<"}:
                # Opening char
                stack.append(char)
            else:
                if ((char == ")" and stack.pop() == "(")
                        or (char == "]" and stack.pop() == "[")
                        or (char == "}" and stack.pop() == "{")
                        or (char == ">" and stack.pop() == "<")):
                    continue
                else:
                    solution += illegal_score[char]

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
    (this_dir / "sample_input.txt", 26397),
    (this_dir / "input.txt", 271245),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
