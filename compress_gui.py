from tkinter import Tk, StringVar, LabelFrame, Entry, Button
import tkinter as tk
from tkinter import filedialog
import os
import compress
from PIL import Image, ImageTk
from itertools import count, cycle

img = '' #image to be processed
root = Tk() #initializing root
display_text = StringVar()

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image = None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image = next(self.frames))
            self.after(self.delay, self.next_frame)


def browse_image():
    """lets the user browse and pick an image file
    Accepted extensions are: .jpg, .png, .gif

    Parameters
    ----------
    No parameters
    Returns
    -------
    No returns
    """
    global img
    global img_read
    filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Browse Image File", filetypes = (("GIF Image", "*gif"), ("JPG Image", "*jpg"), ("PNG Image", "*png")))
    display_text.set(filename)
    img = filename

def pixelate_image():
    """pixelates image selected by user

    Parameters
    ----------
    No parameters
    Returns
    -------
    No returns
    """
    if img.endswith(".gif"):
        compress.gif_compressor(img)
        display_image_label.load("compressed.gif")
    else:
        compress.pixelate(img)
        display_image_label.load(img)


display_image_label = ImageLabel(root)
display_image_label.pack()

#----------------------------------------------------------------------------

wrapper_source_file = LabelFrame(root, text = "Source File")
wrapper_source_file.pack(fill = "both", expand = "yes", padx = 20, pady = 20)

label_source_file = LabelFrame(root, text = "Source File")
label_source_file.pack(side = tk.LEFT, padx = 10, pady = 10)

entry_source_file = Entry(wrapper_source_file, textvariable = display_text)
entry_source_file.pack(side = tk.LEFT, padx = 10, pady = 10)

button_source_file = Button(wrapper_source_file, text = "Browse", command = browse_image)
button_source_file.pack(side = tk.LEFT, padx=10, pady= 10)

#--------------------------------------------------------------------------
wrapper_compressing = LabelFrame(root, text = "Process")
wrapper_compressing.pack(fill = "both", expand = "yes", padx = 20, pady = 20)

label_compressing = LabelFrame(root, text = "Process")
label_compressing.pack(side = tk.LEFT, padx = 10, pady = 10)

button_compressing = Button(wrapper_compressing, text = "Compress", command = pixelate_image)
button_compressing.pack(side = tk.LEFT, padx=10, pady= 10)

root.title("Image compressor")
root.geometry("500x300")
root.mainloop()
