from computer import parse_program
from problem11 import robot

if __name__ == "__main__":
    with open("problem11/input") as f:
        inp = f.read(-1).strip()

    print("Part 1")
    r = robot.HullPaintingRobot(parse_program(inp))
    r.run()

    print("Number of panels painted:", len(r.painted_panels))

    # Based on the Space Law Space Brochure that the Space Police attached to one of
    # your windows, a valid registration identifier is always eight capital letters.
    # After starting the robot on a single white panel instead, what registration
    # identifier does it paint on your hull?
    print("\nPart 2")
    r = robot.HullPaintingRobot(parse_program(inp), starting_color=robot.PAINT_WHITE)
    r.run()

    print("Number of panels painted:", len(r.painted_panels))
    print("Bounding box:", r.bounding_box())

    black_char = u"\u25A1"
    white_char = u"\u25A0"

    min_x, max_x, min_y, max_y = r.bounding_box()

    painting = ""
    # we walk through y's from positive to negative, but x's in the opposite way
    for y in range(max_y, min_y - 1, -1):
        for x in range(min_x, max_x + 1):
            color = r.panel_colors.get((x, y), robot.PAINT_BLACK)
            if color == robot.PAINT_BLACK:
                painting += black_char
            elif color == robot.PAINT_WHITE:
                painting += white_char
        painting += "\n"
    print(painting)
