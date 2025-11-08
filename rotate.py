import json
import numpy as np
from PIL import Image
from scipy.ndimage import rotate

# # --- Initialisation ---
# angle = 45
# angle = np.radians(angle)
#
# with open(r"C:\Users\nicot\Documents\img.json", "r") as fp:
#     image = json.load(fp)
#
# arr = np.array(image, dtype=np.uint8)
# h, w = arr.shape[:2]
#
# # --- Nouvelle résolution (en entiers) ---
# new_h = int(abs(h * np.cos(angle)) + abs(w * np.sin(angle)))
# new_w = int(abs(h * np.sin(angle)) + abs(w * np.cos(angle)))
#
# # --- Matrice de rotation ---
# rotation_arr = np.array([
#     [np.cos(angle), -np.sin(angle)],
#     [np.sin(angle), np.cos(angle)]
# ])
#
# # --- Points de rotation (centres) ---
# orig_cx, orig_cy = w / 2, h / 2
# new_cx, new_cy = new_w / 2, new_h / 2
#
# # --- Nouvelle image vide ---
# img = np.zeros((new_h, new_w, 3), dtype=np.uint8)
#
# # --- Application de la rotation ---
# for y in range(h):
#     for x in range(w):
#         # coordonnées centrées par rapport à l’image originale
#         px_pos = np.array([x - orig_cx, y - orig_cy])
#
#         # rotation
#         new_xy = np.dot(rotation_arr, px_pos)
#         new_x = int(new_cx + new_xy[0])
#         new_y = int(new_cy + new_xy[1])
#
#         # vérification des limites
#         if 0 <= new_x < new_w and 0 <= new_y < new_h:
#             img[new_y, new_x] = arr[y, x]
#
# # --- Affichage ---
# Image.fromarray(img).show()


with open(r"C:\Users\nicot\Documents\img.json", "r") as fp:
    image = json.load(fp)

arr = np.array(image, dtype=np.uint8)
arr = rotate(arr, angle=45)

img = Image.fromarray(arr)
img.show()
