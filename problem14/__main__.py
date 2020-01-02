from .refinery import Reactions

if __name__ == "__main__":
    with open("problem14/input") as f:
        inp = f.read(-1).strip()

    r = Reactions.parse(inp)
    print("Part 1")
    print(r.calculate_ore(1, "FUEL"))
