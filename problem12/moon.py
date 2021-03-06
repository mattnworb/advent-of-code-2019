from typing import Tuple, List, Iterable, Set, Optional
from itertools import combinations
import logging

from problem10.map import gcd

logger = logging.getLogger(__name__)


class Moon:
    def __init__(self, position: Iterable[int], velocity=[0, 0, 0]):
        self.position = list(position)
        self.velocity = list(velocity)

    def __repr__(self):
        return f"pos=<{self.position}>, vel=<{self.velocity}>"

    def add_velocity_to_position(self):
        for axis in [0, 1, 2]:
            self.position[axis] += self.velocity[axis]

    def total_energy(self):
        # The total energy for a single moon is its potential energy multiplied
        # by its kinetic energy. A moon's potential energy is the sum of the
        # absolute values of its x, y, and z position coordinates. A moon's
        # kinetic energy is the sum of the absolute values of its velocity
        # coordinates.
        return self.potential_energy() * self.kinetic_energy()

    def potential_energy(self):
        return sum(abs(p) for p in self.position)

    def kinetic_energy(self):
        return sum(abs(v) for v in self.velocity)


def _copy_moons(moons):
    return [Moon(m.position, m.velocity) for m in moons]


def run_simulation(moons: List[Moon], rounds: int) -> List[Moon]:
    moons = _copy_moons(moons)

    # Simulate the motion of the moons in time steps. Within each time step,
    # first update the velocity of every moon by applying gravity. Then, once
    # all moons' velocities have been updated, update the position of every moon
    # by applying velocity. Time progresses by one step once all of the
    # positions are updated.

    for round in range(rounds):
        apply_gravity(moons)
        logger.debug("Round=%d after gravity, moons=%s", round, moons)

        # Once all gravity has been applied, apply velocity: simply add the
        # velocity of each moon to its own position. For example, if Europa has
        # a position of x=1, y=2, z=3 and a velocity of x=-2, y=0,z=3, then its
        # new position would be x=-1, y=2, z=6. This process does not modify the
        # velocity of any moon.
        for moon in moons:
            moon.add_velocity_to_position()

    return moons


def apply_gravity(moons: List[Moon]):
    # To apply gravity, consider every pair of moons. On each axis (x, y, and
    # z), the velocity of each moon changes by exactly +1 or -1 to pull the
    # moons together. For example, if Ganymede has an x position of 3, and
    # Callisto has a x position of 5, then Ganymede's x velocity changes by +1
    # (because 5 > 3) and Callisto's x velocity changes by -1 (because 3 < 5).
    # However, if the positions on a given axis are the same, the velocity on
    # that axis does not change for that pair of moons.

    for m1, m2 in combinations(moons, 2):

        for axis in range(3):
            if m1.position[axis] < m2.position[axis]:
                m1.velocity[axis] += 1
                m2.velocity[axis] -= 1
            elif m1.position[axis] > m2.position[axis]:
                m1.velocity[axis] -= 1
                m2.velocity[axis] += 1


def total_energy_in_system(moons: List[Moon]) -> int:
    return sum(m.total_energy() for m in moons)


def _hash(moons, axis):
    k = []
    for moon in moons:
        k.append(moon.position[axis])
    for moon in moons:
        k.append(moon.velocity[axis])
    return tuple(k)


def steps_until_repeat(moons, max_search_rounds=10000):
    moons = _copy_moons(moons)

    history: List[Set[Tuple[int]]] = [set(), set(), set()]
    names = ["X", "Y", "Z"]
    cycle_length: List[Optional[int]] = [None, None, None]

    for axis in range(3):
        history[axis].add(_hash(moons, axis))

    for round in range(1, max_search_rounds):
        moons = run_simulation(moons, 1)
        for axis in range(3):
            k = _hash(moons, axis)
            if k in history[axis] and cycle_length[axis] is None:
                cycle_length[axis] = round
                logger.info(
                    "found cycle in %s after %d rounds", names[axis], cycle_length[axis]
                )

            elif cycle_length[axis] is None:
                history[axis].add(k)

        if all(c is not None for c in cycle_length):
            break

    assert all(
        c is not None for c in cycle_length
    ), f"Did not find cycles after {max_search_rounds} rounds"

    # LCM of 3 numbers is lcm(lcm(a, b), c)
    return int(lcm(lcm(cycle_length[0], cycle_length[1]), cycle_length[2]))


def lcm(a, b):
    return abs(a * b) / gcd(a, b)
