import pathlib
import os
from tkinter import *
from PIL import Image, ImageTk
import numpy as np


class UnsupportedFileError(Exception):
    def __init__(self, message):
        super.__init__(message)


class Support():
    def __init__(self, win: Toplevel | None = None):
        self.win = win
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
        self.formated_img_content["meta"]["mod"] = str()

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
                # formated_line = re.split(' +', line)
                formated_line = [int(val) for val in line.split() if val]
                formated_datas.append(formated_line)

            # PEUT ETRE REVOIR REFORMATAGE SI 1 LIGNE FICHIER PAS EGAL A LIGNE IMAGE
            # self.formated_img_content["pix"] = formated_datas

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

            # self.formated_img_content["pix"] = formated_datas

        # Vérifier qu'aucune ligne n'est vide
        formated_datas_arr = np.array(formated_datas, dtype=object)
        formated_datas_arr = formated_datas_arr[np.array([len(row) > 0 for row in formated_datas_arr])]
        self.formated_img_content["pix"] = formated_datas_arr.tolist()


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

    def __calculate_ratio(self, image: dict) -> int:
        max_lines_px = 720
        max_height_px = 1280

        img_lines_px = image["meta"]["lig"]
        img_height_px = image["meta"]["col"]

        ratio = 0
        while True:
            ratio += 1
            if img_lines_px*ratio > max_lines_px or img_height_px*ratio > max_height_px:
                break

        return ratio

    def create_image(self, image: dict, ratio: int = 1) -> None:
        ratio = self.__calculate_ratio(image=image)/ratio
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

        return self.img_to_display

    def display_image(self, image: Image) -> None:
        self.win.title("image")

        image = ImageTk.PhotoImage(image)
        image_label = Label(self.win, image=image)
        image_label.image = image
        image_label.pack()

    def compare(self, imgs: list):
        image_to_display = ImageTk.PhotoImage(imgs[0])
        image2_to_display = ImageTk.PhotoImage(imgs[1])

        self.win.title("test")
        image1 = Label(self.win, image=image_to_display)
        image1.image = image_to_display
        image1.grid(column=1, row=1, padx=10)
        image2 = Label(self.win, image=image2_to_display)
        image2.image = image2_to_display
        image2.grid(column=2, row=1, padx=10)


if __name__ == "__main__":
    win = Tk()
    support = Support(win=win)
    imgs_paths = [pathlib.Path("images\\salva.pbm"), pathlib.Path("images\\salva.ppm")]
    images = list()
    for i in imgs_paths:
        support_i = Support(win=win)
        img = support_i.open(filename=i)
        img = support_i.create_image(image=img)
        images.append(img)

    support.compare(imgs=images)
