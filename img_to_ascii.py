from argparse import ArgumentParser
from uuid import uuid4

import numpy as np
from PIL import Image


def map_int_to_ascii(val, ascii_arr, min1, max1, min2, max2):
    if val < min1:
        return ascii_arr[int(min2)]
    if val > max1:
        return ascii_arr[int(max2)]

    mapped_value = int((val - min1) * ((max2 - min2) / (max1 - min1)) + min2)

    if max2 >= mapped_value >= min2:
        return ascii_arr[mapped_value]


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--image", help="path to image file")
    args = parser.parse_args()

    ascii_gradient = (
    "`^\",:;Il!i~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    )
    
    img_lum = Image.open(args.image).convert("L")
    img_arr = np.asarray(img_lum)

    map_vectorized = np.vectorize(map_int_to_ascii)
    ascii_arr = map_vectorized(img_arr, 0, 255, 0, len(ascii_gradient) - 1)

    np.savetxt(f"{args.image}_ascii_{uuid4().hex}.txt", ascii_arr, fmt="%s")
