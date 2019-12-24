from .computer import Computer

def test_problem02():
    cases = [
        # input, expected
        
        # 1,0,0,0,99 becomes 2,0,0,0,99 (1 + 1 = 2).
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),

        # 2,3,0,3,99 becomes 2,3,0,6,99 (3 * 2 = 6).
        ([2,3,0,3,99], [2,3,0,6,99]),

        # 2,4,4,5,99,0 becomes 2,4,4,5,99,9801 (99 * 99 = 9801).
        ([2,4,4,5,99,0], [2,4,4,5,99,9801]),

        # 1,1,1,4,99,5,6,0,99 becomes 30,1,1,4,2,5,6,0,99.
        ([1,1,1,4,99,5,6,0,99], [30,1,1,4,2,5,6,0,99]),
    ]

    for ops, expected in cases:
        assert Computer(ops, input_val=0, outputfn=print, verbose=False).run() == expected