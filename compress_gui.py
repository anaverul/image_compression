from tkinter import Tk, StringVar, LabelFrame, Entry, Button
import tkinter as tk
from tkinter import filedialog
import os
import compress
from PIL import Image, ImageTk
from itertools import count, cycle

img = ''
root = Tk()
text_1 = StringVar()

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
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


def browse_image():
    global img
    global img_read
    filename = filedialog.askopenfilename(initialdir = os.getcwd(), title = "Browse Image File", filetypes = (("GIF Image", "*gif"), ("JPG Image", "*jpg"), ("PNG Image", "*png")))
    text_1.set(filename)
    img = filename

def pixelate_image():
    if img.endswith(".gif"):
        compress.gif_compressor(img)
        lbl.load("compressed.gif")
    else:
        compress.pixelate(img)
        lbl.load(img)

 
lbl = ImageLabel(root)
lbl.pack()

#----------------------------------------------------------------------------

wrapper = LabelFrame(root, text = "Source File")
wrapper.pack(fill = "both", expand = "yes", padx = 20, pady = 20)

label = LabelFrame(root, text = "Source File")
label.pack(side = tk.LEFT, padx = 10, pady = 10)

entry = Entry(wrapper, textvariable = text_1)
entry.pack(side = tk.LEFT, padx = 10, pady = 10)

button = Button(wrapper, text = "Browse", command = browse_image)
button.pack(side = tk.LEFT, padx=10, pady= 10)

#--------------------------------------------------------------------------
wrapper2 = LabelFrame(root, text = "Process")
wrapper2.pack(fill = "both", expand = "yes", padx = 20, pady = 20)

label2 = LabelFrame(root, text = "Process")
label2.pack(side = tk.LEFT, padx = 10, pady = 10)

button2 = Button(wrapper2, text = "Compress", command = pixelate_image)
button2.pack(side = tk.LEFT, padx=10, pady= 10)

root.title("Image compressor")
root.geometry("500x300")
root.mainloop()