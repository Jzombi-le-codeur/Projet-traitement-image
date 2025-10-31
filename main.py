import pathlib
from tkinter import *
from support import Support
from pathlib import Path
import json


class Win(Tk):
    def __init__(self):
        super().__init__()
        self.support = Support()
        self.resolution = (1024, 576)
        self.imgs = []

    def open_image(self, filename: str | pathlib.Path):
        image = self.support.open(filename=filename)
        self.imgs.append(image)
        print(self.imgs)

    def init_informations(self):
        # Titre fenêtre
        self.title("Projet Traitement Image")

        # Résolution fenêtre
        self.geometry(f"{str(self.resolution[0])}x{str(self.resolution[1])}")

    def manage_win(self):
        # Informations fenêtres
        self.init_informations()
        self.open_image(filename=pathlib.Path(r"images\\salva.ppm"))
        self.mainloop()

if __name__ == "__main__":
    Win().manage_win()
