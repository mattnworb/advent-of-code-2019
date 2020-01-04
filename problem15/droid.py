from collections import Counter
from typing import Dict, Tuple, Optional, Iterator, List, Set, Union
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
        self.ship_map: ShipMap = {}

        # the robot's initial position is traversable by definition
        self.pos = (0, 0)
        self.ship_map[self.pos] = Tile.TRAVERSABLE

        self.oxygen_station_pos = None

    def known_map(self) -> ShipMap:
        """Return a copy of the known map"""
        return dict(self.ship_map)

    def current_pos(self) -> Position:
        return self.pos

    def oxygen_station(self) -> Optional[Position]:
        return self.oxygen_station_pos

    def has_explorable_positions(self) -> bool:
        """Test if there are any positions on the map with unknown regions next to them."""
        # any(self.explorable_positions()) will treat a position like (0, 0) as False
        return any(True for p in self.explorable_positions())

    def explorable_positions(self) -> Iterator[Position]:
        """
        Iterate over UNKNOWN positions on the map that are reachable from the
        robot's current position. In other words, this iterator gives the set of
        positions the robot could move to and learn something new about the map.
        """

        visited: Set[Position] = set()
        frontier: Set[Position] = set([self.pos])

        while frontier:
            current = frontier.pop()
            visited.add(current)
            for d in Direction:
                next_pos = add_to_position(current, d)
                t = self.ship_map.get(next_pos, Tile.UNKNOWN)
                if t == Tile.UNKNOWN:
                    yield next_pos
                elif t == Tile.TRAVERSABLE or t == Tile.OXYGEN_STATION:
                    if next_pos not in visited:
                        frontier.add(next_pos)

    def compute_path(
        self, dest: Position, start_pos: Optional[Position] = None,
    ) -> List[Direction]:
        # can't route to wall
        assert self.ship_map.get(dest) != Tile.WALL, "dest cannot be wall"

        unvisited: Set[Position] = set()
        distances: Dict[Position, Union[int, float]] = {}
        for pos, tile in self.ship_map.items():
            if tile == Tile.TRAVERSABLE or tile == Tile.OXYGEN_STATION:
                unvisited.add(pos)
                for neighbor in self.nonwall_neighbors(pos):
                    unvisited.add(neighbor)

        if not start_pos:
            start_pos = self.pos

        inf = float("inf")
        distances = {pos: inf for pos in unvisited}
        distances[start_pos] = 0

        prev: Dict[Position, Position] = {}

        while unvisited:
            smallest_distance, u = None, None
            for node in unvisited:
                distance = distances[node]
                if smallest_distance is None or distance < smallest_distance:
                    smallest_distance = distance
                    u = node

            if smallest_distance == inf:
                raise ValueError(f"no path to {dest} from {start_pos}")

            assert u is not None
            unvisited.remove(u)

            if u == dest:
                break

            for neighbor in self.nonwall_neighbors(u):
                if (
                    self.ship_map.get(neighbor, Tile.UNKNOWN) == Tile.UNKNOWN
                    and neighbor != dest
                ):
                    # if the neighbor is unknown, only score it if it is the dest
                    continue
                if neighbor in unvisited:
                    tentative = distances[u] + 1
                    if tentative < distances[neighbor]:
                        distances[neighbor] = tentative
                        prev[neighbor] = u

        # print("Dest:", dest)

        # min_pos = min(distances)
        # max_pos = max(distances)

        # print("Distances:")
        # for y in range(min_pos[1], max_pos[1] + 1):
        #     line = ""
        #     for x in range(min_pos[0], max_pos[0] + 1):
        #         p = (x, y)
        #         if p not in distances or distances[p] == inf:
        #             line += "?"
        #         else:
        #             line += str(distances[p])
        #     print(line)

        path: List[Position] = []
        current = dest
        while current in prev and current != start_pos:
            path.insert(0, current)
            current = prev[current]

        directions = []
        current = start_pos
        for node in path:
            # what direction takes us from current to node?
            x1, y1 = current
            x2, y2 = node
            if x1 == x2 and y1 == y2 + 1:
                d = Direction.NORTH
            elif x1 == x2 and y1 == y2 - 1:
                d = Direction.SOUTH
            elif x1 == x2 + 1 and y1 == y2:
                d = Direction.WEST
            elif x1 == x2 - 1 and y1 == y2:
                d = Direction.EAST
            else:
                raise ValueError("oops")
            # print(f'current={current} to {node}: {d}')
            directions.append(d)
            current = node
        return directions

    def nonwall_neighbors(self, node: Position) -> Iterator[Position]:
        """Return the non-WALL neighors of a given node. Will return UNKNOWN neighbors."""
        for d in Direction:
            sibling = add_to_position(node, d)
            if self.ship_map.get(sibling) != Tile.WALL:
                yield sibling

    def count_tiles(self) -> Dict[str, int]:
        return dict(Counter(tile.name for tile in self.ship_map.values()))

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
            self.oxygen_station_pos = intended

        # update the map so it always reflects unknown tiles
        for d in Direction:
            neighbor = add_to_position(self.pos, d)
            if neighbor not in self.ship_map:
                self.ship_map[neighbor] = Tile.UNKNOWN

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
                p = (x, y)
                if p == self.pos:
                    ch = "D"
                elif p == (0, 0):
                    ch = "S"
                else:
                    ch = self.ship_map.get(p, Tile.UNKNOWN).value
                line += ch
            print(line)
