from typing import Tuple, List, Iterable
from itertools import combinations
import logging

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
        moons = apply_gravity(moons)
        logger.debug("Round=%d after gravity, moons=%s", round, moons)

        # Once all gravity has been applied, apply velocity: simply add the
        # velocity of each moon to its own position. For example, if Europa has
        # a position of x=1, y=2, z=3 and a velocity of x=-2, y=0,z=3, then its
        # new position would be x=-1, y=2, z=6. This process does not modify the
        # velocity of any moon.
        for moon in moons:
            moon.add_velocity_to_position()

    return moons


def apply_gravity(moons: List[Moon]) -> List[Moon]:
    # To apply gravity, consider every pair of moons. On each axis (x, y, and
    # z), the velocity of each moon changes by exactly +1 or -1 to pull the
    # moons together. For example, if Ganymede has an x position of 3, and
    # Callisto has a x position of 5, then Ganymede's x velocity changes by +1
    # (because 5 > 3) and Callisto's x velocity changes by -1 (because 3 < 5).
    # However, if the positions on a given axis are the same, the velocity on
    # that axis does not change for that pair of moons.

    new_moons = [Moon(m.position, m.velocity) for m in moons]

    for m1, m2 in combinations(new_moons, 2):

        for axis in [0, 1, 2]:
            if m1.position[axis] < m2.position[axis]:
                m1.velocity[axis] += 1
                m2.velocity[axis] -= 1
            elif m1.position[axis] > m2.position[axis]:
                m1.velocity[axis] -= 1
                m2.velocity[axis] += 1
    return new_moons


def total_energy_in_system(moons: List[Moon]) -> int:
    return sum(m.total_energy() for m in moons)
