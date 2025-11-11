from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import pathlib
from PIL import Image, ImageTk
from support import Support
from traitement import Traitement


class Win(Tk):
    def __init__(self):
        super().__init__()

        # Utils
        self.traitement = Traitement()

        # Sauvegardes
        self.img1 = {
            "filepath": pathlib.Path(),
            "imgs": list()
        }
        self.img2 = {
            "filepath": pathlib.Path(),
            "imgs": list()
        }
        self.imgs = [self.img1, self.img2]

        # States
        self.started = BooleanVar()
        self.started.trace("w", self.manage_pages)
        self.editing = BooleanVar()
        self.editing.trace("w", self.manage_pages)

        # Pages
        self.init_page = InitPage(win=self)
        self.edit_page = EditPage(win=self)

        # Settings
        self.file_conversion = True

    def init_informations(self):
        self.title("Projet Traitement Image")
        self.geometry("1280x720")

    def manage_pages(self, *args):
        if self.started.get():
            if not self.editing.get():
                self.edit_page.pack_forget()
                self.init_page.pack(expand=True)
                self.init_page.run()

            else:
                self.init_page.pack_forget()
                self.edit_page.pack()
                self.edit_page.run()

    def run(self):
        self.init_informations()
        self.started.set(True)
        self.mainloop()


class InitPage(Frame):
    def __init__(self, win):
        self.win = win
        super().__init__()

        self.state = StringVar()
        self.state.trace("w", self.update_page)

    def __open_file(self, img: int):
        filename = pathlib.Path(filedialog.askopenfilename(
            filetypes=[("Images", "*.pbm *.pgm *.ppm")]
        ))
        self.win.imgs[img-1]["filepath"] = filename

        if img == 1:
            self.state.set("file_opened")

        elif img == 2:
            self.state.set("all_files_opened")

    def __switch_page(self):
        self.state.set("switch_page")

    def create_page(self):
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack()

        self.open_file_button = Button(self.buttons_frame,
                                       text="Ouvrir un fichier",
                                       command=lambda: self.__open_file(img=1))
        self.open_file_button.pack()

        self.edit_button = Button(self.buttons_frame, text="Editer l'image", command=self.__switch_page)

    def update_page(self, *args):
        if self.state.get() == "file_opened":
            self.open_file_button.config(command=lambda: self.__open_file(img=2))
            self.edit_button.pack()

        elif self.state.get() == "all_files_opened":
            self.open_file_button.config(state="disabled")

        elif self.state.get() == "switch_page":
            self.win.editing.set(True)

    def manage_page(self):
        self.create_page()

    def run(self):
        self.manage_page()


class EditPage(Frame):
    def __init__(self, win):
        self.win = win
        super().__init__()
        self.win_traitement = WinTraitement(edit_page=self)

        self.active_image = IntVar()  # 0(compare)/1/2/
        self.active_image_trace_id = self.active_image.trace_add("write", self.__draw_image)
        self.new_image = BooleanVar()
        self.new_image_trace_id = self.new_image.trace_add("write", self.__draw_image)

    def __set_without_flag(self, var: str, value):
        if var == "new_image":
            self.new_image.trace_remove("write", self.new_image_trace_id)
            self.new_image.set(value)
            self.new_image_trace_id = self.new_image.trace_add("write", self.__draw_image)

    def __open_image(self, image: int = 0):
        if image == 0:
            for img in self.win.imgs:
                support = Support()
                if img["filepath"] != pathlib.Path():
                    img["imgs"].append(support.open(filename=img["filepath"]))

        else:
            support = Support()
            self.win.imgs[image-1]["imgs"].append(support.open(filename=self.win.imgs[image-1]["filepath"]))

    def __draw_image(self, *args):
        active_image = self.active_image.get()
        if active_image != 0:
            support = Support()
            image = support.create_image(image=self.win.imgs[active_image-1]["imgs"][-1])
            image = ImageTk.PhotoImage(image=image)
            self.img_label.config(image=image)
            self.img_label.image = image

        # Réinitaliser les flags
        if self.new_image.get():
            self.__set_without_flag(var="new_image", value=False)

    def __save_image(self):
        path = pathlib.Path(filedialog.askdirectory())
        Support().save(img=self.win.imgs[self.active_image.get()-1]["imgs"][-1], path=path)

    def create_page(self):
        self.edit_win_filters = EditWinFilters(edit_page=self)
        self.edit_win_filters.pack()
        self.img_label = Label(self)
        self.img_label.pack()
        self.save_button = Button(self, text="Sauvegarder", command=self.__save_image)
        self.save_button.pack()

    def manage_page(self):
        self.create_page()
        self.__open_image()
        self.active_image.set(1)

    def run(self):
        self.manage_page()


