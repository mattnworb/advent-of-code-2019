from computer import parse_program
from problem11 import robot

if __name__ == "__main__":
    with open("problem11/input") as f:
        inp = f.read(-1).strip()

    print("Part 1")
    r = robot.HullPaintingRobot(parse_program(inp))
    r.run()

    print(len(r.painted_panels))
