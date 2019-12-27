from .main import parse_image, count_pixels


class TestPart1:
    def test_example1(self):
        layers = parse_image("123456789012", 3, 2)
        expected = [
            # layer 1
            [[1, 2, 3], [4, 5, 6],],
            # layer 2
            [[7, 8, 9], [0, 1, 2],],
        ]
        assert layers == expected

    def test_count_pixels(self):
        layer = [
            [1, 2, 3],
            [4, 5, 6],
        ]
        assert count_pixels(layer, 1) == 1
        assert count_pixels(layer, 2) == 1

        layer = [
            [1, 2, 3],
            [0, 0, 0],
        ]
        assert count_pixels(layer, 0) == 3
