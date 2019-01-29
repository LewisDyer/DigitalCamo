"""This file handles the logic for the creation of camouflage, including the 
   generative process underlying its creation.

   Parts of this file may be edited if you'd like to make more extensive modifications to the
   generative process, however the majority of basic changes would be better made in
   user_config."""

from PIL import Image, ImageDraw, ImageColor
from random import random, randrange, choice
from math import ceil
import numpy as np

def tile_board(start_x, start_y, squares, square_size, 
               depth_prob = DEPTH_PROB, max_depth= MAX_DEPTH):
        for i in range(squares[0]):
            for j in range(squares[1]):
                draw_square(start_x + square_size*i, start_y + square_size*j, square_size, LAYERS)
                if random() <= depth_prob and max_depth:
                    tile_board(start_x + square_size*i, start_y + square_size*j, 
                               (1,1), depth_prob = depth_prob * 0.5, max_depth = max_depth-1)

def draw_square(start_x, start_y, size, layers):

        randoms = [randrange(1, 4, 1) for l in range(layers)]
        sizes = sorted([r / sum(randoms) for r in randoms], reverse=True)

        ANCHORS = [(0, 0), #top left
                   (0, 1), #bottom left
                   (1, 0), #top right
                   (1, 1)] #bottom right
        anchor = choice(ANCHORS)

        anchor_x1 = start_x + anchor[0] * size
        anchor_y1 = start_y + anchor[1] * size

        anchor = (1 if (anchor[0] == 0) else -1, 1 if (anchor[1] == 0) else -1)

        colour = choice(COLOURS)
        #print("base colour is ", colour)
        draw1.rectangle((start_x, start_y, start_x + size, start_y +size), fill=colour) # base square
        for length in sizes:
            colour = choice(COLOURS)
            draw1.rectangle((anchor_x1, anchor_y1, 
                             anchor_x1 + (size * length * anchor[0]), anchor_y1 + (size * length * anchor[1])), fill=colour, outline="black")

def make_camo(x, y, size, square_size = 10):
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    draw1 = ImageDraw.Draw(canvas)
    # Overestimate how many squares we'll need - making a little more better than not enough!
    no_squares = (ceil(size[0] / square_size), ceil(size[1] / square_size)) 
    tile_board(x, y, no_squares, square_size)

    data = np.array(canvas)
    
    data[(data == (255, 255, 255, 255)).all(axis = -1)] = ImageColor.getcolor(SLIVER_COLOUR, 'RGBA')

    canvas = Image.fromarray(data, mode='RGBA')
    del draw1

    return canvas