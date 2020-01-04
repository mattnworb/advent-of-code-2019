from .droid import *
from computer import parse_program
import random
import collections
from typing import Counter


def choose_next_move_manually(robot: RepairDroid) -> Direction:
    next_move = ""
    while next_move == "":
        next_move = input("Next move: (N, S, W, E): ")
        if next_move not in ["N", "S", "W", "E"]:
            next_move = ""
    return Direction.from_str(next_move)


def choose_next_move_randomly(robot: RepairDroid) -> Direction:
    robot_pos = robot.current_pos()
    known_map = robot.known_map()

    valid_directions = list(Direction)
    random.shuffle(valid_directions)
    for d in valid_directions:
        p = add_to_position(robot_pos, d)
        if p not in known_map or known_map[p] != Tile.WALL:
            return d
    raise ValueError()


def choose_next_move_based_on_explorable_positions(
    robot: RepairDroid,
) -> Optional[Direction]:

    # TODO avoid recalculating this on every choice, instead choose an
    # unexplored position, compute a path, then follow the path until reached.
    candidates = sorted(robot.explorable_positions())
    if not candidates:
        return None
    dest = candidates[0]

    # this algorithm should never try to move us into a wall
    assert robot.ship_map.get(dest) != Tile.WALL

    moves = robot.compute_path(dest)
    assert moves, f"No path from {robot.current_pos()} to destination {dest}?"

    return moves[0]


if __name__ == "__main__":
    with open("problem15/input") as f:
        inp = f.read(-1).strip()

    program = parse_program(inp)
    assert len(program) == 1045, f"program had length {len(program)}"

    print("Part 1")
    robot = RepairDroid(program)

    not_found = False

    rounds = 10000
    for step in range(1, rounds + 1):
        next_move = choose_next_move_based_on_explorable_positions(robot)

        if not next_move:
            print(f"No more positions to explore on map after {step} steps")
            # no more explorable moves?
            break

        robot.move_once(next_move)

        if robot.oxygen_station() and not_found:
            print(f"found oxygen station after {step} steps")
            not_found = True
            # can break here for Part 1, but for Part 2 we want to fully explore the map

        # if step % 100 == 0:
        #     print('Step', step)

    robot.print_screen()

    station = robot.oxygen_station()
    print("Robot position:", robot.current_pos())
    print("Oxygen station:", station if station else "Unknown")
    print("Has unexplored positions:", robot.has_explorable_positions())

    assert station, "Did not find oxygen station"

    path_to_station = robot.compute_path(
        station, start_pos=(0, 0), allow_moves_to_unknown=False
    )
    print(
        f"\nPath to oxygen station from starting position is {len(path_to_station)} moves"
    )

    # verify the path is correct
    new_robot = RepairDroid(program)
    visited_pos: Set[Position] = set()
    for move in path_to_station:
        new_robot.move_once(move)
        assert new_robot.current_pos() not in visited_pos
        visited_pos.add(new_robot.current_pos())
    assert station == new_robot.current_pos()
