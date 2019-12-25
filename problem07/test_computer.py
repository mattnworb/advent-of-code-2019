from .computer import Computer


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
            c = Computer(ops, inputs=0, verbose=False)
            c.run()
            assert c.opcodes == expected


def is_zero(v):
    assert v == 0, f"expected output of 0 but got {v}"


def is_one(v):
    assert v == 1, f"expected output of 1 but got {v}"


def expect_output(n):
    def a(v):
        assert v == n, f"expected output of {n} but got {v}"

    return a


class TestProblem06:
    def test_parse_instruction(self):
        c = Computer([1002, 4, 3, 4], inputs=1)
        c.parse_instruction(1002)

        assert c.current_op == 2
        assert c.param_modes == [0, 1, 0]

    def test_part2_example1(self):
        opcodes = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]

        # 1 is not 8
        assert [0] == Computer(opcodes, inputs=1, verbose=False).run()

        # 8 is 8
        assert [1] == Computer(opcodes, inputs=8, verbose=False).run()

    def test_part2_example2(self):
        opcodes = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]

        # is input less than 8?
        # 1 is less than 8
        assert [1] == Computer(opcodes, inputs=1, verbose=False).run()

        # 8 and 9 are not less than 8
        assert [0] == Computer(opcodes, inputs=8, verbose=False).run()
        assert [0] == Computer(opcodes, inputs=9, verbose=False).run()

    def test_part2_example3(self):
        opcodes = [3, 3, 1108, -1, 8, 3, 4, 3, 99]

        # is input equal to 8?
        assert [0] == Computer(opcodes, inputs=1, verbose=False).run()
        assert [0] == Computer(opcodes, inputs=9, verbose=False).run()
        assert [1] == Computer(opcodes, inputs=8, verbose=False).run()

    def test_part2_example4(self):
        opcodes = [3, 3, 1107, -1, 8, 3, 4, 3, 99]

        assert [1] == Computer(opcodes, inputs=1, verbose=False).run()
        assert [0] == Computer(opcodes, inputs=9, verbose=False).run()
        assert [0] == Computer(opcodes, inputs=8, verbose=False).run()

    def test_part2_example5(self):
        opcodes = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]

        assert [0] == Computer(opcodes, inputs=0, verbose=False).run()
        assert [1] == Computer(opcodes, inputs=1, verbose=False).run()

    def test_part2_example6(self):
        opcodes = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]

        assert [0] == Computer(opcodes, inputs=0, verbose=False).run()
        assert [1] == Computer(opcodes, inputs=1, verbose=False).run()

    def test_part2_example7(self):
        opcodes = [
            3,
            21,
            1008,
            21,
            8,
            20,
            1005,
            20,
            22,
            107,
            8,
            21,
            20,
            1006,
            20,
            31,
            1106,
            0,
            36,
            98,
            0,
            0,
            1002,
            21,
            125,
            20,
            4,
            20,
            1105,
            1,
            46,
            104,
            999,
            1105,
            1,
            46,
            1101,
            1000,
            1,
            20,
            4,
            20,
            1105,
            1,
            46,
            98,
            99,
        ]

        # output 999 if the input value is below 8
        assert [999] == Computer(opcodes, inputs=0, verbose=False).run()

        # output 1000 if the input value is equal to 8
        assert [1000] == Computer(opcodes, inputs=8, verbose=False).run()

        # output 1001 if the input value is greater than 8.
        assert [1001] == Computer(opcodes, inputs=10, verbose=False).run()
