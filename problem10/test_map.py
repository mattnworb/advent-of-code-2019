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
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""

map4 = """
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""

map5 = """
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
    @pytest.mark.parametrize("test_map", [map1, map2, map3, map4, map5])
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

    def test_is_asteroid(self):
        m1 = AsteroidMap.parse(map1)
        assert not m1.is_asteroid((0, 0))
        assert m1.is_asteroid((1, 0))
        assert m1.is_asteroid((4, 4))

    def test_is_in_line_of_sight(self):
        m1 = AsteroidMap.parse(map1)
        assert m1.is_in_line_of_sight((1, 0), (4, 0))
        # same but order flopped
        assert m1.is_in_line_of_sight((4, 0), (1, 0))

        assert m1.is_in_line_of_sight((1, 0), (0, 2))
        assert m1.is_in_line_of_sight((1, 0), (1, 2))

        assert not m1.is_in_line_of_sight((1, 0), (3, 4))  # blocked by (2, 2)
        assert not m1.is_in_line_of_sight((1, 0), (4, 1))  # not an asteroid

    def test_count_line_of_sight(self):
        """
        .7..7
        .....
        67775
        ....7
        ...87
        """
        m1 = AsteroidMap.parse(map1)
        assert 7 == m1.count_line_of_sight((1, 0))
        assert 7 == m1.count_line_of_sight((4, 0))

    @pytest.mark.parametrize(
        "test_map,expected",
        [
            (map1, (3, 4)),
            (map2, (5, 8)),
            (map3, (1, 2)),
            (map4, (6, 3)),
            (map5, (11, 13)),
        ],
    )
    def test_find_best_monitoring_station(self, test_map, expected):
        m = AsteroidMap.parse(test_map)
        assert expected == m.find_best_monitoring_station()


def test_slope():
    assert slope((1, 2), (3, 3)) == (2, 1)

    assert slope((1, 2), (3, 4)) == (1, 1)
    # same slope
    assert slope((1, 2), (5, 6)) == (1, 1)

    # same line
    assert slope((1, 2), (5, 2)) == (1, 0)

    assert slope((1, 0), (4, 0)) == (1, 0)

    # order swapped should have negative slope
    assert slope((4, 0), (1, 0)) == (-1, 0)
