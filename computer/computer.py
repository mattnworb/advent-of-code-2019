import queue

from enum import Enum


class RunResult(Enum):
    RUNNABLE = 0
    HALTED = 1
    BLOCK_ON_INPUT = 2


MAX_MEMORY = 2000

NUM_PARAMS = {
    1: 3,  # addition: two operands and the storage location
    2: 3,  # multiplication
    3: 1,  # read_input
    4: 1,  # store_output,
    5: 2,  # jump-if-true
    6: 2,  # jump-if-false
    7: 3,  # less-than
    8: 3,  # equals
    9: 1,  # adject relative base
    99: 0,  # halt
}

OP_NAMES = {
    1: "ADD",
    2: "MULT",
    3: "READ_INPUT",
    4: "WRITE_OUTPUT",
    5: "JUMP_IF_TRUE",
    6: "JUMP_IF_FALSE",
    7: "LESS_THAN",
    8: "EQUALS",
    9: "ADJUST_RELATIVE_BASE",
    99: "HALT",
}


def parse_program(program_string):
    return list(map(int, program_string.split(",")))


class Computer(object):
    def __init__(self, opcodes, inputs, verbose=False):
        self.memory = list(opcodes)  # make a copy
        self.original_opcodes = list(opcodes)
        self.pos = 0

        self.input_queue = queue.Queue()
        if isinstance(inputs, int):
            self.add_input(inputs)
        else:
            for i in inputs:
                self.add_input(i)

        self.current_op = None
        self.param_modes = []
        self.relative_base = 0
        self.run_until_block_mode = False
        self.halted = False

        self.verbose = verbose

    def log(self, msg):
        if self.verbose:
            print(msg)

    def read(self, absolute=None, offset=None):
        """Reads one value from memory"""

        if absolute is not None:
            p = absolute

        elif offset is not None:
            p = self.pos + offset

        else:
            raise ValueError("Must pass either absolute or offset kwarg")

        self.extend_memory_if_necessary(p)
        return self.memory[p]

    def write(self, val, absolute=None, offset=None):
        """Writes one value to memory"""

        if absolute is not None:
            p = absolute

        elif offset is not None:
            p = self.pos + offset

        else:
            raise ValueError("Must pass either absolute or offset kwarg")

        self.extend_memory_if_necessary(p)
        self.memory[p] = val

    def extend_memory_if_necessary(self, pos):
        assert (
            pos < MAX_MEMORY
        ), f"pos={pos} is too high for max memory setting ({MAX_MEMORY})"

        while pos >= len(self.memory):
            self.memory.append(0)

    def add_input(self, val):
        """Add input val to end of input queue"""
        self.input_queue.put(val, block=False)

    # opcode 1
    def add(self):
        param1 = self.read(offset=1)
        param2 = self.read(offset=2)
        param3 = self.read(offset=3)

        a = self.read_value(0, param1)
        b = self.read_value(1, param2)

        if self.param_modes[2] == 0:
            self.write(a + b, absolute=param3)
            self.log(f"add {a} + {b}, storing result in pos {param3}")

        self.pos += 4

    # opcode 2
    def mult(self):
        param1 = self.read(offset=1)
        param2 = self.read(offset=2)
        param3 = self.read(offset=3)

        a = self.read_value(0, param1)
        b = self.read_value(1, param2)

        if self.param_modes[2] == 0:
            self.write(a * b, absolute=param3)
            self.log(f"mult {a} * {b}, storing result in pos {param3}")

        self.pos += 4

    # opcode 3
    # Opcode 3 takes a single integer as input and saves it to the position
    # given by its only parameter. For example, the instruction 3,50 would
    # take an input value and store it at address 50.
    def read_input(self):
        dst = self.read(offset=1)

        if self.param_modes[0] == 0:
            if self.run_until_block_mode and self.input_queue.empty():
                return True
            else:
                next_input = self.input_queue.get(block=False)
            self.log(f"read_input: storing {next_input} in address {dst}")
            self.write(next_input, absolute=dst)

        self.pos += 2
        return False

    # Opcode 4 outputs the value of its only parameter. For example,
    # the instruction 4,50 would output the value at address 50.
    def store_output(self):
        val = self.read_value(0, self.read(offset=1))
        self.log(f"store_output: adding {val} to output")
        self.output.append(val)

        self.pos += 2

    def jump_if_true(self):
        # if the first parameter is non-zero, it sets the instruction pointer
        # to the value from the second parameter. Otherwise, it does nothing.
        p = self.read_value(0, self.read(offset=1))
        self.log(f"jump_if_true: testing if {p} != 0")
        if p != 0:
            pos = self.read_value(1, self.read(offset=2))
            self.log(f"jump_if_true: jumping to {pos}")
            self.pos = pos
        else:
            self.pos += 3

    def jump_if_false(self):
        # if the first parameter is zero, it sets the instruction pointer
        # to the value from the second parameter. Otherwise, it does nothing.
        p = self.read_value(0, self.read(offset=1))
        self.log(f"jump_if_false: testing if {p} == 0")
        if p == 0:
            pos = self.read_value(1, self.read(offset=2))
            self.log(f"jump_if_false: jumping to {pos}")
            self.pos = pos
        else:
            self.pos += 3

    def less_than(self):
        # if the first parameter is less than the second parameter, it stores 1
        # in the position given by the third parameter. Otherwise, it stores 0.
        a = self.read_value(0, self.read(offset=1))
        b = self.read_value(1, self.read(offset=2))

        if self.param_modes[2] == 0:
            dst = self.read(offset=3)
            self.log(f"less_than: testing if {a} < {b}, storing answer in {dst}")
            if a < b:
                self.write(1, absolute=dst)
            else:
                self.write(0, absolute=dst)

        self.pos += 4

    def equal(self):
        # if the first parameter is equal to the second parameter, it stores 1
        # in the position given by the third parameter. Otherwise, it stores 0.
        a = self.read_value(0, self.read(offset=1))
        b = self.read_value(1, self.read(offset=2))

        if self.param_modes[2] == 0:
            dst = self.read(offset=3)

            self.log(f"equal: testing if {a} == {b}, storing output in address {dst}")

            if a == b:
                self.write(1, absolute=dst)
            else:
                self.write(0, absolute=dst)

        self.pos += 4

    def adjust_relative_base(self):
        param = self.read_value(0, self.read(offset=1))
        self.relative_base += param
        self.log(f"adjust_relative_base: new base is {self.relative_base}")

        self.pos += 2

    def parse_instruction(self, inst):
        """
        Parameter modes are stored in the same value as the instruction's opcode.
        
        The opcode is a two-digit number based only on the ones and tens digit of 
        the value, that is, the opcode is the rightmost two digits of the first 
        value in an instruction. 
        
        Parameter modes are single digits, one per parameter, read right-to-left 
        from the opcode: the first parameter's mode is in the hundreds digit, 
        the second parameter's mode is in the thousands digit, the third parameter's 
        mode is in the ten-thousands digit, and so on. Any missing modes are 0.
        """
        # right two most digits
        opcode = inst % 100
        param_count = NUM_PARAMS[opcode]
        param_modes = []
        # start with hundreds digit
        a, b = 1000, 100
        for c in range(param_count):
            param_modes.append(inst % a // b)
            a *= 10
            b *= 10

        self.log(
            f"parse_instruction: inst={inst}, storing current_op={opcode} ({OP_NAMES[opcode]}) param_modes={param_modes}"
        )
        self.current_op = opcode
        self.param_modes = param_modes

    def read_value(self, param_num, val):
        """
        Right now, your ship computer already understands parameter mode 0,
        position mode, which causes the parameter to be interpreted as a
        position - if the parameter is 50, its value is the value stored at
        address 50 in memory. Until now, all parameters have been in position
        mode.

        Now, your ship computer will also need to handle parameters in mode 1,
        immediate mode. In immediate mode, a parameter is interpreted as a
        value: if the parameter is 50, its value is simply 50.

        Parameters in mode 2, relative mode, behave very similarly to parameters
        in position mode: the parameter is interpreted as a position. Like
        position mode, parameters in relative mode can be read from or written
        to.

        The important difference is that relative mode parameters don't count
        from address 0. Instead, they count from a value called the relative
        base. The relative base starts at 0.
        """
        mode = self.param_modes[param_num]

        if mode == 0:
            self.log(f"read_value: param_num={param_num} param={val} = position mode")
            return self.read(absolute=val)

        elif mode == 1:
            self.log(f"read_value: param_num={param_num} param={val} = immediate mode")
            return val

        elif mode == 2:
            self.log(
                f"read_value: param_num={param_num} param={val} relative_base={self.relative_base} = relative mode"
            )
            dst = self.relative_base + val
            return self.read(absolute=dst)

        raise ValueError(f"unknown param mode: {mode}")

    def run(self, until_blocked=False):
        """
        Runs the program until halted, or if until_blocked is True, stops when blocked on input. Returns the output. 
        To check the program after running, look at .opcodes.
        """

        if self.halted:
            raise ValueError("Cannot run halted computer")

        self.run_until_block_mode = until_blocked

        self.log(f"starting program: {self.memory}")

        self.output = []

        while self.pos < len(self.memory):
            result = self.run_one_iteration()
            if result == RunResult.HALTED:
                self.halted = True
                return self.output, result
            elif result == RunResult.BLOCK_ON_INPUT and until_blocked == True:
                return self.output, result

    def run_one_iteration(self) -> RunResult:
        """Runs one instruction of the program."""
        self.log(f"\nrun: at position={self.pos} opcodes={self.memory}")

        self.parse_instruction(self.read(offset=0))

        if self.current_op == 1:
            self.add()
            return RunResult.RUNNABLE

        elif self.current_op == 2:
            self.mult()
            return RunResult.RUNNABLE

        elif self.current_op == 3:
            blocked = self.read_input()
            if blocked:
                return RunResult.BLOCK_ON_INPUT
            return RunResult.RUNNABLE

        elif self.current_op == 4:
            self.store_output()
            return RunResult.RUNNABLE

        elif self.current_op == 5:
            self.jump_if_true()
            return RunResult.RUNNABLE

        elif self.current_op == 6:
            self.jump_if_false()
            return RunResult.RUNNABLE

        elif self.current_op == 7:
            self.less_than()
            return RunResult.RUNNABLE

        elif self.current_op == 8:
            self.equal()
            return RunResult.RUNNABLE

        elif self.current_op == 9:
            self.adjust_relative_base()
            return RunResult.RUNNABLE

        elif self.current_op == 99:
            self.log(f"halt")
            return RunResult.HALTED

        else:
            raise ValueError(f"unknown opcode: {self.current_op}")