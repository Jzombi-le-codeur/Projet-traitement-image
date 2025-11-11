from tkinter import *
from tkinter import filedialog
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

        self.support = Support()
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
                if img["filepath"] != pathlib.Path():
                    img["imgs"].append(self.support.open(filename=img["filepath"]))

        else:
            self.win.imgs[image-1]["imgs"].append(self.support.open(filename=self.win.imgs[image-1]["filepath"]))

    def __draw_image(self, *args):
        active_image = self.active_image.get()
        if active_image != 0:
            image = self.support.create_image(image=self.win.imgs[active_image-1]["imgs"][-1])
            image = ImageTk.PhotoImage(image=image)
            self.img_label.config(image=image)
            self.img_label.image = image

        # Réinitaliser les flags
        if self.new_image.get():
            self.__set_without_flag(var="new_image", value=False)

    def create_page(self):
        self.edit_win_filters = EditWinFilters(edit_page=self)
        self.edit_win_filters.pack()
        self.img_label = Label(self)
        self.img_label.pack()

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
        self.symhori_button = Button(self.sym_frame, text="Symétrie horizontale")
        self.symhori_button.grid(column=1, row=0)
        
        
        """ Rotation """
        # Frame Rotation
        self.rot_frame = Frame(self)
        self.rot_frame.grid(column=1, row=0, padx=self.frames_sep)

        # Free Rotation
        self.rot_button = Button(self.rot_frame, text="Rotation")
        self.rot_button.grid(column=0, row=0)

        # Rotation 90°
        self.rot90_button = Button(self.rot_frame, text="Rotation 90°")
        self.rot90_button.grid(column=1, row=0)

        # Rotation 180°
        self.rot180_button = Button(self.rot_frame, text="Rotation 180°")
        self.rot180_button.grid(column=2, row=0)


        """ Convertion """
        # Frame Conversion
        self.convert_frame = Frame(self)
        self.convert_frame.grid(column=2, row=0, padx=self.frames_sep)

        # Convertion noir/blanc
        self.convert_bw_button = Button(self.convert_frame, text="Convertir en noir et blanc")
        self.convert_bw_button.grid(column=0, row=0)

        # Convertion niveaux de gris
        self.convert_grey_button = Button(self.convert_frame, text="Convertir en niveaux de gris")
        self.convert_grey_button.grid(column=1, row=0)


        """ Réglages """
        # Frame Réglages
        self.image_settings_frame = Frame(self)
        self.image_settings_frame.grid(column=2, row=0, padx=self.frames_sep)

        # Luminosité
        self.brightness_button = Button(self.image_settings_frame, text="Changer la luminosité")
        self.brightness_button.grid(column=0, row=0)

        # Taille
        self.size_button = Button(self.image_settings_frame, text="Changer la taille")
        self.size_button.grid(column=1, row=0)

        # Couleurs
        self.rgb_button = Button(self.image_settings_frame, text="Modifier les RGB")
        self.rgb_button.grid(column=2, row=0)
        
        
class WinTraitement:
    def __init__(self, edit_page):
        self.edit_page = edit_page
        self.traitement = Traitement()

    def apply_filter(self, filter: str):
        img = self.edit_page.win.imgs[self.edit_page.active_image.get() - 1]["imgs"][-1]
        if filter == "symvert":
            image = self.symVert(img=img)

        self.edit_page.win.imgs[self.edit_page.active_image.get() - 1]["imgs"].append(image)
        self.edit_page.new_image.set(True)

    def symVert(self, img: dict) -> dict:
        image = self.traitement.symVert(img=img)
        return image


Win().run()
