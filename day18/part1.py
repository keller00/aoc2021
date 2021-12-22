from __future__ import annotations

import argparse
import pathlib
from typing import Any
from typing import Generator

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Pair:
    def __init__(
            self,
            lhs: Pair | int,
            rhs: Pair | int,
            parent: Pair | None = None,
    ) -> None:
        self.lhs = lhs
        self.rhs = rhs
        self.parent = parent

    def __repr__(self) -> str:
        return f"[{self.lhs}, {self.rhs}]"

    @property
    def level(self) -> int:
        level = 0
        current_pair: Pair | None = self
        while current_pair is not None:
            level += 1
            current_pair = current_pair.parent
        return level

    def __iter__(self) -> Generator[Pair, None, None]:
        if isinstance(self.lhs, Pair):
            yield from iter(self.lhs)
        yield self
        if isinstance(self.rhs, Pair):
            yield from iter(self.rhs)


def turn_lists_into_pairs(node: Any) -> Pair | int:
    if isinstance(node, int):
        return node
    else:
        assert len(node) == 2, "Wrong input?"
        return Pair(
            turn_lists_into_pairs(node[0]),
            turn_lists_into_pairs(node[1]),
        )


def calculate_magnitude(node: Pair | int) -> int:
    if isinstance(node, int):
        return node
    else:
        return 3 * calculate_magnitude(node.lhs) + 2 * calculate_magnitude(
            node.rhs)


def add_parents(node: Pair) -> None:
    if isinstance(node.lhs, Pair):
        node.lhs.parent = node
        add_parents(node.lhs)
    if isinstance(node.rhs, Pair):
        node.rhs.parent = node
        add_parents(node.rhs)


def add_to_left_element(node: Pair, n: int) -> None:
    current_node: Pair = node
    # Keep going up until parent exists, and it's left child isn't where we
    #  came form
    while current_node.parent is not None and current_node.parent.lhs == \
            current_node:
        current_node = current_node.parent
    assert isinstance(node.parent, Pair)
    if current_node.parent is None:
        return
    current_node = current_node.parent
    if isinstance(current_node.lhs, int):
        current_node.lhs += n
        return
    current_node = current_node.lhs
    # Now find the right most child in this tree
    while isinstance(current_node.rhs, Pair):
        current_node = current_node.rhs
    current_node.rhs += n


def add_to_right_element(node: Pair, n: int) -> None:
    current_node = node
    while current_node.parent is not None and current_node.parent.rhs == \
            current_node:
        current_node = current_node.parent
    assert isinstance(node.parent, Pair)
    if current_node.parent is None:
        return
    current_node = current_node.parent
    if isinstance(current_node.rhs, int):
        current_node.rhs += n
        return
    current_node = current_node.rhs
    # Now find the right most child in this tree
    while isinstance(current_node.lhs, Pair):
        current_node = current_node.lhs
    current_node.lhs += n


def explode(p: Pair) -> None:
    assert isinstance(p.lhs, int)
    assert isinstance(p.rhs, int)
    add_to_left_element(p, p.lhs)
    add_to_right_element(p, p.rhs)
    assert isinstance(p.parent, Pair)
    if p == p.parent.lhs:
        p.parent.lhs = 0
    elif p == p.parent.rhs:
        p.parent.rhs = 0


def reduce_once(node: Pair) -> bool:
    """Returns whether it reduced anything."""
    for p in iter(node):
        if p.level > 4:
            explode(p)
            return True
    for p in iter(node):
        if isinstance(p.lhs, int) and p.lhs >= 10:
            p.lhs = Pair(int(p.lhs / 2), int(p.lhs / 2 + 0.5), p)
            return True
        elif isinstance(p.rhs, int) and p.rhs >= 10:
            p.rhs = Pair(int(p.rhs / 2), int(p.rhs / 2 + 0.5), p)
            return True
    return False


def reduce(node: Pair) -> None:
    can_reduce = True
    while can_reduce:
        can_reduce = reduce_once(node)


def add(lhs: Pair, rhs: Pair) -> Pair:
    p = Pair(lhs, rhs)
    lhs.parent = p
    rhs.parent = p
    reduce(p)
    return p


def solve(_input: str) -> int:
    input_lines = _input.splitlines()
    snailfish_numbers: list[Pair] = []
    for input_line in input_lines:
        placeholder = dict()  # type: ignore
        exec(f"lists={input_line}", {}, placeholder)
        intermediate_pairs = turn_lists_into_pairs(placeholder["lists"])
        assert isinstance(intermediate_pairs, Pair)
        add_parents(intermediate_pairs)
        snailfish_numbers.append(intermediate_pairs)

    current_number = snailfish_numbers[0]
    for n in snailfish_numbers[1:]:
        current_number = add(current_number, n)

    return calculate_magnitude(current_number)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "sample_input.txt", 4140),
    (this_dir / "input.txt", 3734),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
