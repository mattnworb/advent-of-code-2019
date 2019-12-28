from __future__ import annotations


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
        count = 0

        for other in self.asteroid_positions():
            if other == asteroid:
                continue

            if self.is_in_line_of_sight(asteroid, other):
                count += 1

        return count

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

    def remove_asteroids(self, asteroids_to_remove: set) -> AsteroidMap:
        """Return a new AsteroidMap with the given asteroids removed from this map."""
        return AsteroidMap(self.asteroids - asteroids_to_remove, self.num_x, self.num_y)
