import computer
import collections
from typing import Dict

from problem13 import arcade

if __name__ == "__main__":
    with open("problem13/input") as f:
        inp = f.read(-1).strip()

    print("Part 1")
    a = arcade.Arcade(computer.parse_program(inp))
    a.play_once()
    print(a.count_blocks())
    # print_screen(screen)

    # The game didn't run because you didn't put in any quarters. Unfortunately,
    # you did not bring any quarters. Memory address 0 represents the number of
    # quarters that have been inserted; set it to 2 to play for free.
    print("\nPart 2")
    a = arcade.Arcade(computer.parse_program(inp))
    a.play_continously()
