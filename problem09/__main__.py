import computer

# The BOOST program will ask for a single input; run it in test mode by
# providing it the value 1. It will perform a series of checks on each opcode,
# output any opcodes (and the associated parameter modes) that seem to be
# functioning incorrectly, and finally output a BOOST keycode.
#
# Once your Intcode computer is fully functional, the BOOST program should
# report no malfunctioning opcodes when run in test mode; it should only output
# a single value, the BOOST keycode. What BOOST keycode does it produce?
if __name__ == "__main__":
    with open("problem09/input") as f:
        inp = f.read(-1).strip()

    program = computer.parse_program(inp)

    c = computer.Computer(program, inputs=1)
    outputs, result = c.run()

    assert result == computer.RunResult.HALTED
    print("Part 1:")
    print(outputs)

    # Finally, you can lock on to the Ceres distress signal! You just need to
    # boost your sensors using the BOOST program.
    #
    # The program runs in sensor boost mode by providing the input instruction
    # the value 2. Once run, it will boost the sensors automatically, but it
    # might take a few seconds to complete the operation on slower hardware. In
    # sensor boost mode, the program will output a single value: the coordinates
    # of the distress signal.
    #
    # Run the BOOST program in sensor boost mode. What are the coordinates of the
    # distress signal?
    c = computer.Computer(program, inputs=2)
    outputs, result = c.run()

    assert result == computer.RunResult.HALTED
    print("\nPart 2:")
    print(outputs)
