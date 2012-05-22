#!/usr/bin/env python

"""
Generate a random image using PIL.
"""

import argparse
import math
import random

from   PIL import Image, ImageColor


def generate_image_by_output_size(requested_size_in_kilobytes):
    """
    Generate a random bitmap by requested file size.

    Secret formula: 3 * HEIGHT * WIDTH == ~OUTPUT_SIZE_IN_BYTES
    """
    # split height & width to make box
    size_in_kb = long(requested_size_in_kilobytes) * 1024
    axis = long(math.sqrt(size_in_kb/3))

    size = (axis, axis)
    color = (255, 0, 0)
    img = Image.new("RGB", size, color)
    return img

def generate_random_image_by_size(requested_size_in_kilobytes, monochrome=False):
    """
    Generate a random image by size, optionally in monochrome
    """
    img = generate_image_by_output_size(requested_size_in_kilobytes)
    img_data = []
    pixel_color = ""
    monochrome_colors = ("white", "black", )
    for pixel in img.getdata():
        if monochrome:
            pixel_color = random.choice(monochrome_colors)
            img_data.append(ImageColor.getrgb(pixel_color))
        else:
            # randomize indices between 0 & 255
            img_data.append((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),))

    randomized_image = Image.new("RGB", size=img.size)
    randomized_image.putdata(img_data)
    return randomized_image

def save_image(img, file_path, image_type=None):
    """
    Helper to save Image object to file, with optional explicit type.
    """
    if image_type:
        img.save(file_path, image_type)
    else:
        img.save(file_path)

def main():
    """
    Parse arguments and run functions.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--monochrome', '-m', dest="monochrome", action="store_true", help="Make image black-and-white")
    parser.add_argument('--size', '-s', dest="requested_size", help="Requested size, in kilobytes, of image")
    parser.add_argument('--random', '-r', dest="randomize", action="store_true", help="Make a randomly-colored image")
    parser.add_argument('--output', '-f', dest='output_path', help="Output file")

    args = parser.parse_args()

    if args.requested_size:
        img = None
        if args.randomize:
            img = generate_random_image_by_size(args.requested_size, monochrome=args.monochrome)
        else:
            img = generate_image_by_output_size(args.requested_size)
        save_image(img, args.output_path)

if __name__ == '__main__':
    main()
