from __future__ import annotations

import argparse

import pytest


def check_number(number: int) -> bool:
    x: int = 0
    z: int = 0
    w: int = 0

    digits = map(int, iter(str(number)))

    w = next(digits)
    x = z % 26 + 11
    if x != w:
        z = 26 * z + (w + 5)

    w = next(digits)
    x = z % 26 + 13
    if x != w:
        z = 26 * z + (w + 5)

    w = next(digits)
    x = z % 26 + 12
    if x != w:
        z = 26 * z + (w + 1)

    w = next(digits)
    x = z % 26 + 15
    if x != w:
        z = 26 * z + (w + 15)

    w = next(digits)
    x = z % 26 + 10
    if x != w:
        z = 26 * z + (w + 2)

    w = next(digits)
    x = z % 26 - 1
    z = z // 26
    if x != w:
        z = 26 * z + (w + 2)

    w = next(digits)
    x = z % 26 + 14
    if x != w:
        z = 26 * z + (w + 5)

    w = next(digits)
    x = z % 26 - 8
    z = z // 26
    if x != w:
        z = 26 * z + (w + 8)

    w = next(digits)
    x = z % 26 - 7
    z = z // 26
    if x != w:
        z = 26 * z + (w + 14)

    w = next(digits)
    x = z % 26 - 8
    z = z // 26
    if x != w:
        z = 26 * z + (w + 12)

    w = next(digits)
    x = z % 26 + 11
    if x != w:
        z = 26 * z + (w + 7)

    w = next(digits)
    x = z % 26 - 2
    z = z // 26
    if x != w:
        z = 26 * z + (w + 14)

    w = next(digits)
    x = z % 26 - 2
    z = z // 26
    if x != w:
        z = 26 * z + (w + 13)

    w = next(digits)
    x = z % 26 - 13
    z = z // 26
    if x != w:
        z = 26 * z + (w + 6)

    return z == 0


def main() -> int:
    argparse.ArgumentParser()
    return 0


@pytest.mark.parametrize("number", [
    96918996924991,
    91811241911641,
])
def test_sample_data(number: int) -> None:
    assert check_number(number)


if __name__ == "__main__":
    raise SystemExit(main())
