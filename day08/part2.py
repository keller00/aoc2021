from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


digit_segments = (
    ('a', 'b', 'c', 'e', 'f', 'g'),  # 0
    ('c', 'f'),  # 1
    ('a', 'c', 'd', 'e', 'g'),  # 2
    ('a', 'c', 'd', 'f', 'g'),  # 3
    ('b', 'c', 'd', 'f'),  # 4
    ('a', 'b', 'd', 'f', 'g'),  # 5
    ('a', 'b', 'd', 'e', 'f', 'g'),  # 6
    ('a', 'c', 'f'),  # 7
    ('a', 'b', 'c', 'd', 'e', 'f', 'g'),  # 8
    ('a', 'b', 'c', 'd', 'f', 'g'),  # 9
)


# Notes:
# * 1 is the only number that uses 2 segments
# * 4 is the only number that uses 4 segments
# * 7 is the only number that uses 3 segments
# * 8 is the only number that uses 7 segments
#
# * 2, 3, 5 are the only numbers using 5 segments, they differ in bc and ef
#   * 2 is one difference from 3 and 5 is also 1 difference away from 5
#
# * 0, 6, 9 are the only numbers using 6 segments, they differ in ce 0 misses d

def get_edge_differences(a: str, b: str) -> set[str]:
    return set(a) - set(b)


def get_edge_differences_length(a: str, b: str) -> int:
    return len(get_edge_differences(a, b))


def solve(_input: str) -> int:
    input_lines = _input.splitlines()  # TODO: put this line in template
    puzzle_input = []
    solution = 0
    for line in input_lines:
        lhs, rhs = line.split(' | ')
        # puzzle_input.append((set(lhs.split()), rhs.split()))
        puzzle_input.append(({"".join(sorted(e)) for e in lhs.split()}, [
                            "".join(sorted(e)) for e in rhs.split()]))

    for input_seqs, outputs in puzzle_input:
        nums = set(outputs) | input_seqs
        guesses: dict[int, str | None] = {i: None for i in range(10)}
        for i in nums:
            # Obvious ones
            if len(i) == 2:
                guesses[1] = i
            elif len(i) == 3:
                guesses[7] = i
            elif len(i) == 4:
                guesses[4] = i
            elif len(i) == 7:
                guesses[8] = i
        # Find 2, 3, 5
        len_5 = {e for e in nums if len(e) == 5}
        assert len(len_5) <= 3
        if len(len_5) == 3:
            for a in len_5:
                rest_5 = set(len_5) - {a}
                if all(
                        [get_edge_differences_length(
                            a, x) == 1 for x in rest_5]
                ):
                    guesses[3] = a
                    break
            # 0, 6, 9
            len_6 = {e for e in nums if len(e) == 6}
            for i in len_6:
                if len(set(i) - set(guesses[3])) == 1:  # type: ignore
                    guesses[9] = i
                    rest_6 = len_6 - {i}
                    for i in rest_5:
                        if len(set(guesses[9]) - set(i)) == 1:  # type: ignore
                            guesses[5] = i
                            guesses[2] = (rest_5 - {i}).pop()
                            break
                    else:
                        raise Exception("cant' find 5")
                    # 0 vs 6
                    for i in rest_6:
                        if len(set(i) - set(guesses[7])) == 3:  # type:ignore
                            guesses[0] = i
                            guesses[6] = (rest_6 - {i}).pop()
                            break
                    else:
                        raise Exception("Couldn't find 0")
                    digit_map = {v: k for k, v in guesses.items()}
                    solution += int("".join(str(digit_map[o])
                                    for o in outputs))

        else:
            raise Exception("can't find 2, 3, 5")

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
    (this_dir / "sample_input.txt", 61229),
    (this_dir / "input.txt", 990964),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
