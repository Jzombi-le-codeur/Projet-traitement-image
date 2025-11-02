from copy import deepcopy
from support import Support
import numpy as np


class Traitement:
    def __init__(self):
        self.support = Support()

    def symVert(self, img: dict, local=False) -> dict:
        img = deepcopy(img)
        img_pxs = np.array(img["pix"], dtype=np.uint8)
        img_pxs = img_pxs[::-1]
        img["pix"] = img_pxs
        if not local:
            img["meta"]["mod"] = "\n- Symétrie Horizontale"
        return img

    def symHori(self, img: dict, local=False) -> dict:
        img = deepcopy(img)
        img_pxs = np.array(img["pix"], dtype=np.uint8)
        img_pxs = img_pxs[:, ::-1]
        img["pix"] = img_pxs
        if not local:
            img["meta"]["mod"] = "\n- Symétrie Horizontale"
        return img

    def rot180(self, img: dict) -> dict:
        process_img = deepcopy(img)
        process_img = self.symVert(process_img, local=True)  # verticale
        process_img = self.symHori(process_img, local=True)  # horizontale
        process_img["meta"]["mod"] = "\n- Rotation 180°"
        return process_img

    def rot90(self, img: dict) -> dict:
        img = deepcopy(img)
        img_pxs = np.array(img["pix"], dtype=np.uint8)
        img_pxs = np.rot90(img_pxs, k=-1)
        img["pix"] = img_pxs
        img["meta"]["mod"] = "\n- Rotation 90°"
        return img

    def convert_to_grey_mode(self, img: dict, file_conversion, local=False) -> dict:
        if file_conversion:
            img = deepcopy(img)
            if img["meta"]["extension"] == ".ppm":
                img_pxs = np.array(img["pix"], dtype=np.uint8)
                # img_pxs[:, :] = np.mean(img_pxs, axis=2).astype(np.uint8)
                img_pxs = np.mean(img_pxs, axis=2).astype(np.uint8)
                img["pix"] = img_pxs

            elif img["meta"]["extension"] == ".pbm":
                img_pxs = np.array(img["pix"], dtype=np.uint8)
                img_pxs[img_pxs == 1] = 255
                img["pix"] = img_pxs

            img["meta"]["extension"] = ".pgm"

        else:
            if img["meta"]["extension"] == ".ppm":
                img = deepcopy(img)
                img_pxs = np.array(img["pix"], dtype=np.uint8)
                img_pxs = np.mean(img_pxs, axis=2, keepdims=True)
                img_pxs = np.repeat(img_pxs, repeats=3, axis=2)
                img["pix"] = img_pxs

            if local:
                if img["meta"]["extension"] == ".pbm":
                    img_pxs = np.array(img["pix"], dtype=np.uint8)
                    img_pxs[img_pxs == 1] = 255
                    img["pix"] = img_pxs

                elif img["meta"]["extension"] == ".ppm":
                    img_pxs = np.array(img["pix"], dtype=np.uint8)
                    img_pxs = np.mean(img_pxs, axis=2).astype(np.uint8)
                    img["pix"] = img_pxs

                elif img["meta"]["extension"] == ".pbm":
                    img_pxs = np.array(img["pix"], dtype=np.uint8)
                    img_pxs[img_pxs == 1] = 255
                    img["pix"] = img_pxs


        if not local:
            img["meta"]["mod"] = "\n- Converti en niveaux de gris"

        return img

    def convert_to_bw_mode(self, img: dict, file_conversion: bool) -> dict:
        if img["meta"]["extension"] != ".pbm":
            img = deepcopy(img)
            img = self.convert_to_grey_mode(img=img, local=True, file_conversion=False)
            img_pxs = np.array(img["pix"], dtype=np.uint8)

            seuil = 128
            img_pxs[img_pxs < seuil] = 0
            if not file_conversion:
                img_pxs[img_pxs >= seuil] = 255

            else:
                img_pxs[img_pxs >= seuil] = 1
                img["meta"]["extension"] = ".pgm"

            img["pix"] = img_pxs

        img["meta"]["mod"] = "\n- Converti en noir et blanc"

        return img

    def change_brightness(self, img: dict, t: int) -> dict:
        if img["meta"]["extension"] != ".pbm":
            img = deepcopy(img)
            img_pxs = np.array(img["pix"], dtype=np.uint8)
            # img_pxs = 255*(img_pxs/255)**(1+(t/100))
            img_pxs = img_pxs*(1+(t/100))
            img_pxs = np.clip(img_pxs, 0, 255)
            img["pix"] = img_pxs

        if t < 0:
            img["meta"]["mod"] = "\n- Luminosité diminuée"

        elif t > 0:
            img["meta"]["mod"] = "\n- Luminosité augmentée"

        return img
