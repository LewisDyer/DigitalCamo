"""This file handles actions relating to masks - for example, creating masks, saving them,
   checking for their existence, and so on.
"""

from PIL import Image
from pathlib import Path
from os.path import abspath, dirname, isfile

def make_mask(image_path, threshold=200, inverse = False):
    """Given the filename of an image in /masks/, creates a black and white version of that
       image, using the given threshold, and places it in /temporal/."""

    im_path = dirname(abspath(__file__)) # get base dir
    Path(abspath('.') + '\\masks\\').mkdir(exist_ok = True) # create /masks/ if not exist
    mask = Image.open(im_path + '\\masks\\' + image_path) # find mask in /masks/

    Path(abspath('.') + '\\temporal\\').mkdir(exist_ok = True) # make /temporal/ if not exist

    if inverse:
        mask_end = "i_mask.png" # define prefixes for inverse/regular mask
    else:
        mask_end = "__mask.png"

   # where the mask will go if we create it
    mask_path = im_path + '\\temporal\\' + Path(image_path).resolve().stem + mask_end

    if isfile(mask_path):
        # Don't make a mask if we already have one with that name
        mask = Image.open(mask_path)
    else:
        if inverse:
            fn = lambda x: 255 if not (x > threshold) else 0 # mask light sections
        else:
            fn = lambda x: 255 if (x > threshold) else 0 # mask dark sections
        mask = mask.convert('L').point(fn, mode='1') # convert to grayscale
        mask.save(mask_path)
    return mask