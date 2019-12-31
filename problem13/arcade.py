from collections import defaultdict
from typing import Dict

from computer import Computer, RunResult

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

    def play_once(self):
        self.reset_screen()

        self.computer = Computer(self.program, max_memory_length=10000)

        outputs, result = self.computer.run()
        assert result == RunResult.HALTED
        assert len(outputs) % 3 == 0

        self.update_screen(outputs)

    def play_continously(self):
        self.reset_screen()

        p = list(self.program)
        p[0] = 2
        self.computer = Computer(p, max_memory_length=10000)

        result = None
        while result != RunResult.HALTED:
            outputs, result = self.computer.run(until_blocked=True)
            self.update_screen(outputs)
            self.print_screen()
            # print(result)
            score = self.screen[-1][0]
            if result == RunResult.BLOCK_ON_INPUT:
                x = input(f"Score is {score}. Press enter to continue")
                self.computer.add_input(0)
            elif result == RunResult.HALTED:
                print(f"Score is {score}. Game over")

    def count_blocks(self):
        count = 0
        for x in self.screen:
            for y in self.screen[x]:
                if self.screen[x][y] == TILE_BLOCK:
                    count += 1
        return count

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
