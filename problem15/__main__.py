from .droid import RepairDroid, Direction
from computer import parse_program

if __name__ == "__main__":
    with open("problem15/input") as f:
        inp = f.read(-1).strip()

    program = parse_program(inp)
    assert len(program) == 1045, f"program had length {len(program)}"

    robot = RepairDroid(program)

    while True:
        robot.print_screen()

        next_input = ""
        while next_input == "":
            next_input = input("Next move: (N, S, W, E): ")
            if next_input not in ["N", "S", "W", "E"]:
                next_input = ""

        robot.move_once(Direction.from_str(next_input))

        print("\n\n")
