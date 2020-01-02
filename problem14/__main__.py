from problem14.refinery import Reactions
import problem14

if __name__ == "__main__":
    with open("problem14/input") as f:
        inp = f.read(-1).strip()

    r = Reactions.parse(inp)
    print("Part 1")
    print(r.calculate_ore(1, "FUEL"))

    print("\nPart 2")
    # After collecting ORE for a while, you check your cargo hold: 1 trillion
    # (1000000000000) units of ORE.
    #
    # With that much ore, given the examples above:
    #
    # - The 13312 ORE-per-FUEL example could produce 82892753 FUEL.
    # - The 180697 ORE-per-FUEL example could produce 5586022 FUEL.
    # - The 2210736 ORE-per-FUEL example could produce 460664 FUEL.
    #
    # Given 1 trillion ORE, what is the maximum amount of FUEL you can produce?
    goal = 1_000_000_000_000

    low = 1
    high = 5000000

    # check if the high is high enough first
    assert r.calculate_ore(high, "FUEL") >= goal, f"high of {high} is not high enough"

    while low <= high:
        mid = (high + low) // 2

        ore_amount = r.calculate_ore(mid, "FUEL")

        if ore_amount < goal:
            # too low - go right
            low = mid + 1

            # best guess can only be when the guess is less than goal
            best_guess = mid
        elif ore_amount > goal:
            # too high - go left
            high = mid - 1

    print(
        f'Best guess: {best_guess} FUEL can be made by {r.calculate_ore(best_guess, "FUEL")} ORE. '
        f'{best_guess + 1} FUEL would require {r.calculate_ore(best_guess + 1, "FUEL")} ORE.'
    )
