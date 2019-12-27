from problem08.main import parse_image, count_pixels

# The image you received is 25 pixels wide and 6 pixels tall.

# To make sure the image wasn't corrupted during transmission, the Elves would
# like you to find the layer that contains the fewest 0 digits. On that layer,
# what is the number of 1 digits multiplied by the number of 2 digits?


if __name__ == "__main__":
    with open("problem08/input") as f:
        inp = f.read(-1).strip()

    image = parse_image(inp, 25, 6)

    # find the layer that contains the fewest 0 digits
    layer_with_min_zeros = None
    zero_count = None
    for layer in image:
        zc = count_pixels(layer, 0)
        if zero_count is None or zc < zero_count:
            zero_count = zc
            layer_with_min_zeros = layer

    # what is the number of 1 digits multiplied by the number of 2 digits?
    product = count_pixels(layer_with_min_zeros, 1) * count_pixels(
        layer_with_min_zeros, 2
    )
    print(product)
