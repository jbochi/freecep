#! /usr/bin/env python
import sys
import getopt
from PIL import Image

import cep

def improve(image):

    try:
        im = Image.open(image)
    except IOError:
        print "Error: Unable to open '{0}'".format(image)
        return None

    c = cep.Correios()
    im = c._improve_image(im)    

    return im

if __name__ == "__main__":
    if len(sys.argv) == 3:
        image = sys.argv[1]
        output = sys.argv[2]

        im = improve(image)
        im.save(output)
    else:
        print "improve.py <filename> <output>"
