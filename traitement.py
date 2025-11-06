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
        col = img["meta"]["col"]
        lig = img["meta"]["lig"]
        img["meta"]["col"] = lig
        img["meta"]["lig"] = col
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

    def increase_size(self, img: dict, ratio: int) -> dict:
        img = deepcopy(img)
        if img["meta"]["extension"] == ".pbm":
            image_pxs = np.array(img["pix"], dtype=np.uint8)
            image_pixels = np.repeat(np.repeat(image_pxs, repeats=ratio, axis=1), repeats=ratio, axis=0)

        elif img["meta"]["extension"] == ".pgm":
            image_pxs = np.array(img["pix"], dtype=np.uint8)
            image_pixels = np.repeat(np.repeat(image_pxs, repeats=ratio, axis=1), repeats=ratio, axis=0)

        elif img["meta"]["extension"] == ".ppm":
            image_pxs = np.array(img["pix"], dtype=np.uint8)
            image_pixels = np.repeat(np.repeat(image_pxs, repeats=ratio, axis=1), repeats=ratio, axis=0)

        img["pix"] = image_pixels

        img["meta"]["lig"] = str(int(img["meta"]["lig"])*int(ratio))
        img["meta"]["col"] = str(int(img["meta"]["col"])*int(ratio))
        img["meta"]["mod"] = "Image aggrandie"

        return img

    def decrease_size(self, img: dict, ratio: int) -> dict:
        img = deepcopy(img)
        print(img["meta"])
        img_pxs = np.array(img["pix"], dtype=np.uint8)
        if len(img_pxs)%2 == 1:
            img_pxs_first = img_pxs[:, :-1, :]

        else:
            img_pxs_first = img_pxs

        img_pxs_first = np.reshape(img_pxs_first, (img_pxs_first.shape[0], img_pxs_first.shape[1] // 2, 2, 3))
        img_pxs_first = np.mean(img_pxs_first, axis=-2)
        img_pxs_first = img_pxs_first.astype(int)
        last_col = img_pxs[:, -1, :]
        if len(img_pxs) % 2 == 1:
            img_pxs = np.concatenate([img_pxs_first, last_col[:, np.newaxis, :]], axis=1)

        else:
            img_pxs = img_pxs_first

        img["pix"] = img_pxs
        print(img_pxs.shape)
        img["meta"]["col"] = img_pxs.shape[1]
        img["meta"]["lig"] = img_pxs.shape[0]
        img["meta"]["mod"] = "\n- Taille réduite"
        return img
