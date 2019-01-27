from PIL import ImageTk, Image, ImageDraw, ImageColor
from pathlib import Path
import os
from os.path import abspath, dirname
import tkinter as tk
import random
from math import ceil
import numpy as np




"""Feel free to define your own palettes! Palettes have a name, a list of colours (which are chosen from randomly when 
   colouring a square), and an additional colour used to fill in the cracks in the image."""
palettes = {
    "Digital Camo": (['#007400', '#006600', '#005600', '#004400'], '#00AF00'),

    "Magma Bubbles": (['#740000', '#660000', '#560000', '#210000', '#DD5812', '#DD5830'], '#AF0000'),

    "Drowning": (['#000074', '#000066', '#000056', '#000021'], '#0000AF'),

    "Retro": (['#7851a9','#1034a6','#0087bd', '#c40233', '#ffd300'], '#000000'),

    "Google": (['#008744', '#0057e7', '#d62d20', '#ffa700'], '#ffffff'),

    "Basic": (['#FFFFFF', '#222222', '#444444', '#666666', '#888888', '#AAAAAA', '#CCCCCC'], '#EEEEEE'),
}

CHOSEN_PALETTE = "Digital Camo"

def random_colour():
    # generates a random hex colour code
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)

try:
    COLOURS, SLIVER_COLOUR = palettes[CHOSEN_PALETTE]
except KeyError:
    COLOURS, SLIVER_COLOUR = ([random_colour() for i in range(5)], random_colour())
    print("Palette not found, using random colours...")
    print(COLOURS)
    print(SLIVER_COLOUR)


DEPTH_PROB = 0.6
MAX_DEPTH = 4
LAYERS = 2

def make_mask(image_path, threshold=200):
    """Given the filename of an image in /masks/, creates a black and white version of that
       image, using the given threshold, and places it in /temporal/."""

    im_path = dirname(abspath(__file__))
    print("------")
    print(im_path)
    Path(abspath('.') + '\\masks\\').mkdir(exist_ok = True)
    mask = Image.open(im_path + '\\masks\\' + image_path)

    fn = lambda x: 255 if x > threshold else 0

    mask = mask.convert('L').point(fn, mode='1')

    Path(abspath('.') + '\\temporal\\').mkdir(exist_ok = True)

    mask_path = im_path + '\\temporal\\' + Path(image_path).resolve().stem + "__mask.png"
    mask.save(mask_path)
    return mask
    

def make_camo(x, y, size, square_size = 5):
    BG_COLOUR = '#000000'
    canvas = Image.new("RGB", size, BG_COLOUR)
    draw1 = ImageDraw.Draw(canvas)

    def tile_board(start_x, start_y, squares, depth_prob = DEPTH_PROB, max_depth=MAX_DEPTH):
        for i in range(squares[0]):
            for j in range(squares[1]):
                draw_square(start_x + square_size*i, start_y + square_size*j, square_size, LAYERS)
                if random.random() <= depth_prob and max_depth:
                    tile_board(start_x + square_size*i, start_y + square_size*j, 
                               (1,1), depth_prob = depth_prob * 0.5, max_depth = max_depth-1)
    
    def draw_square(start_x, start_y, size, layers):
        randoms = [random.randrange(1, 4, 1) for l in range(layers)]
        sizes = sorted([r / sum(randoms) for r in randoms], reverse=True)
        ANCHORS = [(0, 0), #top left
                   (0, 1), #bottom left
                   (1, 0), #top right
                   (1, 1)] #bottom right
        anchor = random.choice(ANCHORS)

        anchor_x1 = start_x + anchor[0] * size
        anchor_y1 = start_y + anchor[1] * size

        anchor = (1 if (anchor[0] == 0) else -1, 1 if (anchor[1] == 0) else -1)

        colour = random.choice(COLOURS)
        #print("base colour is ", colour)
        draw1.rectangle((start_x, start_y, start_x + size, start_y +size), fill=colour) # base square
        for length in sizes:
            colour = random.choice(COLOURS)
            draw1.rectangle((anchor_x1, anchor_y1, 
                             anchor_x1 + (size * length * anchor[0]), anchor_y1 + (size * length * anchor[1])), fill=colour, outline="black")
            #print("(", str(anchor_x1), ",", str(anchor_y1), ") to (", str(anchor_x1 + (size * length * anchor[0])), ",", str(anchor_y1 + (size * length * anchor[1])) + ") coloured ", colour)

    no_squares = (ceil(size[0] / square_size), ceil(size[1] / square_size)) 
    tile_board(x, y, no_squares)
    #draw_square(0, 0, size, 3)

    data = np.array(canvas)
    
    data[(data == (255, 255, 255)).all(axis = -1)] = ImageColor.getrgb(SLIVER_COLOUR)

    canvas = Image.fromarray(data, mode='RGB')
    del draw1

    return canvas


image_path = "mario_stock.jpg"
mask = make_mask(image_path, threshold=125)

canvas = make_camo(0, 0, mask.size)

mask_info, canvas_info = np.array(mask), np.array(canvas)

print(mask_info)

print(canvas_info)

for x, y in np.ndindex(mask_info.shape):
    canvas_info[x][y] = canvas_info[x][y] if mask_info[x][y] else ImageColor.getrgb('#FF0000')

canvas = Image.fromarray(canvas_info, mode='RGB')

Path(abspath('.') + '\\output\\').mkdir(exist_ok = True)

canvas.save(dirname(abspath(__file__)) + "\\output\\" + Path(image_path).resolve().stem + "__output.png")


def show_image(image):
    window = tk.Tk()                   
    window.resizable(False, False)

    output = ImageTk.PhotoImage(image)
    panel = tk.Label(window, image=output)
    panel.pack(side="bottom", fill="both", expand="yes")
    window.mainloop()

show_image(canvas)