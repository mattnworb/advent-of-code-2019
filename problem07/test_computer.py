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
            assert (
                Computer(ops, input_val=0, outputfn=print, verbose=False).run()
                == expected
            )


def is_zero(v):
    assert v == 0, f"expected output of 0 but got {v}"


def is_one(v):
    assert v == 1, f"expected output of 1 but got {v}"


class TestProblem06:
    def test_parse_instruction(self):
        c = Computer([1002, 4, 3, 4], input_val=1, outputfn=print)
        c.parse_instruction(1002)

        assert c.current_op == 2
        assert c.param_modes == [0, 1, 0]

    def test_part2_example1(self):
        opcodes = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]

        # 1 is not 8
        result = Computer(opcodes, input_val=1, outputfn=is_zero, verbose=False).run()

        # 8 is 8
        result = Computer(opcodes, input_val=8, outputfn=is_one, verbose=False).run()
