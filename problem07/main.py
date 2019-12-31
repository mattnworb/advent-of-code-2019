from itertools import permutations

from computer import Computer


def find_max_thruster(program, feedback_mode=False):
    if feedback_mode:
        possible_phase_settings = permutations([5, 6, 7, 8, 9], 5)
    else:
        possible_phase_settings = permutations([0, 1, 2, 3, 4], 5)

    max_val = 0
    max_phase_setting = None

    for phase_setting in possible_phase_settings:
        val = run_amplifiers(5, phase_setting, program, feedback_mode)
        if val > max_val:
            max_val = val
            max_phase_setting = phase_setting

    return max_val, max_phase_setting


def run_amplifiers(count, phase_settings, opcodes, feedback_mode=False):
    assert count == len(phase_settings)

    if feedback_mode == True:
        # setup each computer
        computers = []
        for n in range(count):
            phase = phase_settings[n]
            inputs = [phase]
            if n == 0:
                inputs.append(0)
            c = Computer(opcodes, inputs)
            computers.append(c)

        # then run them
        while True:
            for ix, c in enumerate(computers):
                outputs, result = c.run(until_blocked=True)
                # pass output to next computer
                next_computer = (
                    computers[ix + 1] if ix != len(computers) - 1 else computers[0]
                )
                for output in outputs:
                    next_computer.add_input(output)
                last_output = outputs

            if all((c.halted for c in computers)):
                last_output = computers[-1].output
                assert len(last_output) == 1
                return last_output[0]
    else:
        output_from_last = 0

        for n in range(count):
            phase = phase_settings[n]
            inputs = [phase, output_from_last]
            c = Computer(opcodes, inputs)
            output, result = c.run()
            assert (
                len(output) == 1
            ), f"Expected output length of 1 but got {len(output)}"
            output_from_last = output[0]

        return output_from_last
