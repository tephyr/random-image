#!/usr/bin/env python

"""
Generate a random image using PIL.
"""

import argparse
import math
import random

from   PIL import Image


def generate_image():
    size = (200,200)
    color = (255,0,0,0)
    img = Image.new("RGB",size,color)
    return img

def generate_image_by_output_size(requested_size_in_kilobytes):
    """
    Generate a random bitmap by requested file size.

    Secret formula: 3 * HEIGHT * WIDTH == ~OUTPUT_SIZE_IN_BYTES
    """
    # split height & width
    size_in_kb = long(requested_size_in_kilobytes) * 1024
    axis = long(math.sqrt(size_in_kb/3))

    size = (axis, axis)
    color = (255, 10, 15)
    img = Image.new("RGB", size, color)
    return img

def generate_random_image_by_size(requested_size_in_kilobytes):
    img = generate_image_by_output_size(requested_size_in_kilobytes)
    img_data = []
    for pixel in img.getdata():
        # randomize 1st index, between 0 & 255
        img_data.append((random.randint(0, 255), pixel[1], pixel[2],))

    randomized_image = Image.new("RGB", size=img.size)
    randomized_image.putdata(img_data)
    return randomized_image

def save_image(img, file_path, image_type=None):
    if image_type:
        img.save(file_path, image_type)
    else:
        img.save(file_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', '-s', dest="requested_size", help="Requested size, in kilobytes, of image")
    parser.add_argument('--random', '-r', dest="randomize", action="store_true", help="Make a randomly-colored image")
    parser.add_argument('--output', '-f', dest='output_path', help="Output file")

    args = parser.parse_args()

    if args.requested_size:
        img = None
        if args.randomize:
            img = generate_random_image_by_size(args.requested_size)
        else:
            img = generate_image_by_output_size(args.requested_size)
        save_image(img, args.output_path)

if __name__ == '__main__':
    main()
