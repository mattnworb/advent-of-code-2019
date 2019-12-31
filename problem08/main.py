from typing import List


class Image:
    @staticmethod
    def parse_image(image_str, width, height):
        assert (
            len(image_str) % (width * height) == 0
        ), f"Image with width={width} and height={height} has number of pixels {len(image_str)}"

        num_layers = len(image_str) // (width * height)

        layers: List[List[List[int]]] = []

        ix = 0
        for l in range(num_layers):
            layers.append([])
            for h in range(height):
                layers[l].append([])
                for w in range(width):
                    pixel = int(image_str[ix])
                    layers[l][h].append(pixel)
                    ix += 1
                    # print(l, w, h)

        return Image(layers, width, height)

    def __init__(self, layers, width, height):
        self.layers = layers
        self.width = width
        self.height = height

    def count_pixels(self, layer_num, value):
        """Return the number of pixels in the layer with the given value"""
        count = 0
        for row in self.layers[layer_num]:
            for pixel in row:
                if pixel == value:
                    count += 1
        return count

    def visible_pixel(self, h, w):
        """Returns the value of the visible pixel at position (h, w), i.e. where height=h and width=w."""
        # 2 = transparent
        # 1 = white
        # 0 = black
        for layer in self.layers:
            p = layer[h][w]
            if p != 2:
                return p

    def render(self, black_char="0", white_char="1") -> str:
        s = ""
        for h in range(self.height):
            # apepnd newline after the first row
            if s != "":
                s += "\n"
            for w in range(self.width):
                p = self.visible_pixel(h, w)
                assert p == 0 or p == 1
                if p == 1:
                    s += white_char
                elif p == 0:
                    s += black_char
        return s
