from __future__ import annotations

import argparse
import pathlib

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


def count_lit_pixels(image: list[list[str]]) -> int:
    lit_pixels = 0
    for counting_line in image:
        for c in counting_line:
            if c == "#":
                lit_pixels += 1
    return lit_pixels


def extend_image(image: list[list[str]], default_value: str) -> list[list[
        str]]:
    padding_line: list[str] = []
    for _ in range(len(image[0]) + 2):
        padding_line.append(default_value)
    return [padding_line] + [[default_value, *extending_line, default_value]
                             for extending_line in image] + [
        padding_line]


def get_value(
        image: list[list[str]],
        y: int,
        x: int,
        default_value: str,
) -> str:
    if x < 0 or y < 0 or y >= len(image) or x >= len(image[0]):
        return default_value
    return image[y][x]


def enhance_image(
        image: list[list[str]],
        image_enhancing_algorithm: str,
        default_value: str,
) -> tuple[list[list[str]], str]:
    new_image: list[list[str]] = []
    for y, enhancing_line in enumerate(image):
        building_line: list[str] = []
        for x, c in enumerate(enhancing_line):
            neighbours: list[str] = []
            for looking_y in range(y - 1, y + 2):
                for looking_x in range(x - 1, x + 2):
                    neighbours.append(get_value(image, looking_y, looking_x,
                                                default_value))
            index = int("".join(
                ["1" if e == "#" else "0" for e in neighbours]
            ), 2)
            building_line.append(image_enhancing_algorithm[index])
        new_image.append(building_line)
    return new_image, image_enhancing_algorithm[511 if default_value == "#"
                                                else 0]


def solve(_input: str) -> int:
    input_lines = _input.splitlines()

    image_enhancing_algorithm = input_lines[0]
    image: list[list[str]] = [list(line) for line in input_lines[2:]]
    default_value = "."
    for _ in range(50):
        extended_image = extend_image(image, default_value)
        image, default_value = enhance_image(extended_image,
                                             image_enhancing_algorithm,
                                             default_value)

    return count_lit_pixels(image)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 3351),
    (this_dir / "input.txt", 16728),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
