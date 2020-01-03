from .droid import *
from computer import parse_program
import random


def choose_next_move_manually(robot_pos: Position, known_map: ShipMap) -> Direction:
    next_move = ""
    while next_move == "":
        next_move = input("Next move: (N, S, W, E): ")
        if next_move not in ["N", "S", "W", "E"]:
            next_move = ""
    return Direction.from_str(next_move)


def choose_next_move_randomly(robot_pos: Position, known_map: ShipMap) -> Direction:
    valid_directions = list(Direction)
    random.shuffle(valid_directions)
    for d in valid_directions:
        p = add_to_position(robot_pos, d)
        if p not in known_map or known_map[p] != Tile.WALL:
            return d
    raise ValueError()


if __name__ == "__main__":
    with open("problem15/input") as f:
        inp = f.read(-1).strip()

    program = parse_program(inp)
    assert len(program) == 1045, f"program had length {len(program)}"

    robot = RepairDroid(program)

    rounds = 100000
    print(f"Making random moves for {rounds} rounds")
    for step in range(rounds):
        # robot.print_screen()

        # next_move = choose_next_move_manually(robot.current_pos(), robot.known_map())
        next_move = choose_next_move_randomly(robot.current_pos(), robot.known_map())

        robot.move_once(next_move)

        # print("\n\n")
    print()
    print(f"Map after {rounds} iterations:")
    robot.print_screen()
    o = robot.oxygen_station()
    print("Found oxygen station:", o if o else "No")
    print("Has unexplored positions:", robot.has_explorable_positions())
    print("Tile count:", robot.count_tiles())
    # print(len(robot.computer.memory))