class EditWinFilters(Frame):
    def __init__(self, edit_page):
        self.edit_page = edit_page
        super().__init__(edit_page)

        self.aff = self.edit_page.win_traitement.apply_filter  # Fonction "apply filter"

        self.frames_sep = 10
        self.filters()

    def filters(self):
        """ Symétrie """
        # Frame Symétrie
        self.sym_frame = Frame(self)
        self.sym_frame.grid(column=0, row=0, padx=self.frames_sep)
        
        # Symétrie verticale
        self.symvert_button = Button(self.sym_frame, text="Symétrie verticale", command=lambda: self.aff("symvert"))
        self.symvert_button.grid(column=0, row=0)
        
        # Symétrie horizontale
        self.symhori_button = Button(self.sym_frame, text="Symétrie horizontale", command=lambda: self.aff("symhori"))
        self.symhori_button.grid(column=1, row=0)
        
        
        """ Rotation """
        # Frame Rotation
        self.rot_frame = Frame(self)
        self.rot_frame.grid(column=1, row=0, padx=self.frames_sep)

        # Free Rotation
        self.rot_button = Button(self.rot_frame, text="Rotation", command=lambda: self.aff("rot"))
        self.rot_button.grid(column=0, row=0)

        # Rotation 90°
        self.rot90_button = Button(self.rot_frame, text="Rotation 90°", command=lambda: self.aff("rot90"))
        self.rot90_button.grid(column=1, row=0)

        # Rotation 180°
        self.rot180_button = Button(self.rot_frame, text="Rotation 180°", command=lambda: self.aff("rot180"))
        self.rot180_button.grid(column=2, row=0)


        """ Convertion """
        # Frame Conversion
        self.convert_frame = Frame(self)
        self.convert_frame.grid(column=2, row=0, padx=self.frames_sep)

        # Convertion noir/blanc
        self.convert_bw_button = Button(self.convert_frame, text="Convertir en noir et blanc",
                                        command=lambda: self.aff("bw"))
        self.convert_bw_button.grid(column=0, row=0)

        # Convertion niveaux de gris
        self.convert_grey_button = Button(self.convert_frame, text="Convertir en niveaux de gris",
                                          command=lambda: self.aff("grey"))
        self.convert_grey_button.grid(column=1, row=0)


        """ Réglages """
        # Frame Réglages
        self.image_settings_frame = Frame(self)
        self.image_settings_frame.grid(column=3, row=0, padx=self.frames_sep)

        # Luminosité
        self.brightness_button = Button(self.image_settings_frame, text="Changer la luminosité",
                                        command=lambda: self.aff("brightness"))
        self.brightness_button.grid(column=0, row=0)

        # Taille
        self.size_button = Button(self.image_settings_frame, text="Changer la taille",
                                  command=lambda: self.aff("size"))
        self.size_button.grid(column=1, row=0)

        # Couleurs
        self.rgb_button = Button(self.image_settings_frame, text="Modifier les RGB",
                                 command=lambda: self.aff("rgb"))
        self.rgb_button.grid(column=2, row=0)
        
        
class WinTraitement:
    def __init__(self, edit_page):
        self.edit_page = edit_page
        self.traitement = Traitement()

    def apply_filter(self, filter: str):
        img = self.edit_page.win.imgs[self.edit_page.active_image.get() - 1]["imgs"][-1]
        if filter == "symvert":
            image = self.traitement.symVert(img=img)

        elif filter == "symhori":
            image = self.traitement.symHori(img=img)

        elif filter == "rot":
            angle = simpledialog.askinteger(
                title="Angle",
                prompt="De combien d'angle veux-tu appliquer la rotation ? (-360 - 360)"
            )
            angle = min(360, max(-360, angle))
            image = self.traitement.rotate(img=img, angle=angle)

        elif filter == "rot90":
            image = self.traitement.rot90(img=img)

        elif filter == "rot180":
            image = self.traitement.rot180(img=img)

        elif filter == "bw":
            image = self.traitement.convert_to_bw_mode(img=img, file_conversion=self.edit_page.win.file_conversion)

        elif filter == "grey":
            image = self.traitement.convert_to_grey_mode(img=img, file_conversion=self.edit_page.win.file_conversion)

        elif filter == "brightness":
            t = simpledialog.askinteger(
                title="Taux luminosité",
                prompt="De combien de % veux-tu changer la luminosité de l'image (-100 - 100) ?"
            )
            t = min(100, max(-100, t))
            print(t)
            image = self.traitement.change_brightness(img=img, t=t)

        elif filter == "size":
            ratio = simpledialog.askinteger(
                title="Ratio changement de taille",
                prompt="Par combien de fois veux-tu multiplier/diviser la taille (-5 - 5)"
            )
            ratio = min(5, max(-5, ratio))
            if ratio > 0:
                image = self.traitement.increase_size(img=img, ratio=ratio)

            elif ratio < 0:
                image = self.traitement.decrease_size(img=img, ratio=ratio)

            else:
                image = img

        elif filter == "rgb":
            r = simpledialog.askinteger(
                title="Valeur rouge",
                prompt="Valeur rouge ? (-255 - 255)"
            )
            r = max(-255, min(255, r))
            g = simpledialog.askinteger(
                title="Valeur vert",
                prompt="Valeur vert ? (-255 - 255)"
            )
            g = max(-255, min(255, g))
            b = simpledialog.askinteger(
                title="Valeur bleu",
                prompt="Valeur bleu ? (-255 - 255)"
            )
            b = max(-255, min(255, b))

            image = self.traitement.change_rgb(img=img, rgb=(r, g, b))

        self.edit_page.win.imgs[self.edit_page.active_image.get() - 1]["imgs"].append(image)
        self.edit_page.new_image.set(True)


Win().run()
