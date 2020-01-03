from .droid import *

import pytest  # type: ignore


def parse_map(map_str) -> RepairDroid:
    # program is empty, need to avoid making any moves
    robot = RepairDroid([])

    lines = map_str.strip().split("\n")
    longest_line = max(len(line.strip()) for line in lines)
    for y, line in enumerate(lines):
        for x in range(longest_line):
            if x >= len(line):
                continue
            p = (x, y)
            ch = line[x]
            if ch == "." or ch == "D":
                tile = Tile.TRAVERSABLE
            elif ch == "#":
                tile = Tile.WALL
            robot.ship_map[p] = tile
            if ch == "D":
                robot.pos = p

    return robot


EXAMPLE_MAP = """
..##
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

    # (0,0) is the upper-left position in the map string, not where the robot is
    params = [
        (parse_map(EXAMPLE_MAP), {(0, 0), (1, 0), (0, 1), (0, 2), (3, 3)}),
        (parse_map(EXAMPLE_MAP_NO_EXPLORABLE), set()),
    ]
    ids = ["EXAMPLE_MAP", "EXAMPLE_MAP_NO_EXPLORABLE"]

    @pytest.mark.parametrize("robot,expected_set", params, ids=ids)
    def test_explorable_positions(self, robot: RepairDroid, expected_set):
        explorable = set(robot.explorable_positions())
        assert explorable == expected_set

    @pytest.mark.parametrize("robot,expected_set", params, ids=ids)
    def test_has_explorable_positions(self, robot: RepairDroid, expected_set):
        assert robot.has_explorable_positions() == (len(expected_set) > 0)

    def test_explorable_positions_initial_robot(self):
        robot = RepairDroid([])
        assert set(robot.explorable_positions()) == {(0, 1), (0, -1), (1, 0), (-1, 0)}

    def test_compute_path_optimal(self):
        robot = parse_map(EXAMPLE_MAP)
        # use (0,1) as destination since there are non-optimal routes to it
        dest = (0, 1)

        assert robot.compute_path(dest) == [
            Direction.NORTH,
            Direction.WEST,
            Direction.WEST,
            Direction.WEST,
        ]

    def test_compute_path(self):
        robot = parse_map(EXAMPLE_MAP)
        dest = (0, 0)

        assert robot.compute_path(dest) == [
            Direction.NORTH,
            Direction.WEST,
            Direction.WEST,
            Direction.WEST,
            Direction.NORTH,
        ]
