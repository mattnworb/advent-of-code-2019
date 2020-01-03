import problem10.map

if __name__ == "__main__":
    with open("problem10/input") as f:
        inp = f.read(-1).strip()

    m = problem10.map.AsteroidMap.parse(inp)
    print("Part 1")

    monitoring_station, count = m.find_best_monitoring_station()
    print("Monitoring station:", monitoring_station)

    # Part 2:
    #
    # Fortunately, in addition to an asteroid scanner, the new monitoring
    # station also comes equipped with a giant rotating laser perfect for
    # vaporizing asteroids. The laser starts by pointing up and always rotates
    # clockwise, vaporizing any asteroid it hits.
    #
    # If multiple asteroids are exactly in line with the station, the laser only
    # has enough power to vaporize one of them before continuing its rotation.
    # In other words, the same asteroids that can be detected can be vaporized,
    # but if vaporizing one asteroid makes another one detectable, the
    # newly-detected asteroid won't be vaporized until the laser has returned to
    # the same position by rotating a full 360 degrees.
    #
    # The Elves are placing bets on which will be the 200th asteroid to be
    # vaporized. Win the bet by determining which asteroid that will be; what do
    # you get if you multiply its X coordinate by 100 and then add its Y
    # coordinate? (For example, 8,2 becomes 802.)

    vaporized = problem10.map.vaporize_order(m)

    print("\nPart 2")
    print(f"200th vaporized asteroid: {vaporized[199]}")
