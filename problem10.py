from problem10 import AsteroidMap

if __name__ == "__main__":
    with open("problem10/input") as f:
        inp = f.read(-1).strip()

    m = AsteroidMap.parse(inp)
    print("Part 1")
    print(m.find_best_monitoring_station())
