"""This file handles the logic for the creation of camouflage, including the 
   generative process underlying its creation.

   Parts of this file may be edited if you'd like to make more extensive modifications to the
   generative process, however the majority of basic changes would be better made in
   user_config."""

from PIL import Image, ImageDraw, ImageColor
from random import random, randrange, choice
from math import ceil
import numpy as np

import user_config


def tile_board(start_x, start_y, squares, draw, palette="Basic", 
               square_size=10, depth_prob=0.5, max_depth=3, 
               layers=3):

    colours = user_config.get_palette(palette)
    for i in range(squares[0]):
        for j in range(squares[1]):
            draw_square(start_x + square_size*i, start_y + square_size*j, square_size, layers, draw, colours=colours)
            if random() <= depth_prob and max_depth:
                tile_board(start_x + square_size*i, start_y + square_size*j, 
                            (1,1), draw, palette, square_size, depth_prob=depth_prob*0.5, 
                            max_depth=max_depth-1, layers=layers-1)

def draw_square(start_x, start_y, size, layers, draw, colours):

        #randoms = [randrange(1, 4, 1) for l in range(layers)]
        #sizes = sorted([r / sum(randoms) for r in randoms], reverse=True)
        sizes = sorted([random() for l in range(layers)], reverse=True)
        print(sizes)

        ANCHORS = [(0, 0), #top left
                   (0, 1), #bottom left
                   (1, 0), #top right
                   (1, 1)] #bottom right
        anchor = choice(ANCHORS)

        anchor_x1 = start_x + anchor[0] * size
        anchor_y1 = start_y + anchor[1] * size

        anchor = (1 if (anchor[0] == 0) else -1, 1 if (anchor[1] == 0) else -1)

        colour = choice(colours[0])
        draw.rectangle((start_x, start_y, start_x + size, start_y +size), fill=colour) # base square
        for length in sizes:
            colour = choice(colours[0])
            draw.rectangle((anchor_x1, anchor_y1, 
                             anchor_x1 + (size * length * anchor[0]), 
                             anchor_y1 + (size * length * anchor[1])), 
                             fill=colour, outline=colours[1])

def make_camo(x, y, size, palette="Basic", 
               square_size=10, depth_prob=0.5, max_depth=3, 
               layers=3):
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    draw1 = ImageDraw.Draw(canvas)
    # Overestimate how many squares we'll need - making a little more better than not enough!
    no_squares = (ceil(size[0] / square_size), ceil(size[1] / square_size)) 
    tile_board(x, y, no_squares, draw1, palette,
               square_size, depth_prob, max_depth, 
               layers)

    data = np.array(canvas)
    canvas = Image.fromarray(data, mode='RGBA')
    del draw1

    return canvas