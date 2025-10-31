from tkinter import *
from PIL import Image, ImageTk


image = Image.new(mode="RGB", size=(300, 300), color="blue")

fen = Tk()

fen.geometry("310x310")

img = ImageTk.PhotoImage(image=image)
label = Label(fen, image=img)
label.grid(row=0, column=0, padx=5, pady=5)

fen.mainloop()
