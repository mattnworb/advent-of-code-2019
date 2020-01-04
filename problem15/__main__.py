from .droid import *
from computer import parse_program
import random
import collections
from typing import Counter

if __name__ == "__main__":
    with open("problem15/input") as f:
        inp = f.read(-1).strip()

    program = parse_program(inp)
    assert len(program) == 1045, f"program had length {len(program)}"

    print("Part 1")
    robot = RepairDroid(program)
    robot.explore_entire_map()
    station = robot.oxygen_station()
    assert station is not None

    robot.print_screen()
    print(f"Robot moves attempted={robot.moves_attempted}, made={robot.moves_made}")

    dist = robot.bfs_score(Position(0, 0))
    print(f"Distance from (0,0) to oxygen station at {station}: {dist[station]}")

    print("\nPart 2")
    dist = robot.bfs_score(station)
    # what is furthest from oxygen station?
    print(f"Furthest spot from oxygen station: {max(dist.values())}")
