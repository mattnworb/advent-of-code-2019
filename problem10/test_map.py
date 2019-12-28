from .map import AsteroidMap, slope
import pytest

map1 = """
.#..#
.....
#####
....#
...##
"""

map2 = """
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""

map3 = """
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""


class TestAsteroidMap:
    @pytest.mark.parametrize("test_map", [map1, map2, map3])
    def test_num_asteroids(self, test_map):
        assert test_map.count("#") == AsteroidMap.parse(test_map).num_asteroids()

    def test_asteroid_positions(self):
        m1 = AsteroidMap.parse(map1)
        actual = set(m1.asteroid_positions())

        expected = {
            (1, 0),
            (4, 0),
            (0, 2),
            (1, 2),
            (2, 2),
            (3, 2),
            (4, 2),
            (4, 3),
            (3, 4),
            (4, 4),
        }
        assert expected == actual


def test_slope():
    assert slope((1, 2), (3, 3)) == (2, 1)

    assert slope((1, 2), (3, 4)) == (1, 1)
    # same slope
    assert slope((1, 2), (5, 6)) == (1, 1)

    # same line
    assert slope((1, 2), (5, 2)) == (1, 0)
