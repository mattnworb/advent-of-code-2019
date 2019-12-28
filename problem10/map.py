def _map(ch):
    if ch == "#":
        return 1
    elif ch == ".":
        return 0
    raise ValueError()


def slope(a, b):
    """
    Returns the slope between the two points, minimized to the smallest values.
    i.e. returns (2,1) instead of (4,2).
    """
    s = b[0] - a[0], b[1] - a[1]
    return s[0] // gcd(s[0], s[1]), s[1] // gcd(s[0], s[1])


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


class AsteroidMap:
    @staticmethod
    def parse(map_str: str):
        p = []
        for line in map_str.strip().split("\n"):
            chars = list(line.strip())
            r = list(map(_map, chars))
            p.append(r)
        return AsteroidMap(p)

    def __init__(self, positions):
        # test that the two dimensional array has the same length in each row
        assert len(set([len(row) for row in positions])) == 1
        self.positions = positions

    def num_asteroids(self):
        """Returns the number of asteroids in the map."""
        count = 0
        for row in self.positions:
            count += sum(row)
        return count

    def asteroid_positions(self):
        """Return an iterator whose values are the (x, y) positions of each asteroid."""
        for y, row in enumerate(self.positions):
            for x, pos in enumerate(row):
                if pos == 1:
                    yield (x, y)

    def count_line_of_sight(self, asteroid):
        """Count how many asteroids are in line of sight from the given asteroid (with position (x,y))."""
        for other in self.asteroid_positions():
            if other == asteroid:
                continue
            # compute the slope/"vector" between these two asteroids
