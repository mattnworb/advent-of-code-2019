import computer
import enum


class Direction(enum.Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3

    def rotate_left(self):
        return Direction((self.value + 1) % 4)

    def rotate_right(self):
        return Direction((self.value - 1) % 4)


# outputs from IntCode program
# colors
PAINT_BLACK = 0
PAINT_WHITE = 1
# turns
TURN_LEFT = 0
TURN_RIGHT = 1


class HullPaintingRobot:
    def __init__(self, program):
        self.direction = Direction.UP
        self.panel_colors = {}
        self.painted_panels = set()
        self.current_pos = (0, 0)
        self.computer = computer.Computer(program, inputs=[])

    def run(self):
        result = None
        while result != computer.RunResult.HALTED:
            result = self.run_one_iteration()

    def run_one_iteration(self):
        # check color of current position
        current_panel_color = self.panel_colors.get(self.current_pos, PAINT_BLACK)

        self.computer.add_input(current_panel_color)
        output, result = self.computer.run(until_blocked=True)

        assert len(output) == 2
        color, turn = output

        if result != computer.RunResult.HALTED:
            self.paint_and_move(color, turn)

        return result

    def paint_and_move(self, color, turn):
        assert color == PAINT_BLACK or color == PAINT_WHITE
        assert turn == TURN_LEFT or turn == TURN_RIGHT

        # do the painting
        self.panel_colors[self.current_pos] = color
        self.painted_panels.add(self.current_pos)

        # make the turn
        if turn == TURN_LEFT:
            self.direction = self.direction.rotate_left()
        elif turn == TURN_RIGHT:
            self.direction = self.direction.rotate_right()

        # move forward one
        if self.direction == Direction.UP:
            self.current_pos = (self.current_pos[0], self.current_pos[1] + 1)

        elif self.direction == Direction.DOWN:
            self.current_pos = (self.current_pos[0], self.current_pos[1] - 1)

        elif self.direction == Direction.RIGHT:
            self.current_pos = (self.current_pos[0] + 1, self.current_pos[1])

        elif self.direction == Direction.LEFT:
            self.current_pos = (self.current_pos[0] - 1, self.current_pos[1])
