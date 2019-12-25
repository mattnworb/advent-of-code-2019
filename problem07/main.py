from itertools import permutations

from .computer import Computer


def find_max_thruster(program):
    possible_phase_settings = permutations([0, 1, 2, 3, 4], 5)

    max_val = 0

    for phase_setting in possible_phase_settings:
        val = run_amplifiers(5, phase_setting, program)
        if val > max_val:
            max_val = val
            max_phase_setting = phase_setting
    return max_val, max_phase_setting


def run_amplifiers(count, phase_settings, opcodes):
    assert count == len(phase_settings)

    output_from_last = 0

    for n in range(count):
        phase = phase_settings[n]
        inputs = [phase, output_from_last]
        c = Computer(opcodes, inputs)
        output = c.run()
        assert len(output) == 1
        output_from_last = output[0]

    return output_from_last


def parse_program(program_string):
    return list(map(int, program_string.split(",")))


if __name__ == "__main__":
    with open("input", "r") as f:
        my_input = f.readlines()

    possible_phase_settings = permutations([0, 1, 2, 3, 4], 5)

    max_val, phases = find_max_thruster(parse_program(my_input))

    print(max_val)
