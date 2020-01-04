from collections import Counter
from typing import Dict, Tuple, Optional, Iterator, List, Set, Union
from enum import Enum, unique
from computer import Computer, RunResult
import time


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

    def opposite(self):
        if self == Direction.NORTH:
            return Direction.SOUTH

        if self == Direction.SOUTH:
            return Direction.NORTH

        if self == Direction.EAST:
            return Direction.WEST

        if self == Direction.WEST:
            return Direction.EAST

        raise ValueError

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


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other) -> "Position":
        if isinstance(other, Direction):
            if other == Direction.NORTH:
                return Position(self.x, self.y - 1)

            if other == Direction.SOUTH:
                return Position(self.x, self.y + 1)

            if other == Direction.WEST:
                return Position(self.x - 1, self.y)

            if other == Direction.EAST:
                return Position(self.x + 1, self.y)

        return NotImplemented

    def __lt__(self, value):
        if isinstance(value, Position):
            return (self.x, self.y) < (value.x, value.y)
        return NotImplemented

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, value):
        return isinstance(value, Position) and self.x == value.x and self.y == value.y

    def __repr__(self):
        return f"Position({self.x}, {self.y})"


ShipMap = Dict[Position, Tile]


class RepairDroid:
    def __init__(self, program):
        self.computer = Computer(
            program, initial_memory_size=2000, max_memory_length=10000
        )
        self.ship_map: ShipMap = {}

        # the robot's initial position is traversable by definition
        self.pos = Position(0, 0)
        self.ship_map[self.pos] = Tile.TRAVERSABLE

        self.oxygen_station_pos = None

        self.moves_attempted = 0
        self.moves_made = 0

    def current_pos(self) -> Position:
        return self.pos

    def oxygen_station(self) -> Optional[Position]:
        return self.oxygen_station_pos

    def nonwall_neighbors(
        self, node: Position, allow_unknown=True
    ) -> Iterator[Position]:
        """Return the non-WALL neighors of a given node. Will return UNKNOWN neighbors."""
        for d in Direction:
            sibling = node + d
            if self.ship_map.get(sibling) != Tile.WALL:
                yield sibling

    def count_tiles(self) -> Dict[str, int]:
        return dict(Counter(tile.name for tile in self.ship_map.values()))

    def move_once(self, direction: Direction):
        self.computer.add_input(direction.value)

        # start = time.monotonic()
        outputs, result = self.computer.run(until_blocked=True)
        # elapsed = time.monotonic() - start
        # print(f"Computer run took {elapsed} seconds")

        self.moves_attempted += 1

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

        intended = self.pos + direction

        if output == 0:
            self.ship_map[intended] = Tile.WALL

        if output == 1:
            self.ship_map[intended] = Tile.TRAVERSABLE
            self.pos = intended
            self.moves_made += 1

        if output == 2:
            self.ship_map[intended] = Tile.OXYGEN_STATION
            self.pos = intended
            self.oxygen_station_pos = intended
            self.moves_made += 1

    def print_screen(self):
        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        for position in self.ship_map:
            x, y = position.x, position.y
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)

        assert min_x <= max_x
        assert min_y <= max_y

        for y in range(min_y, max_y + 1):
            line = ""
            for x in range(min_x, max_x + 1):
                p = Position(x, y)
                if p == self.pos:
                    ch = "D"
                elif p == (0, 0):
                    ch = "S"
                else:
                    ch = self.ship_map.get(p, Tile.UNKNOWN).value
                line += ch
            print(line)

    def bfs_score(self, start: Position) -> Dict[Position, int]:
        """
        Compute the distance of each tile in the map from the start position.
        Map must be fully explored.
        """

        assert start in self.ship_map
        assert self.ship_map[start] in [Tile.TRAVERSABLE, Tile.OXYGEN_STATION]

        queue: List[Position] = [start]
        visited: Set[Position] = set()
        dist = {start: 0}

        while queue:
            node = queue.pop(0)
            visited.add(node)
            for d in Direction:
                neighbor = node + d
                if (
                    neighbor in self.ship_map
                    and neighbor not in visited
                    and self.ship_map[neighbor] != Tile.WALL
                    and self.ship_map[neighbor] != Tile.UNKNOWN
                ):
                    queue.append(neighbor)
                    dist[neighbor] = dist[node] + 1
        return dist

    def explore_entire_map(self):
        # dfs
        def dfs(p: Position):
            for d in Direction:
                next_p = p + d
                if next_p not in self.ship_map:
                    # print(f'at {p}, moving to {d}')
                    self.move_once(d)
                    # did we actually move?
                    if self.pos == next_p:
                        dfs(next_p)
                        self.move_once(d.opposite())

        dfs(self.pos)
