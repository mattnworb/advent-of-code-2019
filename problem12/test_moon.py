from .moon import Moon, Position


class TestMoon:
    def test_repr(self):
        pos = Position(-1, 0, 2)
        vel = Position(0, 0, 0)
        m = Moon(pos, vel)
        assert repr(m) == "pos=<x=-1, y= 0, z= 2>, vel=<x= 0, y= 0, z= 0>"
