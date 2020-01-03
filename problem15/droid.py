from collections import defaultdict
from typing import Dict, Tuple, Optional
from enum import Enum, unique
from computer import Computer, RunResult


@unique
class Tile(Enum):
    WALL = "#"
    UNKNOWN = " "
    TRAVERSABLE = "."
    OXYGEN_STATION = "O"


@unique
class Direction(Enum):
    # Only four movement commands are understood: north (1), south (2), west (3), and east (4)
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    @staticmethod
    def from_str(s: str) -> "Direction":
        if s == "N":
            return Direction.NORTH
        if s == "S":
            return Direction.SOUTH
        if s == "W":
            return Direction.WEST
        if s == "E":
            return Direction.EAST
        raise ValueError()


Position = Tuple[int, int]
ShipMap = Dict[Position, Tile]


def add_to_position(position: Position, direction: Direction) -> Position:
    if direction == Direction.NORTH:
        return (position[0], position[1] - 1)
    if direction == Direction.SOUTH:
        return (position[0], position[1] + 1)
    if direction == Direction.WEST:
        return (position[0] - 1, position[1])
    if direction == Direction.EAST:
        return (position[0] + 1, position[1])

    raise ValueError()


class RepairDroid:
    def __init__(self, program):
        self.computer = Computer(
            program, initial_memory_size=2000, max_memory_length=10000
        )
        self.ship_map: ShipMap = defaultdict(lambda: Tile.UNKNOWN)
        self.pos = (0, 0)
        self.oxygen_station_pos = None

        outputs, result = self.computer.run(until_blocked=True)
        assert result == RunResult.BLOCK_ON_INPUT, f"result was unexpected {result}"

    def known_map(self) -> ShipMap:
        """Return a copy of the known map"""
        return dict(self.ship_map)

    def current_pos(self) -> Position:
        return self.pos

    def oxygen_station(self) -> Optional[Position]:
        return self.oxygen_station_pos

    def has_explorable_positions(self) -> bool:
        """Test if there are any positions on the map with unknown regions next to them."""
        for position, tile in self.ship_map.items():
            if tile != Tile.TRAVERSABLE:
                continue
            for d in Direction:
                sibling = add_to_position(position, d)
                if self.ship_map[sibling] == Tile.UNKNOWN:
                    return True
        return False

    def count_tiles(self) -> Dict[Tile, int]:
        c: Dict[Tile, int] = {}
        for position, tile in self.ship_map.items():
            if tile not in c:
                c[tile] = 1
            else:
                c[tile] += 1
        return c

    def move_once(self, direction: Direction):
        self.computer.add_input(direction.value)
        outputs, result = self.computer.run(until_blocked=True)

        assert (
            result == RunResult.BLOCK_ON_INPUT
        ), f"result was unexpected {result}. outputs: {outputs}"
        assert len(outputs) == 1
        output = outputs[0]

        # The repair droid can reply with any of the following status codes:
        #
        # - 0: The repair droid hit a wall. Its position has not changed.
        # - 1: The repair droid has moved one step in the requested direction.
        # - 2: The repair droid has moved one step in the requested direction;
        #   its new position is the location of the oxygen system.
        assert output in [0, 1, 2]

        intended = add_to_position(self.pos, direction)

        if output == 0:
            self.ship_map[intended] = Tile.WALL

        if output == 1:
            self.ship_map[intended] = Tile.TRAVERSABLE
            self.pos = intended

        if output == 2:
            self.ship_map[intended] = Tile.OXYGEN_STATION
            self.pos = intended

    def print_screen(self):
        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        for position in self.ship_map:
            x, y = position
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        assert min_x <= max_x
        assert min_y <= max_y

        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                if self.pos == (x, y):
                    ch = "D"
                else:
                    ch = self.ship_map[(x, y)].value
                line += ch
            print(line)
