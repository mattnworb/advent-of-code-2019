from .robot import (
    Direction,
    HullPaintingRobot,
    PAINT_BLACK,
    PAINT_WHITE,
    TURN_LEFT,
    TURN_RIGHT,
)


class TestDirection:
    def test_rotate_left(self):
        assert Direction.UP.rotate_left() == Direction.LEFT
        assert Direction.LEFT.rotate_left() == Direction.DOWN
        assert Direction.DOWN.rotate_left() == Direction.RIGHT
        assert Direction.RIGHT.rotate_left() == Direction.UP

    def test_rotate_right(self):
        assert Direction.UP.rotate_right() == Direction.RIGHT
        assert Direction.LEFT.rotate_right() == Direction.UP
        assert Direction.DOWN.rotate_right() == Direction.LEFT
        assert Direction.RIGHT.rotate_right() == Direction.DOWN


class TestRobot:
    def test_paint_and_move(self):
        # For example, suppose the robot is about to start running. Drawing
        # black panels as ., white panels as #, and the robot pointing the
        # direction it is facing (< ^ > v), the initial state and region near
        # the robot looks like this:
        #
        # .....
        # .....
        # ..^..
        # .....
        # .....
        robot = HullPaintingRobot(program=[])

        # six moves from example
        robot.paint_and_move(PAINT_WHITE, TURN_LEFT)
        assert robot.direction == Direction.LEFT
        assert robot.current_pos == (-1, 0)

        robot.paint_and_move(PAINT_BLACK, TURN_LEFT)
        assert robot.direction == Direction.DOWN
        assert robot.current_pos == (-1, -1)

        robot.paint_and_move(PAINT_WHITE, TURN_LEFT)
        assert robot.direction == Direction.RIGHT
        assert robot.current_pos == (0, -1)

        robot.paint_and_move(PAINT_WHITE, TURN_LEFT)
        assert robot.direction == Direction.UP
        assert robot.current_pos == (0, 0)

        robot.paint_and_move(PAINT_BLACK, TURN_RIGHT)
        assert robot.direction == Direction.RIGHT
        assert robot.current_pos == (1, 0)

        robot.paint_and_move(PAINT_WHITE, TURN_LEFT)
        assert robot.direction == Direction.UP
        assert robot.current_pos == (1, 1)

        robot.paint_and_move(PAINT_WHITE, TURN_LEFT)
        assert robot.direction == Direction.LEFT
        assert robot.current_pos == (0, 1)

        assert len(robot.painted_panels) == 6
