from problem12 import moon

if __name__ == "__main__":
    # input:
    # <x=17, y=5, z=1>
    # <x=-2, y=-8, z=8>
    # <x=7, y=-6, z=14>
    # <x=1, y=-10, z=4>
    inp = [
        moon.Moon((17, 5, 1)),
        moon.Moon((-2, -8, 8)),
        moon.Moon((7, -6, 14)),
        moon.Moon((1, -10, 4)),
    ]

    # What is the total energy in the system after simulating the moons given in
    # your scan for 1000 steps?
    print("Part 1")
    print(moon.total_energy_in_system(moon.run_simulation(inp, 1000)))
