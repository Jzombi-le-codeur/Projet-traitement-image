import pathlib
from tkinter import *
from support import Support
from traitement import Traitement
from tkinter import messagebox


class Win(Tk):
    def __init__(self):
        super().__init__()
        self.n_wins = 16
        self.wins = [None]*self.n_wins
        self.wins_opened = [False]*self.n_wins
        self.resolution = (1024, 576)
        self.imgs = []

        self.traitement = Traitement()
        self.file_conversion = True

    def close_win(self, img_id):
        if self.wins[img_id - 1]:
            self.wins[img_id - 1].destroy()
        self.wins[img_id - 1] = None
        if img_id == 1:
            self.show_img_1_button["text"] = "Afficher"

        elif img_id == 2:
            self.show_img_2_button["text"] = "Afficher"

        elif img_id == 3:
            self.compare_button["text"] = "Comparer"

        self.wins_opened[img_id - 1] = False

    def show_image(self, filename: str | pathlib.Path, img_id: int):
        try:
            if self.wins_opened[img_id-1]:
                self.close_win(img_id=img_id)

            else:
                self.wins[img_id-1] = Toplevel()
                win = self.wins[img_id-1]
                support = Support(win=win)
                image_opened = support.open(filename=filename)
                image = support.create_image(image=image_opened)
                support.display_image(image)
                self.wins_opened[img_id-1] = True
                if img_id == 1:
                    self.show_img_1_button["text"] = "Fermer"

                else:
                    self.show_img_2_button["text"] = "Fermer"
                win.protocol("WM_DELETE_WINDOW", lambda: self.close_win(img_id=img_id))

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=img_id)

    def compare_image(self, filenames: list, img_id: int = 3):
        try:
            if self.wins_opened[2]:
                self.close_win(img_id=img_id)
            else:
                self.wins[2] = Toplevel()
                win = self.wins[img_id - 1]
                support = Support(win=win)
                images = []
                for f in filenames:
                    support_i = Support(win=win)
                    img = support_i.open(filename=f)
                    img = support_i.create_image(image=img, ratio=2)
                    images.append(img)

                support.compare(imgs=images)

                self.wins_opened[2] = True
                self.compare_button["text"] = "Fermer"
                win.protocol("WM_DELETE_WINDOW", lambda: self.close_win(img_id=img_id))

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=img_id)

    def init_informations(self):
        # Titre fenêtre
        self.title("Projet Traitement Image")

        # Résolution fenêtre
        self.geometry(f"{str(self.resolution[0])}x{str(self.resolution[1])}")

    def create_form(self):
        self.img_1_path_entry = Entry(self, width=40)
        self.img_1_path_entry.pack()
        self.show_img_1_button = Button(self, text="Afficher",
                                        command=lambda: self.show_image(filename=self.img_1_path_entry.get(),
                                                                        img_id=1))
        self.show_img_1_button.pack()

        self.img_2_path_entry = Entry(self, width=40)
        self.img_2_path_entry.pack()
        self.show_img_2_button = Button(self, text="Afficher",
                                        command=lambda: self.show_image(filename=self.img_2_path_entry.get(),
                                                                        img_id=2))
        self.show_img_2_button.pack()

        self.compare_button = Button(self, text="Comparer", command=lambda: self.compare_image(
            filenames=[self.img_1_path_entry.get(), self.img_2_path_entry.get()]
        ))
        self.compare_button.pack()

    def create_filter_buttons(self):
        self.symvert_button = Button(self, text="Symétrie Verticale", command=lambda: self.symVert())
        self.symvert_button.pack()

        self.symhori_button = Button(self, text="Symétrie Horizontale", command=lambda: self.symHori())
        self.symhori_button.pack()

        self.rotate_frame = Frame(self)
        self.rotate_frame.pack()
        self.rotate_button = Button(self.rotate_frame, text="Rotation",
                                        command=lambda: self.rotate())
        self.rotate_button.grid(row=0, column=0)
        self.rotate_entry = Entry(self.rotate_frame, width=5)
        self.rotate_entry.grid(row=0, column=1)

        self.rot180_button = Button(self, text="Rotation à 180°", command=lambda: self.rot180())
        self.rot180_button.pack()

        self.rot90_button = Button(self, text="Rotation à 90°", command=lambda: self.rot90())
        self.rot90_button.pack()

        self.convert_to_grey_mode_button = Button(self, text="Convertir en niveaux de gris",
                                                  command=lambda: self.convert_to_grey_mode())
        self.convert_to_grey_mode_button.pack()

        self.convert_to_bw_mode_button = Button(self, text="Convertir en noir et blanc",
                                                  command=lambda: self.convert_to_bw_mode())
        self.convert_to_bw_mode_button.pack()

        self.brightness_frame = Frame(self)
        self.brightness_frame.pack()
        self.increase_brightness_button = Button(self.brightness_frame, text="Augmenter la luminosité - (0-100) %",
                                                command=lambda: self.increase_brightness())
        self.increase_brightness_button.grid(row=0, column=0)
        self.increase_brightness_entry = Entry(self.brightness_frame, width=5)
        self.increase_brightness_entry.grid(row=0, column=1)

        self.decrease_brightness_button = Button(self.brightness_frame, text="Diminuer la luminosité - (0-100) %",
                                                 command=lambda: self.decrease_brightness())
        self.decrease_brightness_button.grid(row=1, column=0)
        self.decrease_brightness_entry = Entry(self.brightness_frame, width=5)
        self.decrease_brightness_entry.grid(row=1, column=1)

        self.size_frame = Frame(self)
        self.size_frame.pack()
        self.increase_size_button = Button(self.size_frame, text="Augmenter la taille de l'image (ratio entier)",
                                                 command=lambda: self.increase_size())
        self.increase_size_button.grid(row=0, column=0)
        self.increase_size_entry = Entry(self.size_frame, width=5)
        self.increase_size_entry.grid(row=0, column=1)

        self.decrease_size_button = Button(self.size_frame, text="Diminuer la taille de l'image (ratio entier) %",
                                                command=lambda: self.decrease_size())
        self.decrease_size_button.grid(row=1, column=0)
        self.decrease_size_entry = Entry(self.size_frame, width=5)
        self.decrease_size_entry.grid(row=1, column=1)

        self.change_rgb_frame = Frame(self)
        self.change_rgb_frame.pack()
        self.change_rgb_button = Button(self.change_rgb_frame, text="Changer le RGB",
                                                 command=lambda: self.change_rgb())
        self.change_rgb_button.grid(row=0, column=0)
        self.change_r_entry = Entry(self.change_rgb_frame, width=5)
        self.change_r_entry.grid(row=0, column=1)
        self.change_g_entry = Entry(self.change_rgb_frame, width=5)
        self.change_g_entry.grid(row=0, column=2)
        self.change_b_entry = Entry(self.change_rgb_frame, width=5)
        self.change_b_entry.grid(row=0, column=3)

    def symVert(self):
        try:
            self.wins[3] = Toplevel()
            win = self.wins[3]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.symVert(img=img)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=4)

    def symHori(self):
        try:
            self.wins[4] = Toplevel()
            win = self.wins[4]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.symHori(img=img)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=5)


    def rot180(self):
        try:
            self.wins[5] = Toplevel()
            win = self.wins[5]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.rot180(img=img)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=6)
        
    def rot90(self):
        try:
            self.wins[6] = Toplevel()
            win = self.wins[6]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.rot90(img=img)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except FileNotFoundError as error:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=7)

    def convert_to_grey_mode(self):
        try:
            self.wins[7] = Toplevel()
            win = self.wins[7]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.convert_to_grey_mode(img=img, file_conversion=self.file_conversion)
            support.img_type = "pgm" if self.file_conversion else support.img_type

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            support.img_type = img["meta"]["extension"]
            support.img_type = support.img_type[1:len(support.img_type)] if support.img_type[0] == "." else support.img_type
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=8)

    def convert_to_bw_mode(self):
        try:
            self.wins[8] = Toplevel()
            win = self.wins[8]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.convert_to_bw_mode(img=img, file_conversion=self.file_conversion)
            support.img_type = "pbm"

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)

            support.img_type = img["meta"]["extension"]
            support.img_type = support.img_type[1:len(support.img_type)] if support.img_type[0] == "." else support.img_type
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=9)

    def increase_brightness(self):
        try:
            t = max(0, min(255, int(self.increase_brightness_entry.get())))
            self.wins[9] = Toplevel()
            win = self.wins[9]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.change_brightness(img=img, t=t)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except ValueError:
            messagebox.showerror(title="Erreur de saisie !", message="Veuillez indiquer le nombre en % (0-100) !")

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=10)

    def decrease_brightness(self):
        try:
            t = min(0, (max(-100, int(self.decrease_brightness_entry.get())*-1)))
            self.wins[10] = Toplevel()
            win = self.wins[10]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.change_brightness(img=img, t=t)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except ValueError:
            messagebox.showerror(title="Erreur de saisie !", message="Veuillez indiquer le nombre en % (0-100) !")

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=11)
            
    def increase_size(self):
        try:
            ratio = max(0, min(255, int(self.increase_size_entry.get())))
            self.wins[12] = Toplevel()
            win = self.wins[12]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.increase_size(img=img, ratio=ratio)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except ValueError:
            messagebox.showerror(title="Erreur de saisie !", message="Veuillez indiquer le nombre en % (0-100) !")

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=13)

    def decrease_size(self):
        try:
            ratio = max(0, min(255, int(self.decrease_size_entry.get())))
            self.wins[13] = Toplevel()
            win = self.wins[13]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.decrease_size(img=img, ratio=ratio)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except ValueError:
            messagebox.showerror(title="Erreur de saisie !", message="Veuillez indiquer le nombre en % (0-100) !")

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=14)

    def change_rgb(self):
        try:
            rgb_values = (max(-100, min(100, int(self.change_r_entry.get()))) if self.change_r_entry.get() else None,
                          max(-100, min(100, int(self.change_g_entry.get()))) if self.change_g_entry.get() else None,
                          max(-100, min(100, int(self.change_b_entry.get()))) if self.change_b_entry.get() else None,
            )
            self.wins[14] = Toplevel()
            win = self.wins[14]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.change_rgb(img=img, rgb=rgb_values)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=15)
            
    def rotate(self):
        try:
            angle = max(0, min(360, int(self.rotate_entry.get())))
            self.wins[15] = Toplevel()
            win = self.wins[15]
            support = Support(win=win)
            img = support.open(filename=self.img_1_path_entry.get())
            image = self.traitement.rotate(img=img, angle=angle)

            support.save(img=image)

            image = support.create_image(image=image, ratio=2)
            img = support.create_image(image=img, ratio=2)

            support.compare(imgs=[img, image])

        except FileNotFoundError:
            messagebox.showerror(title="Fichier inexistant !",
                                 message=f"Le fichier {self.img_1_path_entry.get()}\nn'existe pas !")
            self.close_win(img_id=16)


    def manage_win(self):
        # Informations fenêtres
        self.init_informations()
        self.create_form()
        self.create_filter_buttons()
        self.mainloop()

if __name__ == "__main__":
    Win().manage_win()
