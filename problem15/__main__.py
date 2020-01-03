from .droid import *
from computer import parse_program
import random
import collections
from typing import Counter

import logging

logger = logging.getLogger(__name__)


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

    assert robot.ship_map[dest] != Tile.WALL

    moves = robot.compute_path(dest)
    assert moves, f"No path from {robot.current_pos()} to destination {dest}?"

    logger.info("candidates=%s", candidates)
    logger.info(
        "destination=%s, move=%s, dest is %s", dest, moves[0], robot.ship_map[dest]
    )
    return moves[0]


if __name__ == "__main__":
    with open("problem15/input") as f:
        inp = f.read(-1).strip()

    program = parse_program(inp)
    assert len(program) == 1045, f"program had length {len(program)}"

    robot = RepairDroid(program)

    destinations = []

    rounds = 10000
    for step in range(1, rounds + 1):
        # robot.print_screen()

        # next_move = choose_next_move_manually(robot)
        # next_move = choose_next_move_randomly(robot)
        next_move = choose_next_move_based_on_explorable_positions(robot)

        if not next_move:
            logger.info("no more explorable positions to move to after round %d", step)
            break

        destinations.append(add_to_position(robot.current_pos(), next_move))

        robot.move_once(next_move)
        logger.info(
            "step %d: after move=%s, robot is at %s",
            step,
            next_move,
            robot.current_pos(),
        )

        if robot.oxygen_station():
            print(f"found oxygen station after {step} steps")
            break

        if step % 100 == 0:
            explorable = list(robot.explorable_positions())
            # print(f"Step {step}, tile count: {robot.count_tiles()}, explorable positions: {len(explorable)}")
            print(f"Step {step}, explorable positions: {len(explorable)}")

    print()
    print(f"Map after {rounds} iterations:")
    robot.print_screen()

    o = robot.oxygen_station()
    print()
    print("robot position", robot.current_pos())
    print("Found oxygen station:", o if o else "No")
    print("Has unexplored positions:", robot.has_explorable_positions())
    print("Tile count:", robot.count_tiles())
    # print(len(robot.computer.memory))
    print(
        "Most common destinations:", collections.Counter(destinations).most_common(10)
    )
