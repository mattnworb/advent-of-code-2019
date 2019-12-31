from .map import AsteroidMap, slope, sort_asteroids_clockwise, vaporize_order
import pytest  # type: ignore

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
        "test_map,coord,count",
        [
            (map1, (3, 4), 8),
            (map2, (5, 8), 33),
            (map3, (1, 2), 35),
            (map4, (6, 3), 41),
            (map5, (11, 13), 210),
        ],
    )
    def test_find_best_monitoring_station(self, test_map, coord, count):
        m = AsteroidMap.parse(test_map)
        assert (coord, count) == m.find_best_monitoring_station()

    def test_equals(self):
        m1 = AsteroidMap.parse(map1)
        m2 = AsteroidMap.parse(map2)
        assert m1 == m1
        assert m1 != m2
        assert m2 != m1
        assert not m1 == m2

    def test_remove_asteroids(self):
        m = AsteroidMap.parse(
            """
        ..#
        .#.
        """
        )

        new_map = m.remove_asteroids({(2, 0)})
        assert new_map != m
        assert {(1, 1)} == set(new_map.asteroid_positions())

    def test_vaporize_order(self):
        # In the large example above (the one with the best monitoring station location at 11,13):
        #
        # - The 1st asteroid to be vaporized is at 11,12.
        # - The 2nd asteroid to be vaporized is at 12,1.
        # - The 3rd asteroid to be vaporized is at 12,2.
        # - The 10th asteroid to be vaporized is at 12,8.
        # - The 20th asteroid to be vaporized is at 16,0.
        # - The 50th asteroid to be vaporized is at 16,9.
        # - The 100th asteroid to be vaporized is at 10,16.
        # - The 199th asteroid to be vaporized is at 9,6.
        # - The 200th asteroid to be vaporized is at 8,2.
        # - The 201st asteroid to be vaporized is at 10,9.
        # - The 299th and final asteroid to be vaporized is at 11,1.
        m = AsteroidMap.parse(map5)
        vaporized = vaporize_order(m)

        assert vaporized[0] == (11, 12)
        assert vaporized[1] == (12, 1)
        assert vaporized[2] == (12, 2)
        assert vaporized[9] == (12, 8)
        assert vaporized[19] == (16, 0)
        assert vaporized[49] == (16, 9)
        assert vaporized[99] == (10, 16)
        assert vaporized[198] == (9, 6)
        assert vaporized[199] == (8, 2)
        assert vaporized[200] == (10, 9)
        assert vaporized[298] == (11, 1)


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


def test_sort_asteroids_clockwise():
    m = AsteroidMap.parse(
        """
        .#....#####...#..
        ##...##.#####..##
        ##...#...#.#####.
        ..#.....#...###..
        ..#.#.....#....##
    """
    )

    # The first nine asteroids to get vaporized, in order, would be:
    #
    # .#....###24...#..
    # ##...##.13#67..9#
    # ##...#...5.8####.
    # ..#.....X...###..
    # ..#.#.....#....##

    monitoring_station = (8, 3)
    assert m.find_best_monitoring_station()[0] == monitoring_station

    first_nine = [
        (8, 1),
        (9, 0),
        (9, 1),
        (10, 0),
        (9, 2),
        (11, 1),
        (12, 1),
        (11, 2),
        (15, 1),
    ]

    # sanity check - `<`` is subset
    assert set(first_nine) < set(m.asteroid_positions())
    assert set(first_nine) < m.asteroids_in_line_of_sight(monitoring_station)

    sort_result = sort_asteroids_clockwise(
        monitoring_station, m.asteroids_in_line_of_sight(monitoring_station)
    )
    print(sort_result)
    assert first_nine == sort_result[:9]
