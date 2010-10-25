#! /usr/bin/env python
import sys
import getopt
from PIL import Image


def improve(image):

    try:
        im = Image.open(image)
    except IOError:
        print "Error: Unable to open '{0}'".format(image)
        return None

    # Convert the image to grayscale
    im = im.convert('L')

    # Apply a 175 threshold
    im = im.point(lambda i: i if i < 175 else 255)

    # Scale it by 300%
    (width, height) = im.size
    im = im.resize((width*3, height*3), Image.BICUBIC)

    return im

if __name__ == "__main__":
    if len(sys.argv) == 3:
        image = sys.argv[1]
        output = sys.argv[2]

        im = improve(image)
        im.save(output)
    else:
        print "improve.py <filename> <output>"
