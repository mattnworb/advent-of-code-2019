from .computer import Computer, ParamMode, RunResult, parse_program


def test_parse_instruction():
    c = Computer([1002, 4, 3, 4], inputs=1)
    c.parse_instruction(203)
    assert c.current_op == 3
    assert c.param_modes == [ParamMode.RELATIVE]


class TestProblem02:
    def test_problem02(self):
        cases = [
            # input, expected
            # 1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
            ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
            # 2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
            ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
            # 2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
            ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
            # 1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.
            ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
        ]

        for ops, expected in cases:
            c = Computer(ops, inputs=0, verbose=True)
            c.run()
            assert c.memory == expected


class TestProblem06:
    def test_parse_instruction(self):
        c = Computer([1002, 4, 3, 4], inputs=1)
        c.parse_instruction(1002)

        assert c.current_op == 2
        assert c.param_modes == [
            ParamMode.POSITION,
            ParamMode.IMMEDIATE,
            ParamMode.POSITION,
        ]

    def test_part2_example1(self):
        opcodes = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]

        # 1 is not 8
        assert [0], RunResult.HALTED == Computer(opcodes, inputs=1).run()

        # 8 is 8
        assert [1], RunResult.HALTED == Computer(opcodes, inputs=8).run()

    def test_part2_example2(self):
        opcodes = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]

        # is input less than 8?
        # 1 is less than 8
        assert [1], RunResult.HALTED == Computer(opcodes, inputs=1).run()

        # 8 and 9 are not less than 8
        assert [0], RunResult.HALTED == Computer(opcodes, inputs=8).run()
        assert [0], RunResult.HALTED == Computer(opcodes, inputs=9).run()

    def test_part2_example3(self):
        opcodes = [3, 3, 1108, -1, 8, 3, 4, 3, 99]

        # is input equal to 8?
        assert [0], RunResult.HALTED == Computer(opcodes, inputs=1).run()
        assert [0], RunResult.HALTED == Computer(opcodes, inputs=9).run()
        assert [1], RunResult.HALTED == Computer(opcodes, inputs=8).run()

    def test_part2_example4(self):
        opcodes = [3, 3, 1107, -1, 8, 3, 4, 3, 99]

        assert [1], RunResult.HALTED == Computer(opcodes, inputs=1).run()
        assert [0], RunResult.HALTED == Computer(opcodes, inputs=9).run()
        assert [0], RunResult.HALTED == Computer(opcodes, inputs=8).run()

    def test_part2_example5(self):
        opcodes = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]

        assert [0], RunResult.HALTED == Computer(opcodes, inputs=0).run()
        assert [1], RunResult.HALTED == Computer(opcodes, inputs=1).run()

    def test_part2_example6(self):
        opcodes = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]

        assert [0], RunResult.HALTED == Computer(opcodes, inputs=0).run()
        assert [1], RunResult.HALTED == Computer(opcodes, inputs=1).run()

    def test_part2_example7(self):
        opcodes = parse_program(
            "3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99"
        )

        # output 999 if the input value is below 8
        assert [999], RunResult.HALTED == Computer(opcodes, inputs=0).run()

        # output 1000 if the input value is equal to 8
        assert [1000], RunResult.HALTED == Computer(opcodes, inputs=8).run()

        # output 1001 if the input value is greater than 8.
        assert [1001], RunResult.HALTED == Computer(opcodes, inputs=10).run()


class TestProblem09:
    def test_part1_example1(self):
        """
        109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99 takes no input and produces a copy of itself as output.
        """
        program = parse_program(
            "109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99"
        )

        outputs, result = Computer(program, inputs=[], verbose=True).run()
        assert program == outputs

    def test_part1_example2(self):
        """1102,34915192,34915192,7,4,7,99,0 should output a 16-digit number."""
        program = parse_program("1102,34915192,34915192,7,4,7,99,0")

        outputs, result = Computer(program, inputs=[], verbose=True).run()
        assert len(str(outputs[0])) == 16

    def test_part1_example3(self):
        """104,1125899906842624,99 should output the large number in the middle."""
        program = parse_program("104,1125899906842624,99")
        outputs, result = Computer(program, inputs=[], verbose=True).run()
        assert outputs == [1125899906842624]

    def test_read_input_relative_param(self):
        """
        My first pass at part 01 failed with an output of [203, 0], suggesting
        that the handling of the READ_INPUT op in relative param mode is buggy.
        """
        program = parse_program(
            # adjust relative base to 0 + 5
            "109,5,"
            # read input, store at relative addr 4 (plus base above = 9)
            + "203,4,"
            # mult addr 9 times 2, store result back in addr 9
            + "1002,9,2,9,"
            # output relative address 4 (plus base above = 9)
            + "204,4,"
            # halt
            + "99"
        )
        outputs, result = Computer(program, inputs=[2], verbose=True).run()
        # 2 * 2 = 4
        assert outputs == [4]
