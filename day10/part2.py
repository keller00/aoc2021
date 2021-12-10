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

autocomplete_score = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def solve(_input: str) -> int:
    input_lines = _input.splitlines()

    incomplete_lines: list[str] = []
    for line in input_lines:
        building_line = ""
        stack: list[str] = []
        for char in line:
            if char in {"(", "[", "{", "<"}:
                # Opening char
                stack.append(char)
            else:
                if ((char == ")" and stack[-1] == "(")
                        or (char == "]" and stack[-1] == "[")
                        or (char == "}" and stack[-1] == "{")
                        or (char == ">" and stack[-1] == "<")):
                    stack.pop()
                else:
                    break
            building_line += char
        else:
            incomplete_lines.append(building_line)

    solutions: list[int] = []
    for row in incomplete_lines:
        solution = 0
        stack2: list[str] = []
        building_completion = ""
        for char in row[::-1]:
            if char in {")", "]", "}", ">"}:
                stack2.append(char)
            else:
                try:
                    if ((char == "(") and stack2[-1] == ")"
                            or (char == "[" and stack2[-1] == "]")
                            or (char == "{" and stack2[-1] == "}")
                            or (char == "<" and stack2[-1] == ">")):
                        stack2.pop()
                        continue
                    elif char == "(":
                        building_completion += ")"
                        solution = solution * 5 + autocomplete_score[")"]
                    elif char == "[":
                        building_completion += "]"
                        solution = solution * 5 + autocomplete_score["]"]
                    elif char == "{":
                        building_completion += "}"
                        solution = solution * 5 + autocomplete_score["}"]
                    elif char == "<":
                        building_completion += ">"
                        solution = solution * 5 + autocomplete_score[">"]
                except IndexError:
                    if char == "(":
                        building_completion += ")"
                        solution = solution * 5 + autocomplete_score[")"]
                    elif char == "[":
                        building_completion += "]"
                        solution = solution * 5 + autocomplete_score["]"]
                    elif char == "{":
                        building_completion += "}"
                        solution = solution * 5 + autocomplete_score["}"]
                    elif char == "<":
                        building_completion += ">"
                        solution = solution * 5 + autocomplete_score[">"]
        solutions.append(solution)

    solutions.sort()
    return solutions[len(solutions) // 2]


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
