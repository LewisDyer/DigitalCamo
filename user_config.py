"""This file contains everything relating to user input - for instance, choosing an
   image to mask, or setting various parameters in camo generation.

   Most users should only make changes in this file.    
"""

import random

parameters = {}

parameters['filename'] = "persona5.jpeg"

parameters['threshold'] = 150

parameters['background'] = {
   'palette': 'Persona 5',
   'square_size': 50,
   'max_depth': 4,
   'depth_prob': 0.6,
   'layers':10,
}

parameters['foreground'] = {
   'palette': 'Pop Black',
   'square_size': 15,
   'max_depth': 4,
   'depth_prob': 0.6,
   'layers':4,
}


palettes = {
    "Digital Camo": (['#007400', '#006600', '#005600'], '#00AF00'),

    "Magma Bubbles": (['#740000', '#660000', '#560000', '#210000', '#DD5812', '#DD5830'], '#AF0000'),

    "Drowning": (['#000074', '#000066', '#000056', '#000021'], '#0000AF'),

    "Retro": (['#7851a9','#1034a6','#0087bd', '#c40233', '#ffd300'], '#000000'),

    "Google": (['#008744', '#0057e7', '#d62d20', '#ffa700'], '#ffffff'),

    "Basic": (['#444444', '#666666', '#888888', '#AAAAAA',], '#EEEEEE'),

    "Umbra Witch": (['#555566', '#333344', '#444455', '#334455', '#9988aa'], '#444455'),

    "Persona 5": (['#F90100', '#C51C09', '#AD180A', '#390902'], '#000000'),

    "Pop Black": (['#000000', '#323232', '#222222'], '#000000'),
}

def random_colour():
    # generates a random hex colour code
    return "#" + "%06x" % random.randint(0, 0xFFFFFF)

def get_palette(palette_name):

   try:
      colours, outline_colour = palettes[palette_name]
   except KeyError:
      colours, outline_colour = ([random_colour() for i in range(5)], random_colour())
      print("Palette not found, using random colours...")

   
   return (colours, outline_colour)


