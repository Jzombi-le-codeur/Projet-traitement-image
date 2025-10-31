import json
import pathlib
import os
import re
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
import copy


class UnsupportedFileError(Exception):
    def __init__(self, message):
        super.__init__(message)


class Support(Tk):
    def __init__(self):
        super().__init__()
        self.img_type = str()
        self.img_content = str()
        self.img_file_lines = list()
        self.formated_img_content = {"meta": dict(), "pix": list()}
        self.formated_images = list()
        self.img_to_display = None
        self.images_to_display = list()

    def __get_image_type(self, line: str) -> None:
        if line == "P1":
            self.img_type = "pbm"

        elif line == "P2":
            self.img_type = "pgm"

        elif line == "P3":
            self.img_type = "ppm"

        else:
            raise UnsupportedFileError("Ce format de fichier n'est pas supporté.")

    def __format_img_file(self, filename: str | pathlib.Path) -> None:
        # Metadonnées
        self.formated_img_content["meta"]["title"] = str(pathlib.Path(os.path.basename(filename)).stem)
        self.formated_img_content["meta"]["extension"] = str(pathlib.Path(os.path.basename(filename)).suffix)
        self.formated_img_content["meta"]["col"] = int(self.img_file_lines[1])
        self.formated_img_content["meta"]["lig"] = int(self.img_file_lines[2])
        self.formated_img_content["meta"]["mod"] = str

        # Données
        # Supprimer les métadonnées des données
        n_line = 0
        line_limit_meta = 3 if self.img_type == "pbm" else 4
        for line in self.img_file_lines[:]:
            n_line += 1
            if n_line <= line_limit_meta:
                self.img_content = self.img_content.removeprefix(f"{line}\n")
                self.img_file_lines.remove(line)

            else:
                break

        # Formater les données
        if self.img_type != "ppm":
            formated_datas = []
            for line in self.img_file_lines:
                formated_line = re.split(' +', line)
                formated_datas.append(formated_line)

            # PEUT ETRE REVOIR REFORMATAGE SI 1 LIGNE FICHIER PAS EGAL A LIGNE IMAGE
            self.formated_img_content["pix"] = formated_datas

        else:
            formated_datas = []
            for line in self.img_file_lines:
                # Récupérer les valeurs de chaque couleur
                # line_codes = re.split(' +', line)
                line_codes = [c for c in line.split() if c]

                # Récupérer les couleurs de chaque pixel
                line_pixels = []
                i = 0
                px = []
                for i, code in enumerate(line_codes):
                    code = int(code)
                    if i%3 == 0 and i != 0:
                        # Sauver le pixel
                        line_pixels.append(tuple(px))

                        # Récupérer un nouveau pixel
                        px = []

                    # Mettre à jour le pixel
                    px.append(code)
                    i += 1

                # Ajouter un pixel s'il en reste
                if px:
                    line_pixels.append(tuple(px))

                # Ajouter la ligne aux données de l'image
                formated_datas.append(line_pixels)

            self.formated_img_content["pix"] = formated_datas

    def open(self, filename: str | pathlib.Path) -> dict:
        # Ouvrir le fichier
        with open(filename) as img_file:
            self.img_content = img_file.read()
            self.img_file_lines = self.img_content.split(sep="\n")

        # Vérifier le format du fichier
        self.__get_image_type(line=self.img_file_lines[0])

        # Formater le fichier
        self.__format_img_file(filename=filename)

        return self.formated_img_content

    def __create_image(self, image: dict, ratio: int = 1) -> None:
        if self.img_type == "pbm":
            image_pxs = np.array(image["pix"], dtype=np.uint8)
            image_pxs[image_pxs == 1] = 255
            image_pxs = np.repeat(image_pxs[..., np.newaxis], repeats=3, axis=2)

            image_pixels = np.repeat(np.repeat(image_pxs, repeats=ratio, axis=1), repeats=ratio, axis=0)
            self.img_to_display = Image.fromarray(image_pixels, mode="RGB")

        elif self.img_type == "pgm":
            image_pxs = np.array(image["pix"], dtype=np.uint8)
            image_pxs = np.repeat(image_pxs[..., np.newaxis], repeats=3, axis=2)

            image_pixels = np.repeat(np.repeat(image_pxs, repeats=ratio, axis=1), repeats=ratio, axis=0)
            self.img_to_display = Image.fromarray(image_pixels, mode="RGB")

        else:
            image_pxs = np.array(image["pix"], dtype=np.uint8)
            image_pixels = np.repeat(np.repeat(image_pxs, repeats=ratio, axis=1), repeats=ratio, axis=0)
            self.img_to_display = Image.fromarray(image_pixels, mode="RGB")

    def __display_image(self) -> None:
        self.title("image")

        image_label = Label(self, image=self.img_to_display)
        image_label.pack()

        self.mainloop()

    def show(self, img: dict) -> None:
        self.__create_image(image=img, ratio=20)
        self.__display_image()

    def compare(self, imgs: list):
        images = list()
        for img in imgs:
            self.__create_image(image=img, ratio=20)
            images.append(ImageTk.PhotoImage(self.img_to_display))

        self.images_to_display = images

        self.title("test")
        image1 = Label(self, image=images[0])
        image1.grid(column=1, row=1, padx=10)
        image2 = Label(self, image=images[1])
        image2.grid(column=2, row=1, padx=10)

        self.mainloop()


if __name__ == "__main__":
    support = Support()
    imgs_paths = [pathlib.Path("images\\salva.pbm"), pathlib.Path("images\\salva.ppm")]
    images = list()
    for i in imgs_paths:
        img = support.open(filename=i)
        images.append(img)

    support.compare(imgs=images)
