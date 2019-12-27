from enum import Enum, unique
import queue


class RunResult(Enum):
    RUNNABLE = 0
    HALTED = 1
    BLOCK_ON_INPUT = 2


@unique
class ParamMode(Enum):
    POSITION = 0
    IMMEDIATE = 1
    RELATIVE = 2


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
            addr = absolute

        elif offset is not None:
            addr = self.pos + offset

        else:
            raise ValueError("Must pass either absolute or offset kwarg")

        self.extend_memory_if_necessary(addr)
        value = self.memory[addr]
        # self.log(f"read: reading address={addr} value={value}")
        return value

    def write(self, value, addr):
        """Writes value to memory at address addr"""
        self.extend_memory_if_necessary(addr)
        # self.log(f"write: writing address={addr} value={value}")
        self.memory[addr] = value

    def read_param(self, param_num):
        """Reads a value from memory based on the given parameter number (one-indexed)."""
        assert param_num > 0

        mode = self.param_modes[param_num - 1]
        param_value = self.read(offset=param_num)
        self.log(
            f"read_param: param_num={param_num} mode={mode} param_value={param_value}"
        )

        if mode == ParamMode.POSITION:
            return self.read(absolute=param_value)

        elif mode == ParamMode.IMMEDIATE:
            return param_value

        elif mode == ParamMode.RELATIVE:
            return self.read(absolute=(self.relative_base + param_value))

        else:
            raise ValueError(f"unknown param mode: {mode}")

    def write_param(self, param_num, value):
        """Write a value to memory based on the given parameter number (one-indexed)."""
        assert param_num > 0

        mode = self.param_modes[param_num - 1]
        param_value = self.read(offset=param_num)
        self.log(
            f"write_param: param_num={param_num} mode={mode} param_value={param_value}"
        )

        if mode == ParamMode.POSITION:
            self.write(value, addr=param_value)

        elif mode == ParamMode.IMMEDIATE:
            # do nothing
            pass

        elif mode == ParamMode.RELATIVE:
            self.write(value, addr=(self.relative_base + param_value))

        else:
            raise ValueError(f"unknown param mode: {mode}")

    def extend_memory_if_necessary(self, pos):
        assert (
            pos < MAX_MEMORY
        ), f"pos={pos} is too high, max memory setting ({MAX_MEMORY})"

        while pos >= len(self.memory):
            self.memory.append(0)

    def add_input(self, val):
        """Add input val to end of input queue"""
        self.input_queue.put(val, block=False)

    # opcode 1
    def add(self):
        a = self.read_param(1)
        b = self.read_param(2)

        self.log(f"adding {a} + {b}")
        self.write_param(3, a + b)

        self.pos += 4

    # opcode 2
    def mult(self):
        a = self.read_param(1)
        b = self.read_param(2)

        self.log(f"mult {a} * {b}")
        self.write_param(3, a * b)

        self.pos += 4

    # opcode 3
    # Opcode 3 takes a single integer as input and saves it to the position
    # given by its only parameter. For example, the instruction 3,50 would
    # take an input value and store it at address 50.
    def read_input(self):
        if self.run_until_block_mode and self.input_queue.empty():
            return True

        next_input = self.input_queue.get(block=False)
        self.log(f"read_input: input is {next_input}")
        self.write_param(1, next_input)

        self.pos += 2
        return False

    # Opcode 4 outputs the value of its only parameter. For example,
    # the instruction 4,50 would output the value at address 50.
    def store_output(self):
        val = self.read_param(1)
        self.log(f"store_output: outputting: {val}")
        self.output.append(val)

        self.pos += 2

    def jump_if_true(self):
        # if the first parameter is non-zero, it sets the instruction pointer
        # to the value from the second parameter. Otherwise, it does nothing.
        p = self.read_param(1)
        self.log(f"jump_if_true: testing if {p} is non-zero")
        if p != 0:
            pos = self.read_param(2)
            self.log(f"jump_if_true: jumping to {pos}")
            self.pos = pos
        else:
            self.pos += 3

    def jump_if_false(self):
        # if the first parameter is zero, it sets the instruction pointer
        # to the value from the second parameter. Otherwise, it does nothing.
        p = self.read_param(1)
        self.log(f"jump_if_false: testing if {p} is zero")
        if p == 0:
            pos = self.read_param(2)
            self.log(f"jump_if_false: jumping to {pos}")
            self.pos = pos
        else:
            self.pos += 3

    def less_than(self):
        # if the first parameter is less than the second parameter, it stores 1
        # in the position given by the third parameter. Otherwise, it stores 0.
        a = self.read_param(1)
        b = self.read_param(2)

        val = 1 if a < b else 0
        self.log(f"less_than: testing if {a} < {b}, result={val}")
        self.write_param(3, val)

        self.pos += 4

    def equal(self):
        # if the first parameter is equal to the second parameter, it stores 1
        # in the position given by the third parameter. Otherwise, it stores 0.
        a = self.read_param(1)
        b = self.read_param(2)

        val = 1 if a == b else 0
        self.log(f"equal: testing if {a} == {b}, result={val}")
        self.write_param(3, val)

        self.pos += 4

    def adjust_relative_base(self):
        adjustment = self.read_param(1)
        self.log(
            f"adjust_relative_base: relative_base={self.relative_base}, offset={adjustment}, new base={self.relative_base + adjustment}"
        )
        self.relative_base += adjustment

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
            mode = ParamMode(inst % a // b)
            param_modes.append(mode)
            a *= 10
            b *= 10

        self.log(
            f"parse_instruction: inst={inst}, storing current_op={opcode} ({OP_NAMES[opcode]}) param_modes={param_modes}"
        )
        self.current_op = opcode
        self.param_modes = param_modes

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
            self.log(f"halt - output: {self.output}")
            return RunResult.HALTED

        else:
            raise ValueError(f"unknown opcode: {self.current_op}")
