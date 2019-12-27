from .main import Image


class TestPart1:
    def test_example1(self):
        image = Image.parse_image("123456789012", 3, 2)
        expected = [
            # layer 1
            [[1, 2, 3], [4, 5, 6],],
            # layer 2
            [[7, 8, 9], [0, 1, 2],],
        ]
        assert image.layers == expected

    def test_count_pixels(self):
        # [
        #     [1, 2, 3],
        #     [4, 5, 6],
        # ]
        image = Image.parse_image("123345", 2, 3)
        assert image.count_pixels(0, value=1) == 1
        assert image.count_pixels(0, value=2) == 1
        assert image.count_pixels(0, value=3) == 2

        # [
        #     [1, 2, 3],
        #     [0, 0, 0],
        # ]
        image = Image.parse_image("123000", 2, 3)
        assert image.count_pixels(0, 0) == 3

    def test_visible_pixel(self):
        image = Image.parse_image("0222112222120000", 2, 2)
        assert 4 == len(image.layers)
        # The top-left pixel is black because the top layer is 0.
        assert 0 == image.visible_pixel(0, 0)
        # The top-right pixel is white because the top layer is 2 (transparent), but the second layer is 1.
        assert 1 == image.visible_pixel(0, 1)
        # The bottom-left pixel is white because the top two layers are 2, but the third layer is 1.
        assert 1 == image.visible_pixel(1, 0)
        # The bottom-right pixel is black because the only visible pixel in that position is 0 (from layer 4).
        assert 0 == image.visible_pixel(1, 1)

    def test_render(self):
        image = Image.parse_image("0222112222120000", 2, 2)
        expected = "01\n10"
        assert expected == image.render()
