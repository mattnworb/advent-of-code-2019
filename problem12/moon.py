class Position:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"x={self.x: d}, y={self.y: d}, z={self.z: d}"


class Moon:
    def __init__(self, position: Position, velocity: Position):
        self.position = position
        self.velocity = velocity

    def __repr__(self):
        return f"pos=<{self.position}>, vel=<{self.velocity}>"
