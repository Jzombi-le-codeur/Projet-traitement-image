from copy import deepcopy
from support import Support
import numpy as np
import json
from scipy.ndimage import rotate


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
        print(file_conversion)
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

        print(img["meta"])
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
        img_pxs = np.array(img["pix"], dtype=np.uint8)

        if img["meta"]["extension"] == ".ppm":
            """ Stretch la largeur """
            i = img_pxs.shape[1] % ratio
            cols = img_pxs.shape[1] - i
            img_pxs_first = img_pxs[:, :cols, :]
            img_pxs_first = np.reshape(img_pxs_first, (img_pxs_first.shape[0], img_pxs_first.shape[1] // ratio, ratio, 3))
            img_pxs_first = np.mean(img_pxs_first, axis=-2)
            img_pxs_first = img_pxs_first.astype(int)
            last_col = img_pxs[:, cols:, :]
            """
            if i > 0:
                img_pxs = np.concatenate([img_pxs_first, last_col], axis=1)
    
            else:
            """
            img_pxs = img_pxs_first

            """ Hauteur """
            img_pxs = np.rot90(img_pxs, k=-1)
            i = img_pxs.shape[1] % ratio
            cols = img_pxs.shape[1] - i
            img_pxs_first = img_pxs[:, :cols, :]
            img_pxs_first = np.reshape(img_pxs_first, (img_pxs_first.shape[0], img_pxs_first.shape[1] // ratio, ratio, 3))
            img_pxs_first = np.mean(img_pxs_first, axis=-2)
            img_pxs_first = img_pxs_first.astype(int)
            last_col = img_pxs[:, cols:, :]
            """
            if i > 0:
                img_pxs = np.concatenate([img_pxs_first, last_col], axis=1)
    
            else:
            """
            img_pxs = img_pxs_first

            img_pxs = np.rot90(img_pxs, k=1)

        elif img["meta"]["extension"] == ".pgm" or img["meta"]["extension"] == ".pbm":
            if img["meta"]["extension"] == ".pbm":
                img_pxs[img_pxs == 1] = 255

            i = img_pxs.shape[1] % ratio
            cols = img_pxs.shape[1] - i
            img_pxs_first = img_pxs[:, :cols]
            img_pxs_first = np.reshape(img_pxs_first,
                                       (img_pxs_first.shape[0], img_pxs_first.shape[1] // ratio, ratio))
            img_pxs_first = np.mean(img_pxs_first, axis=-1)
            img_pxs_first = img_pxs_first.astype(int)
            img_pxs = img_pxs_first

            img_pxs = np.rot90(img_pxs, k=-1)
            i = img_pxs.shape[1] % ratio
            cols = img_pxs.shape[1] - i
            img_pxs_first = img_pxs[:, :cols]
            img_pxs_first = np.reshape(img_pxs_first,
                                       (img_pxs_first.shape[0], img_pxs_first.shape[1] // ratio, ratio))
            img_pxs_first = np.mean(img_pxs_first, axis=-1)
            img_pxs_first = img_pxs_first.astype(int)
            img_pxs = img_pxs_first
            img_pxs = np.rot90(img_pxs, k=1)

            if img["meta"]["extension"] == ".pbm":
                img_pxs[img_pxs < 128] = 0
                img_pxs[img_pxs >= 128] = 1

        img["pix"] = img_pxs
        img["meta"]["col"] = img_pxs.shape[1]
        img["meta"]["lig"] = img_pxs.shape[0]
        img["meta"]["mod"] = "\n- Taille réduite"
        return img

    def change_rgb(self, img: dict, rgb: tuple[int | None, int | None, int | None]) -> dict:
        img = deepcopy(img)
        if img["meta"]["extension"] == ".ppm":
            img_pxs = np.array(img["pix"], dtype=np.uint8)
            print(img_pxs)
            print(img_pxs.shape)
            r, g, b = rgb
            if r:
                gb = 1-(r/100)
                r = 1+(r/100)
                img_pxs[:, :, 0] = np.clip(img_pxs[:, :, 0]*r, 0, 255)
                # img_pxs[:, :, 1] = np.clip(img_pxs[:, :, 1]*gb, 0, 255)
                # img_pxs[:, :, 2] = np.clip(img_pxs[:, :, 2]*gb, 0, 255)
                
            if g:
                rb = 1-(g/100)
                g = 1+(g/100)
                # img_pxs[:, :, 0] = np.clip(img_pxs[:, :, 0]*rb, 0, 255)
                img_pxs[:, :, 1] = np.clip(img_pxs[:, :, 1]*g, 0, 255)
                # img_pxs[:, :, 2] = np.clip(img_pxs[:, :, 2]*rb, 0, 255)
                
            if b:
                rg = 1-(b/100)
                b = 1+(b/100)
                # img_pxs[:, :, 0] = np.clip(img_pxs[:, :, 0]*rg, 0, 255)
                # img_pxs[:, :, 1] = np.clip(img_pxs[:, :, 1]*rg, 0, 255)
                img_pxs[:, :, 2] = np.clip(img_pxs[:, :, 2]*b, 0, 255)

            img["pix"] = img_pxs
            img["mod"] = "\n- Changement de couleur"

        return img

    def rotate(self, img: dict, angle: int) -> dict:
        img = deepcopy(img)
        img_pxs = np.array(img["pix"], dtype=np.uint8)
        img["pix"] = rotate(img_pxs, angle=angle)
        img["meta"]["mod"] = "\n- Rotation"
        return img
