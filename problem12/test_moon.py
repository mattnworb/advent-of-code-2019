import logging
from sys import stdout

# logging.basicConfig(level=logging.INFO)

import pytest  # type: ignore

from .moon import (
    Moon,
    run_simulation,
    total_energy_in_system,
    apply_gravity,
    steps_until_repeat,
    lcm,
)


class TestMoon:
    def test_velocity_defaults_to_zero(self):
        m = Moon((1, 1, 1))
        assert m.velocity == [0, 0, 0]

    def test_add_velocity_to_position(self):
        m = Moon((1, 2, 3), (-1, 4, 10))
        m.add_velocity_to_position()
        assert m.position == [0, 6, 13]


def test_run_simulation_zero_rounds():
    moons = [
        Moon((-1, 0, 2)),
        Moon((2, -10, -7)),
        Moon((4, -8, 8)),
        Moon((3, 5, -1)),
    ]

    run_simulation(moons, 0)
    assert moons[0].velocity == [0, 0, 0]
    assert moons[1].velocity == [0, 0, 0]
    assert moons[2].velocity == [0, 0, 0]
    assert moons[3].velocity == [0, 0, 0]
    assert moons[0].position == [-1, 0, 2]
    assert moons[1].position == [2, -10, -7]
    assert moons[2].position == [4, -8, 8]
    assert moons[3].position == [3, 5, -1]


def test_apply_gravity():
    # For example, if Ganymede has an x position of 3, and Callisto has a x
    # position of 5, then Ganymede's x velocity changes by +1 (because 5 > 3)
    # and Callisto's x velocity changes by -1 (because 3 < 5).
    moons = [Moon((3, 3, 3)), Moon((5, 5, 5))]
    apply_gravity(moons)

    assert moons[0].velocity == [1, 1, 1]
    assert moons[1].velocity == [-1, -1, -1]


def test_apply_gravity_same_position():
    # However, if the positions on a given axis are the same, the velocity on
    # that axis does not change for that pair of moons.
    moons = [Moon((5, 5, 5)), Moon((5, 5, 5))]
    apply_gravity(moons)

    assert moons[0].velocity == [0, 0, 0]
    assert moons[1].velocity == [0, 0, 0]


EXAMPLE_1_MOONS = [
    Moon((-1, 0, 2)),
    Moon((2, -10, -7)),
    Moon((4, -8, 8)),
    Moon((3, 5, -1)),
]

EXAMPLE_2_MOONS = [
    Moon((-8, -10, 0)),
    Moon((5, 5, 10)),
    Moon((2, -7, 3)),
    Moon((9, -8, -3)),
]


@pytest.mark.parametrize(
    "num_rounds,input_moons,expected_moons",
    [
        (
            1,
            EXAMPLE_1_MOONS,
            [
                Moon((2, -1, 1), (3, -1, -1)),
                Moon((3, -7, -4), (1, 3, 3)),
                Moon((1, -7, 5), (-3, 1, -3)),
                Moon((2, 2, 0), (-1, -3, 1)),
            ],
        ),
        (
            10,
            EXAMPLE_1_MOONS,
            [
                Moon((2, 1, -3), (-3, -2, 1)),
                Moon((1, -8, 0), (-1, 1, 3)),
                Moon((3, -6, 1), (3, 2, -3)),
                Moon((2, 0, 4), (1, -1, -1)),
            ],
        ),
        (
            100,
            EXAMPLE_2_MOONS,
            [
                Moon((8, -12, -9), (-7, 3, 0)),
                Moon((13, 16, -3), (3, -11, -5)),
                Moon((-29, -11, -1), (-3, 7, 4)),
                Moon((16, -13, 23), (7, 1, 1)),
            ],
        ),
    ],
)
def test_run_simulation(num_rounds, input_moons, expected_moons):
    # don't modify original list/instances
    input_copy = [Moon(m.position, m.velocity) for m in input_moons]

    actual = run_simulation(input_copy, num_rounds)
    assert len(actual) == len(input_moons)

    for n, expected in enumerate(expected_moons):
        print("Expected=", expected, ", Actual=", actual[n])
        assert expected.position == actual[n].position
        assert expected.velocity == actual[n].velocity


def test_total_energy_in_system():
    moons = [
        Moon((2, 1, -3), (-3, -2, 1)),
        Moon((1, -8, 0), (-1, 1, 3)),
        Moon((3, -6, 1), (3, 2, -3)),
        Moon((2, 0, 4), (1, -1, -1)),
    ]
    assert 179 == total_energy_in_system(moons)


def test_total_energy_in_system2():
    moons = run_simulation(EXAMPLE_2_MOONS, 100)
    assert 1940 == total_energy_in_system(moons)


def test_steps_until_repeat():
    assert 2772 == steps_until_repeat(EXAMPLE_1_MOONS)


def test_steps_until_repeat_slow():
    assert 4686774924 == steps_until_repeat(EXAMPLE_2_MOONS)


def test_lcm():
    assert 12 == lcm(4, 6)
