"""This file contains everything relating to the user interface.

    Right now, it's pretty bare - however, if the user interface is expanded upon later in
    development, this is where it'll go."""

import tkinter as tk
from PIL import ImageTk

def show_image(image):
    """Given an Image (from PIL), opens a Tkinter window containing said image.

       This window currently contains no functionality beyond showing the image,
       but more functionality may be added in the future.
    """
    window = tk.Tk()                   
    window.resizable(False, False)

    output = ImageTk.PhotoImage(image)
    panel = tk.Label(window, image=output)
    panel.pack(side="bottom", fill="both", expand="yes")
    window.mainloop()
