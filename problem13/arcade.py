from collections import defaultdict
from typing import Dict

from computer import Computer, RunResult

from enum import Enum
import time


class Direction(Enum):
    LEFT = -1
    NEUTRAL = 0
    RIGHT = 1


TILE_EMPTY = 0
TILE_WALL = 1
TILE_BLOCK = 2
TILE_PADDLE = 3
TILE_BALL = 4

chars = {
    TILE_EMPTY: " ",
    TILE_WALL: "\u2588",
    TILE_BLOCK: "\u25A1",
    TILE_PADDLE: "_",
    TILE_BALL: "\u25CF",
}


class Arcade:
    def __init__(self, program):
        self.program = program
        self.reset_screen()

    def reset_screen(self):
        self.screen: Dict[int, Dict[int, int]] = defaultdict(lambda: defaultdict(int))

    def update_screen(self, outputs):
        for n in range(0, len(outputs), 3):
            x, y, tile = outputs[n], outputs[n + 1], outputs[n + 2]
            self.screen[x][y] = tile

    def find_tile(self, value):
        for x in self.screen:
            for y in self.screen[x]:
                if self.screen[x][y] == value:
                    return x, y
        return None

    def count_blocks(self):
        count = 0
        for x in self.screen:
            for y in self.screen[x]:
                if self.screen[x][y] == TILE_BLOCK:
                    count += 1
        return count

    def play_once(self):
        self.reset_screen()

        self.computer = Computer(self.program, max_memory_length=10000)

        outputs, result = self.computer.run()
        assert result == RunResult.HALTED
        assert len(outputs) % 3 == 0

        self.update_screen(outputs)

    def play_continously(self, print_board=False, sleep=None):
        """
        Plays the arcade until the computer is halted (when all blocks are
        busted). Determines the optimal move for the paddle based on relation to
        ball position.

        Set print_board to True to print the board on each iteration. Set sleep
        to a number to sleep for that many seconds between rounds (use a small
        value like 0.2).
        """
        self.reset_screen()

        p = list(self.program)
        p[0] = 2
        self.computer = Computer(p, max_memory_length=10000)

        result = None
        while result != RunResult.HALTED:
            outputs, result = self.computer.run(until_blocked=True)
            self.update_screen(outputs)
            if print_board:
                self.print_screen()

            score = self.screen[-1][0]
            if result == RunResult.BLOCK_ON_INPUT:
                # x = input(f"Score is {score}. Enter to continue")
                if print_board:
                    print(f"Score is {score}")
                if sleep:
                    time.sleep(sleep)
                move = self.determine_paddle_move()
                self.computer.add_input(move.value)
            elif result == RunResult.HALTED:
                print(f"Score is {score}. Game over")

    def determine_paddle_move(self):
        ball = self.find_tile(TILE_BALL)
        paddle = self.find_tile(TILE_PADDLE)

        if ball[0] > paddle[0]:
            return Direction.RIGHT
        elif ball[0] < paddle[0]:
            return Direction.LEFT
        else:
            return Direction.NEUTRAL

    def print_screen(self, max_y=26, stream=None):
        if stream is None:
            from sys import stdout

            stream = stdout

        max_x = max(self.screen.keys())
        if not max_y:
            max_y = max(max(self.screen[r]) for r in self.screen)

        for y in range(max_y + 1):
            line = ""
            for x in range(max_x + 1):
                tile = self.screen[x][y]
                line += chars[tile]
            print(line, file=stream)
