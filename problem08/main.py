def parse_image(image_str, width, height):
    assert (
        len(image_str) % (width * height) == 0
    ), f"Image with width={width} and height={height} has number of pixels {len(image_str)}"

    num_layers = len(image_str) // (width * height)

    layers = []

    # for ix, pixel in enumerate(image_str):
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

    return layers


def count_pixels(layer, value):
    """Return the number of pixels in the layer with the given value"""
    count = 0
    for row in layer:
        for pixel in row:
            if pixel == value:
                count += 1
    return count
