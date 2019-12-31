import logging
from sys import stdout

logging.basicConfig(level=logging.INFO)

import pytest  # type: ignore

import problem12.moon as moon


class TestMoon:
    def test_velocity_defaults_to_zero(self):
        m = moon.Moon((1, 1, 1))
        assert m.velocity == (0, 0, 0)

    def test_add_velocity_to_position(self):
        m = moon.Moon((1, 2, 3), (-1, 4, 10))
        m.add_velocity_to_position()
        assert m.position == (0, 6, 13)


def test_run_simulation_zero_rounds():
    moons = [
        moon.Moon((-1, 0, 2)),
        moon.Moon((2, -10, -7)),
        moon.Moon((4, -8, 8)),
        moon.Moon((3, 5, -1)),
    ]

    moon.run_simulation(moons, 0)
    assert moons[0].velocity == (0, 0, 0)
    assert moons[1].velocity == (0, 0, 0)
    assert moons[2].velocity == (0, 0, 0)
    assert moons[3].velocity == (0, 0, 0)
    assert moons[0].position == (-1, 0, 2)
    assert moons[1].position == (2, -10, -7)
    assert moons[2].position == (4, -8, 8)
    assert moons[3].position == (3, 5, -1)


def test_apply_gravity():
    # For example, if Ganymede has an x position of 3, and Callisto has a x
    # position of 5, then Ganymede's x velocity changes by +1 (because 5 > 3)
    # and Callisto's x velocity changes by -1 (because 3 < 5).
    moons = [moon.Moon((3, 3, 3)), moon.Moon((5, 5, 5))]
    after = moon.apply_gravity(moons)
    assert len(after) == len(moons)
    assert after[0].velocity == (1, 1, 1)
    assert after[1].velocity == (-1, -1, -1)


def test_apply_gravity_same_position():
    # However, if the positions on a given axis are the same, the velocity on
    # that axis does not change for that pair of moons.
    moons = [moon.Moon((5, 5, 5)), moon.Moon((5, 5, 5))]
    after = moon.apply_gravity(moons)
    assert len(after) == len(moons)
    assert after[0].velocity == (0, 0, 0)
    assert after[1].velocity == (0, 0, 0)


EXAMPLE_1_MOONS = [
    moon.Moon((-1, 0, 2)),
    moon.Moon((2, -10, -7)),
    moon.Moon((4, -8, 8)),
    moon.Moon((3, 5, -1)),
]

EXAMPLE_2_MOONS = [
    moon.Moon((-8, -10, 0)),
    moon.Moon((5, 5, 10)),
    moon.Moon((2, -7, 3)),
    moon.Moon((9, -8, -3)),
]


@pytest.mark.parametrize(
    "num_rounds,input_moons,expected_moons",
    [
        (
            1,
            EXAMPLE_1_MOONS,
            [
                moon.Moon((2, -1, 1), (3, -1, -1)),
                moon.Moon((3, -7, -4), (1, 3, 3)),
                moon.Moon((1, -7, 5), (-3, 1, -3)),
                moon.Moon((2, 2, 0), (-1, -3, 1)),
            ],
        ),
        (
            10,
            EXAMPLE_1_MOONS,
            [
                moon.Moon((2, 1, -3), (-3, -2, 1)),
                moon.Moon((1, -8, 0), (-1, 1, 3)),
                moon.Moon((3, -6, 1), (3, 2, -3)),
                moon.Moon((2, 0, 4), (1, -1, -1)),
            ],
        ),
        (
            100,
            EXAMPLE_2_MOONS,
            [
                moon.Moon((8, -12, -9), (-7, 3, 0)),
                moon.Moon((13, 16, -3), (3, -11, -5)),
                moon.Moon((-29, -11, -1), (-3, 7, 4)),
                moon.Moon((16, -13, 23), (7, 1, 1)),
            ],
        ),
    ],
)
def test_run_simulation(num_rounds, input_moons, expected_moons):
    actual = moon.run_simulation(list(input_moons), num_rounds)
    assert len(actual) == len(input_moons)

    for n, expected in enumerate(expected_moons):
        print("Expected=", expected, ", Actual=", actual[n])
        assert expected.position == actual[n].position
        assert expected.velocity == actual[n].velocity
