NUM_PARAMS = {
    1: 3,  # addition: two operands and the storage location
    2: 3,  # multiplication
    3: 1,  # save_input
    4: 1,  # send_output,
    5: 2,  # jump-if-true
    6: 2,  # jump-if-false
    7: 3,  # less-than
    8: 3,  # equals
    99: 0,  # halt
}


class Computer(object):
    def __init__(self, opcodes, inputs, verbose=True):
        self.opcodes = list(opcodes)  # make a copy
        self.pos = 0

        if isinstance(inputs, int):
            self.input_iterator = iter([inputs])
        else:
            self.input_iterator = iter(inputs)

        self.current_op = None
        self.param_modes = []

        self.verbose = verbose

    def log(self, msg):
        if self.verbose:
            print(msg)

    # opcode 1
    def add(self):
        param1 = self.opcodes[self.pos + 1]
        param2 = self.opcodes[self.pos + 2]
        param3 = self.opcodes[self.pos + 3]

        a = self.read_value(0, param1)
        b = self.read_value(1, param2)

        if self.param_modes[2] == 0:
            self.opcodes[param3] = a + b
        # immediate mode, nothing to store

        self.pos += 4

    # opcode 2
    def mult(self):
        param1 = self.opcodes[self.pos + 1]
        param2 = self.opcodes[self.pos + 2]
        param3 = self.opcodes[self.pos + 3]

        a = self.read_value(0, param1)
        b = self.read_value(1, param2)

        if self.param_modes[2] == 0:
            self.opcodes[param3] = a * b

        self.pos += 4

    # opcode 3
    # Opcode 3 takes a single integer as input and saves it to the position
    # given by its only parameter. For example, the instruction 3,50 would
    # take an input value and store it at address 50.
    def save_input(self):
        dst = self.opcodes[self.pos + 1]

        if self.param_modes[0] == 0:
            next_input = self.input_iterator.__next__()
            self.log(f"save_input: storing {next_input} in address {dst}")
            self.opcodes[dst] = next_input

        self.pos += 2

    # Opcode 4 outputs the value of its only parameter. For example,
    # the instruction 4,50 would output the value at address 50.
    def send_output(self):
        val = self.read_value(0, self.opcodes[self.pos + 1])
        self.log(f"send_output: adding {val} to output")
        self.output.append(val)

        self.pos += 2

    def jump_if_true(self):
        # if the first parameter is non-zero, it sets the instruction pointer
        # to the value from the second parameter. Otherwise, it does nothing.
        if self.read_value(0, self.opcodes[self.pos + 1]) != 0:
            self.pos = self.read_value(1, self.opcodes[self.pos + 2])
        else:
            self.pos += 3

    def jump_if_false(self):
        # if the first parameter is zero, it sets the instruction pointer
        # to the value from the second parameter. Otherwise, it does nothing.
        p = self.read_value(0, self.opcodes[self.pos + 1])
        self.log(f"jump_if_false: testing if {p} == 0")
        if p == 0:
            new_ip = self.read_value(1, self.opcodes[self.pos + 2])
            self.log(f"jump_if_false: updating instruction pointer to {new_ip}")
            self.pos = new_ip
        else:
            self.pos += 3

    def less_than(self):
        # if the first parameter is less than the second parameter, it stores 1
        # in the position given by the third parameter. Otherwise, it stores 0.
        a = self.read_value(0, self.opcodes[self.pos + 1])
        b = self.read_value(1, self.opcodes[self.pos + 2])

        if self.param_modes[2] == 0:
            dst = self.opcodes[self.pos + 3]
            self.log(f"less_than: testing if {a} < {b}, storing answer in {dst}")
            if a < b:
                self.opcodes[dst] = 1
            else:
                self.opcodes[dst] = 0

        self.pos += 4

    def equal(self):
        # if the first parameter is equal to the second parameter, it stores 1
        # in the position given by the third parameter. Otherwise, it stores 0.
        a = self.read_value(0, self.opcodes[self.pos + 1])
        b = self.read_value(1, self.opcodes[self.pos + 2])

        if self.param_modes[2] == 0:
            dst = self.opcodes[self.pos + 3]

            self.log(f"equal: testing if {a} == {b}, storing output in address {dst}")

            if a == b:
                self.opcodes[dst] = 1
            else:
                self.opcodes[dst] = 0

        self.pos += 4

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
            f"parse_instruction: inst={inst}, storing current_op={opcode} param_modes={param_modes}"
        )
        self.current_op = opcode
        self.param_modes = param_modes

    def read_value(self, param_num, val):
        """
        Right now, your ship computer already understands parameter mode 0, position mode, 
        which causes the parameter to be interpreted as a position - if the parameter is 
        50, its value is the value stored at address 50 in memory. Until now, all 
        parameters have been in position mode.

        Now, your ship computer will also need to handle parameters in mode 1, 
        immediate mode. In immediate mode, a parameter is interpreted as a value 
        - if the parameter is 50, its value is simply 50.
        """
        mode = self.param_modes[param_num]
        if mode == 0:
            self.log(f"read_value: param_num={param_num} param={val} = position mode")
            return self.opcodes[val]
        elif mode == 1:
            self.log(f"read_value: param_num={param_num} param={val} = immediate mode")
            return val

        raise ValueError(f"unknown param mode: {mode}")

    def run(self):
        """
        Runs the program. Returns the output. To check the program after running, look at .opcodes.
        """
        self.log(f"starting program: {self.opcodes}")

        self.output = []

        while self.pos < len(self.opcodes):
            self.log(f"\nrun: at position={self.pos} opcodes={self.opcodes}")

            self.parse_instruction(self.opcodes[self.pos])

            if self.current_op == 1:
                self.add()

            elif self.current_op == 2:
                self.mult()

            elif self.current_op == 3:
                self.save_input()

            elif self.current_op == 4:
                self.send_output()

            elif self.current_op == 5:
                self.jump_if_true()

            elif self.current_op == 6:
                self.jump_if_false()

            elif self.current_op == 7:
                self.less_than()

            elif self.current_op == 8:
                self.equal()

            elif self.current_op == 99:
                self.log(f"halt, returning: {self.opcodes}")
                return self.output
                # break

            else:
                raise ValueError(f"unknown opcode: {self.current_op}")
