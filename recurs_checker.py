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
    "Digital Camo": (['#007400', '#006600', '#005600'], '#00AF00'),

    "Magma Bubbles": (['#740000', '#660000', '#560000', '#210000', '#DD5812', '#DD5830'], '#AF0000'),

    "Drowning": (['#000074', '#000066', '#000056', '#000021'], '#0000AF'),

    "Retro": (['#7851a9','#1034a6','#0087bd', '#c40233', '#ffd300'], '#000000'),

    "Google": (['#008744', '#0057e7', '#d62d20', '#ffa700'], '#ffffff'),

    "Basic": (['#444444', '#666666', '#888888', '#AAAAAA',], '#EEEEEE'),

    "Umbra Witch": (['#555566', '#333344', '#444455', '#334455', '#9988aa'], '#444455'),
}

CHOSEN_PALETTE = "Basic"

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

def make_mask(image_path, threshold=200, inverse = False):
    """Given the filename of an image in /masks/, creates a black and white version of that
       image, using the given threshold, and places it in /temporal/."""

    im_path = dirname(abspath(__file__))
    Path(abspath('.') + '\\masks\\').mkdir(exist_ok = True)
    mask = Image.open(im_path + '\\masks\\' + image_path)

    Path(abspath('.') + '\\temporal\\').mkdir(exist_ok = True)

    if inverse:
        mask_end = "i_mask.png"
    else:
        mask_end = "__mask.png"

    mask_path = im_path + '\\temporal\\' + Path(image_path).resolve().stem + mask_end

    if os.path.isfile(mask_path):
        # Don't make a mask if we already have one with that name
        mask = Image.open(mask_path)
    else:
        if inverse:
            fn = lambda x: 255 if not (x > threshold) else 0
        else:
            fn = lambda x: 255 if (x > threshold) else 0
        mask = mask.convert('L').point(fn, mode='1')
        mask.save(mask_path)
    return mask
    

def make_camo(x, y, size, square_size = 10):
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
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
    
    data[(data == (255, 255, 255, 255)).all(axis = -1)] = ImageColor.getcolor(SLIVER_COLOUR, 'RGBA')

    canvas = Image.fromarray(data, mode='RGBA')
    del draw1

    return canvas


image_path = "nu_13_i_think.jpg"
mask_a = make_mask(image_path, threshold=100, inverse=False)

mask_b = make_mask(image_path, threshold=100, inverse=True)

canvas = make_camo(0, 0, mask_a.size)



mask_info, canvas_info = np.array(mask_a), np.array(canvas)

for x, y in np.ndindex(mask_info.shape):
    canvas_info[x][y] = canvas_info[x][y] if not mask_info[x][y] else (0, 0, 0, 0)

canvas = Image.fromarray(canvas_info, mode='RGBA')

CHOSEN_PALETTE = "Drowning"

try:
    COLOURS, SLIVER_COLOUR = palettes[CHOSEN_PALETTE]
except KeyError:
    COLOURS, SLIVER_COLOUR = ([random_colour() for i in range(5)], random_colour())
    print("Palette not found, using random colours...")
    print(COLOURS)
    print(SLIVER_COLOUR)

canvas_i = make_camo(0, 0, mask_b.size)


mask_info, canvas_info = np.array(mask_b), np.array(canvas_i)

for x, y in np.ndindex(mask_info.shape):
    canvas_info[x][y] = canvas_info[x][y] if not mask_info[x][y] else (0, 0, 0, 0)

canvas_i = Image.fromarray(canvas_info, mode='RGBA')

canvas.paste(canvas_i, mask=canvas_i)

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