from __future__ import annotations

import argparse
import operator
import pathlib
from functools import reduce

import pytest

this_dir = pathlib.Path(__file__).parent.resolve()


class Packet:
    def __init__(self, version: int, _type: int):
        self.version = version
        self.type = _type
        self.packets: list[Packet] = []
        self._rest = ""


class LiteralPacket(Packet):
    def __init__(self, version: int, _input: str):
        super().__init__(version, 4)
        building = ""
        for i in range(0, len(_input), 5):
            ch_gr = _input[i: i + 5]
            building += ch_gr[1:]
            if ch_gr[0] == "0":
                self._rest = _input[i + 5:]
                break
        self.value = int(building, 2)


class OperatorPacket(Packet):
    def __init__(self, version: int, _type: int, _input: str):
        super().__init__(version, _type)
        self.length_type_id = int(_input[0], 2)
        self.packets: list[Packet] = []
        if self.length_type_id == 0:
            self.length = int(_input[1: 16], 2)
            _rest = _input[16:]
            consumed = 0
            while consumed != self.length:
                self.packets.append(read_packet(_rest))
                consumed += len(_rest) - len(self.packets[-1]._rest)
                _rest = self.packets[-1]._rest
        else:
            self.length = int(_input[1: 12], 2)
            _rest = _input[12:]
            for i in range(self.length):
                self.packets.append(read_packet(_rest))
                _rest = self.packets[-1]._rest
        self._rest = _rest


def hex_to_binary(_input: str) -> str:
    return "".join([f"{int(e, 16):04b}" for e in _input])


def read_packet(_input: str) -> Packet:
    read_version = int(_input[0: 3], 2)
    read_type = int(_input[3: 6], 2)
    if read_type == 4:
        return LiteralPacket(read_version, _input[6:])
    else:
        return OperatorPacket(read_version, read_type, _input[6:])


def calculate_value(p: Packet) -> int:
    if isinstance(p, LiteralPacket):
        return p.value
    else:
        values = list(map(calculate_value, p.packets))
        if p.type == 0:
            return sum(values)
        elif p.type == 1:
            return reduce(operator.mul, values)
        elif p.type == 2:
            return min(values)
        elif p.type == 3:
            return max(values)
        elif p.type == 5:
            return 1 if values[0] > values[1] else 0
        elif p.type == 6:
            return 1 if values[0] < values[1] else 0
        elif p.type == 7:
            return 1 if values[0] == values[1] else 0
        raise Exception(f"Unknown packet type: {p.type}")


def solve(_input: str) -> int:
    input_line = hex_to_binary(_input.splitlines()[0])

    p = read_packet(input_line)

    return calculate_value(p)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?',
                        default=str(this_dir / "input.txt"))
    args = parser.parse_args()

    with open(args.data_file) as f:
        print(solve(f.read()))

    return 0


@pytest.mark.parametrize(("input_file", "expected_result"), [
    (this_dir / "part2test1.txt", 3),
    (this_dir / "part2test2.txt", 54),
    (this_dir / "part2test3.txt", 7),
    (this_dir / "part2test4.txt", 9),
    (this_dir / "part2test5.txt", 1),
    (this_dir / "part2test6.txt", 0),
    (this_dir / "part2test7.txt", 0),
    (this_dir / "part2test8.txt", 1),
    (this_dir / "input.txt", 911945136934),
])
def test_sample_data(input_file: pathlib.Path, expected_result: int) -> None:
    assert solve(input_file.read_text()) == expected_result


if __name__ == "__main__":
    raise SystemExit(main())
