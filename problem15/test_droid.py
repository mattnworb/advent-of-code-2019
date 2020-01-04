from .droid import *

import pytest  # type: ignore


class TestPosition:
    def test_as_dict_key(self):
        p = Position(0, 0)
        d = {p: 1}
        assert p in d
        assert d[Position(p.x, p.y)] == 1

    def test_equal(self):
        assert Position(0, 0) == Position(0, 0)


def parse_map(map_str) -> RepairDroid:
    # program is empty, need to avoid making any moves
    robot = RepairDroid([])

    lines = map_str.strip().split("\n")
    longest_line = max(len(line.strip()) for line in lines)
    for y, line in enumerate(lines):
        line = line.strip()
        for x in range(longest_line):
            if x >= len(line):
                continue
            p = Position(x, y)
            ch = line[x]
            if ch == "." or ch == "D":
                tile = Tile.TRAVERSABLE
            elif ch == "#":
                tile = Tile.WALL
            elif ch == "O":
                tile = Tile.OXYGEN_STATION
            else:
                raise ValueError
            robot.ship_map[p] = tile
            if ch == "D":
                robot.pos = p

    return robot


EXAMPLE_MAP = """
..##.
....#
..#D#
###.#
"""

EXAMPLE_MAP_NO_EXPLORABLE = """
####
#..D#
####
"""


class TestRepairDroid:
    def test_bfs_score(self):
        m = """
        ###O#
        #...#
        #...#
        #...#
        #D###
        """
        robot = parse_map(m)
        # sanity check
        assert robot.count_tiles() == {
            "WALL": 4 + 4 + 3 + 3,
            "TRAVERSABLE": 10,
            "OXYGEN_STATION": 1,
        }
        # D is at (1,4)
        dist = robot.bfs_score(Position(1, 4))
        assert dist[Position(1, 4)] == 0
        assert dist[Position(3, 0)] == 6
