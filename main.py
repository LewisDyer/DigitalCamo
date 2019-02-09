"""This file contains the main program loop. If you want a high-level overview of the program,
   this is the place to look!

   Run this file if you want to run the actual program.
"""

import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from pathlib import Path
from os.path import abspath, dirname

import camo, masks, ui, user_config

params = user_config.parameters

mask_a = masks.make_mask(params['filename'], params['threshold'], inverse=False)

mask_b = masks.make_mask(params['filename'], params['threshold'], inverse=True)

canvas = camo.make_camo(0, 0, mask_a.size, **params['foreground'])

mask_info, canvas_info = np.array(mask_a), np.array(canvas)

for x, y in np.ndindex(mask_info.shape):
    canvas_info[x][y] = canvas_info[x][y] if not mask_info[x][y] else (0, 0, 0, 0)

canvas = Image.fromarray(canvas_info, mode='RGBA')

canvas_i = camo.make_camo(0, 0, mask_b.size, **params['background'])


mask_info, canvas_info = np.array(mask_b), np.array(canvas_i)

for x, y in np.ndindex(mask_info.shape):
    canvas_info[x][y] = canvas_info[x][y] if not mask_info[x][y] else (0, 0, 0, 0)

canvas_i = Image.fromarray(canvas_info, mode='RGBA')

canvas.paste(canvas_i, mask=canvas_i)

Path(abspath('.') + '\\output\\').mkdir(exist_ok = True)

canvas.save(dirname(abspath(__file__)) + "\\output\\" + Path(params['filename']).resolve().stem + "__output.png")

ui.show_image(canvas)