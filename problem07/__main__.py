from .main import find_max_thruster
from computer import parse_program

if __name__ == "__main__":
    with open("problem07/input", "r") as f:
        my_input = f.readlines()
        my_input = "".join(my_input)

    program = parse_program(my_input)

    # part 1
    print("Part 1")
    max_val, phases = find_max_thruster(program)
    print(max_val)

    # part 2
    print("\nPart 2")
    max_val, phases = find_max_thruster(program, feedback_mode=True)
    print(max_val)
