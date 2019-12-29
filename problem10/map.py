from __future__ import annotations
from math import atan2


def slope(a, b):
    """
    Returns the slope between the two points, minimized to the smallest values.
    i.e. returns (2,1) instead of (4,2).
    """
    s = b[0] - a[0], b[1] - a[1]
    # take the absolute value of the greatest common divisor
    # otherwise for negative slopes we'll end up dividing negative by negative
    div = abs(gcd(s[0], s[1]))
    return s[0] // div, s[1] // div


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def add(a, b):
    """Add two (x,y ) positions together"""
    return a[0] + b[0], a[1] + b[1]


def sort_asteroids_clockwise(monitoring_station, asteroids: set) -> list:
    asteroids_by_slope = {slope(monitoring_station, a): a for a in asteroids}
    # sort the keys.
    #
    # I don't entirely understand why atan2 with x and y swapped works, to sort
    # clockwise from the positive y-axis, but when playing around in a REPL this
    # gives the right answer.
    sorted_slopes = sorted(
        asteroids_by_slope, key=lambda pos: atan2(pos[0], pos[1]), reverse=True
    )
    return list(asteroids_by_slope[s] for s in sorted_slopes)


class AsteroidMap:
    @staticmethod
    def parse(map_str: str):
        lines = [line.strip() for line in map_str.strip().split("\n")]

        asteroids = set()

        for y, line in enumerate(lines):
            # test that the two dimensional array has the same length in each row
            assert len(line) == len(lines[0])
            for x, ch in enumerate(line):
                if ch == "#":
                    asteroids.add((x, y))

        num_x = len(lines[0])
        num_y = len(lines)

        return AsteroidMap(asteroids, num_x, num_y)

    def __init__(self, asteroids, num_x, num_y):
        self.asteroids = frozenset(asteroids)
        self.num_x = num_x
        self.num_y = num_y

    def __repr__(self):
        return f"asteroids={self.asteroids}, num_x={self.num_x}, num_y={self.num_y}"

    def num_asteroids(self):
        """Returns the number of asteroids in the map."""
        return len(self.asteroids)

    def asteroid_positions(self):
        """Return an iterator whose values are the (x, y) positions of each asteroid."""
        return iter(self.asteroids)

    def is_asteroid(self, pos):
        return pos in self.asteroids

    def find_best_monitoring_station(self):
        best_asteroid = None
        highest_count = 0

        for asteroid in self.asteroid_positions():
            count = self.count_line_of_sight(asteroid)
            if count > highest_count:
                highest_count = count
                best_asteroid = asteroid

        return best_asteroid, highest_count

    def count_line_of_sight(self, asteroid):
        """
        Count how many asteroids are in line of sight from the given asteroid
        (with position (x,y)).
        """
        return len(self.asteroids_in_line_of_sight(asteroid))

    def asteroids_in_line_of_sight(self, asteroid) -> set:
        """Return the set of asteroids in line of sight of the given asteroid."""
        return {
            other
            for other in self.asteroid_positions()
            if other != asteroid and self.is_in_line_of_sight(asteroid, other)
        }

    def in_bounds(self, pos) -> bool:
        """Test if position pos is in bounds of the map."""
        return (
            pos[0] >= 0 and pos[0] < self.num_x and pos[1] >= 0 and pos[1] < self.num_y
        )

    def is_in_line_of_sight(self, asteroid1, asteroid2) -> bool:
        """Test if asteroid2 is in line of sight from asteroid1"""

        if not self.is_asteroid(asteroid1) or not self.is_asteroid(asteroid2):
            return False

        s = slope(asteroid1, asteroid2)

        candidate = add(asteroid1, s)
        # take multiples of s
        while self.in_bounds(candidate):
            if candidate == asteroid2:
                return True

            if self.is_asteroid(candidate):
                # found a blocker
                return False

            candidate = add(candidate, s)

        # failed out of bounds check above
        return False

    def remove_asteroids(self, asteroids_to_remove) -> AsteroidMap:
        """Return a new AsteroidMap with the given asteroids removed from this map."""
        return AsteroidMap(
            self.asteroids - set(asteroids_to_remove), self.num_x, self.num_y
        )


def vaporize_order(asteroid_map):
    monitoring_station, _ = asteroid_map.find_best_monitoring_station()

    map_copy = asteroid_map
    vaporized = []

    while map_copy.num_asteroids() > 1:
        to_be_vaporized = sort_asteroids_clockwise(
            monitoring_station, map_copy.asteroids_in_line_of_sight(monitoring_station)
        )

        vaporized.extend(to_be_vaporized)
        map_copy = map_copy.remove_asteroids(to_be_vaporized)

    return vaporized
