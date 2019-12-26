import problem07.main

if __name__ == "__main__":
    with open("problem07/input", "r") as f:
        my_input = f.readlines()
        my_input = "".join(my_input)

    program = problem07.main.parse_program(my_input)

    # part 1
    max_val, phases = problem07.main.find_max_thruster(program)
    print(max_val)

    # part 2
    max_val, phases = problem07.main.find_max_thruster(program, feedback_mode=True)
    print(max_val)
