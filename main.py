from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
import pathlib
from PIL import Image, ImageTk
from support import Support
from traitement import Traitement
import darkdetect


class Win(Tk):
    """ CLASSE GERANT LA FENETRE """
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
        self.i = IntVar(value=-1)
        # self.i_bfr = IntVar(value=self.i.get())
        self.i.trace("w", self.manage_pages)
        self.state = StringVar()

        # States
        self.started = BooleanVar()
        self.started.trace("w", self.manage_pages)
        self.editing = BooleanVar()
        self.editing.trace("w", self.manage_pages)
        self.view_mode = BooleanVar(value=False)
        self.view_mode.trace("w", self.manage_pages)
        self.system_theme = True
        self.dark_mode = False
        self.active_image = IntVar()  # 0(compare)/1/2/

        # Pages
        self.init_page = InitPage(win=self)
        self.edit_page = EditPage(win=self)
        self.view_page = ViewPage(win=self)
        theme_button_text = "Light Mode" if self.dark_mode else "Dark Mode"
        self.theme_button = Button(self, text=theme_button_text, command=self.__change_theme)

        self.state.trace("w", self.init_page.update_page)

        # Settings
        self.file_conversion = True

    def init_informations(self):
        self.title("Projet Traitement Image")
        self.geometry("1280x720")

    def __apply_theme(self, widget, bg_color, fg_color):
        # Essaie de configurer le widget
        try:
            widget.config(bg=bg_color, fg=fg_color),
            activebackground = bg_color,
            activeforeground = fg_color
        except:
            try:
                widget.config(bg=bg_color)  # Certains widgets n'ont pas fg
            except:
                pass

        # Parcours tous les enfants
        for child in widget.winfo_children():
            self.__apply_theme(child, bg_color, fg_color)

    def __set_system_theme(self):
        self.dark_mode = False if darkdetect.isDark() else True

        self.__change_theme()
        self.system_theme = False

    def __change_theme(self):
        if self.dark_mode:
            bg_color = "#f0f0f0"
            fg_color = "#000000"
            self.dark_mode = False
            self.theme_button.config(text="Dark Mode")

        else:
            bg_color = "#2b2d30"
            fg_color = "#ffffff"
            self.dark_mode = True
            self.theme_button.config(text="Light mode")

        self.config(background=bg_color)

        self.__apply_theme(self.init_page, bg_color=bg_color, fg_color=fg_color)
        self.__apply_theme(self.edit_page, bg_color=bg_color, fg_color=fg_color)
        self.__apply_theme(self.view_page, bg_color=bg_color, fg_color=fg_color)
        self.__apply_theme(self.theme_button, bg_color=bg_color, fg_color=fg_color)
        try:
            self.__apply_theme(self.edit_frame, bg_color=bg_color, fg_color=fg_color)

        except AttributeError:
            pass

    def set_theme(self):
        if self.system_theme:
            self.__set_system_theme()

        else:
            self.dark_mode = False if self.dark_mode else True
            self.__change_theme()

    def undo(self):
        if self.imgs[self.active_image.get() - 1]["imgs"][self.i.get()] != self.imgs[self.active_image.get() - 1]["imgs"][0]:
            self.i.set(self.i.get() - 1)

    def redo(self):
        if self.imgs[self.active_image.get() - 1]["imgs"][self.i.get()] != self.imgs[self.active_image.get() - 1]["imgs"][-1]:
            self.i.set(self.i.get() + 1)

    def manage_pages(self, *args):
        if self.started.get():
            if not self.editing.get():
                self.edit_page.pack_forget()
                self.init_page.pack(expand=True)
                self.init_page.run()

            else:
                self.init_page.pack_forget()
                if self.view_mode.get():
                    try:
                        self.edit_frame.pack_forget()

                    except AttributeError:
                        pass

                    self.edit_page.pack_forget()
                    self.view_page.pack()
                    self.view_page.run()

                else:
                    self.view_page.pack_forget()
                    if self.edit_page.first:
                        self.edit_frame = Frame(self)
                        self.previous_button = Button(self.edit_frame, text="<-", command=self.undo)
                        self.next_button = Button(self.edit_frame, text="->", command=self.redo)
                        self.previous_button.grid(column=0, row=0)
                        self.next_button.grid(column=1, row=0)

                    self.edit_frame.pack(anchor="nw")

                    self.edit_page.pack()
                    self.edit_page.run()

        try:
            self.theme_button.pack_forget()

        except:
            pass

        theme_button_text = "Light Mode" if self.dark_mode else "Dark Mode"
        self.theme_button.config(text=theme_button_text)
        self.theme_button.pack(side="bottom")

        self.set_theme()


    def run(self):
        self.init_informations()
        self.started.set(True)
        self.mainloop()


class InitPage(Frame):
    """ Gère la première page de la fenêtre. """
    def __init__(self, win):
        self.win = win
        super().__init__()

    def open_file(self, img: int):
        filename = pathlib.Path(filedialog.askopenfilename(
            filetypes=[("Images", "*.pbm *.pgm *.ppm")]
        ))
        self.win.imgs[img - 1]["filepath"] = filename

        if img == 1:
            self.win.state.set("file_opened")

        elif img == 2:
            self.win.state.set("all_files_opened")

    def __switch_page(self):
        self.win.state.set("switch_page")

    def create_page(self):
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack()

        self.open_file_button = Button(self.buttons_frame,
                                       text="Ouvrir un fichier",
                                       command=lambda: self.open_file(img=1))
        self.open_file_button.pack()

        self.edit_button = Button(self.buttons_frame, text="Editer l'image", command=self.__switch_page)

    def update_page(self, *args):
        if self.win.state.get() == "file_opened":
            self.open_file_button.config(command=lambda: self.open_file(img=2))
            self.edit_button.pack()

        elif self.win.state.get() == "all_files_opened":
            self.open_file_button.config(state="disabled")

        elif self.win.state.get() == "switch_page":
            self.win.editing.set(True)

    def manage_page(self):
        self.create_page()

    def run(self):
        self.manage_page()


class EditPage(Frame):
    """ Gère la page d'édition de l'image. Dépend de Win, et hérite de tk.Frame """
    def __init__(self, win):
        self.win = win
        super().__init__()
        self.win_traitement = WinTraitement(edit_page=self)

        self.first = True

        self.new_image = BooleanVar()
        self.new_image_trace_id = self.new_image.trace_add("write", self.__draw_image)
        self.active_image_trace_id = self.win.active_image.trace_add("write", self.__draw_image)

    def __set_without_flag(self, var: str, value):
        if var == "new_image":
            self.new_image.trace_remove("write", self.new_image_trace_id)
            self.new_image.set(value)
            self.new_image_trace_id = self.new_image.trace_add("write", self.__draw_image)

    def __open_image(self, image: int = 0):
        if image == 0:
            for img in self.win.imgs:
                if img["filepath"] != pathlib.Path() and not img["imgs"]:
                    support = Support()
                    img["imgs"].append(support.open(filename=img["filepath"]))
        else:
            img_obj = self.win.imgs[image - 1]
            if img_obj["filepath"] != pathlib.Path() and not img_obj["imgs"]:
                support = Support()
                img_obj["imgs"].append(support.open(filename=img_obj["filepath"]))

    def __draw_image(self, *args):
        active_image = self.win.active_image.get()
        if active_image != 0:
            support = Support()
            image = support.create_image(image=self.win.imgs[active_image - 1]["imgs"][self.win.i.get()])
            image = ImageTk.PhotoImage(image=image)
            self.img_label.config(image=image)
            self.img_label.image = image

        # Réinitaliser les flags
        if self.new_image.get():
            self.__set_without_flag(var="new_image", value=False)
            del self.win.imgs[self.win.active_image.get() - 1]["imgs"][-2:self.win.i.get()-1:-1]
            self.win.i.set(-1)

    def __save_image(self):
        path = pathlib.Path(filedialog.askdirectory())
        Support().save(img=self.win.imgs[self.win.active_image.get() - 1]["imgs"][self.win.i.get()], path=path)

    def change_image(self):
        if not self.win.imgs[1]["imgs"]:
            self.win.init_page.open_file(img=2)
            self.__open_image(2)

            self.win.active_image.set(2)
            self.change_image_button.config(text="Afficher l'image 1")

            self.win.state.set("all_images_opened")

        else:
            if self.win.active_image.get() == 1:
                self.win.active_image.set(2)
                self.change_image_button.config(text="Afficher l'image 1")

            elif self.win.active_image.get() == 2:
                self.win.active_image.set(1)
                self.change_image_button.config(text="Afficher l'image 2")

    def __define_change_button_text(self) -> str:
        if not self.win.imgs[1]["imgs"]:
            return "Ouvrir une 2e image"

        else:
            return f"Ouvrir l'image {self.win.active_image.get()}"
        
    def __set_view_mode(self):
        self.win.view_mode.set(True)

    def create_page(self):
        self.edit_win_filters = EditWinFilters(edit_page=self)
        self.edit_win_filters.pack()
        self.main_frame = Frame(self)
        # self.main_frame.pack(fill="x")
        self.main_frame.pack()
        self.img_label = Label(self.main_frame)
        self.img_label.grid(column=0, row=0)
        self.change_image_button = Button(self, text=self.__define_change_button_text(), command=self.change_image)
        self.change_image_button.pack()
        self.set_view_mode_button = Button(self, text="Mode Vue", command=self.__set_view_mode)
        self.set_view_mode_button.pack()
        self.save_button = Button(self, text="Sauvegarder", command=self.__save_image)
        self.save_button.pack()

    def manage_page(self):
        if self.first:
            self.create_page()

        self.__open_image()
        if self.first:
            if self.win.imgs[1]["imgs"]:
                self.win.active_image.set(2)
                self.__define_change_button_text()
                self.change_image()

            else:
                self.win.active_image.set(1)

            self.first = False

        self.__draw_image()

    def run(self):
        self.manage_page()


class EditWinFilters(Frame):
    """ Classe gérant les boutons pour appliquer les filtres sur la page. Dépend de EditPage, et hérite de tk.Frame """
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
    """ Classe appliquant les filtres (exécute les méthode de Traitement). Dépend de EditPage, et hérite de tk.Frame """
    def __init__(self, edit_page):
        self.edit_page = edit_page
        self.traitement = Traitement()

    def apply_filter(self, filter: str):
        img = self.edit_page.win.imgs[self.edit_page.win.active_image.get() - 1]["imgs"][self.edit_page.win.i.get()]
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

        self.edit_page.win.imgs[self.edit_page.win.active_image.get() - 1]["imgs"].append(image)
        self.edit_page.new_image.set(True)


class ViewPage(Frame):
    """ Classe gérant la page de view-only des images. Dépend de Win, et hérite de tk.Frame """
    def __init__(self, win):
        self.win = win
        super().__init__()

        self.first = True

        self.main_frame = Frame(self)
        self.img_label = Label(self.main_frame)
        self.img2_label = Label(self.main_frame)

        self.new_image = BooleanVar()
        self.new_image_trace_id = self.new_image.trace_add("write", self.__draw_image)
        self.active_image_trace_id = self.win.active_image.trace_add("write", self.__draw_image)

        self.compare = BooleanVar(value=False)
        self.compare_trace_id = self.compare.trace_add("write", self.update_compare)

    def __set_without_flag(self, var: str, value):
        if var == "new_image":
            self.new_image.trace_remove("write", self.new_image_trace_id)
            self.new_image.set(value)
            self.new_image_trace_id = self.new_image.trace_add("write", self.__draw_image)

    def __open_image(self, image: int = 0):
        if image == 0:
            for img in self.win.imgs:
                if img["filepath"] != pathlib.Path() and not img["imgs"]:
                    support = Support()
                    img["imgs"].append(support.open(filename=img["filepath"]))
        else:
            img_obj = self.win.imgs[image - 1]
            if img_obj["filepath"] != pathlib.Path() and not img_obj["imgs"]:
                support = Support()
                img_obj["imgs"].append(support.open(filename=img_obj["filepath"]))

    def __draw_image(self, *args):
        if not self.compare.get():
            try:
                self.img2_label.grid_forget()

            except Exception:
                pass

            active_image = self.win.active_image.get()
            if active_image != 0:
                support = Support()
                image = support.create_image(image=self.win.imgs[active_image - 1]["imgs"][self.win.i.get()])
                image = ImageTk.PhotoImage(image=image)
                self.img_label.config(image=image)
                self.img_label.image = image

        else:
            self.img2_label.grid(column=1, row=0)

            support = Support()
            image = support.create_image(image=self.win.imgs[0]["imgs"][self.win.i.get()])
            image = ImageTk.PhotoImage(image=image)
            self.img_label.config(image=image)
            self.img_label.image = image

            image2 = support.create_image(image=self.win.imgs[1]["imgs"][self.win.i.get()])
            image2 = ImageTk.PhotoImage(image=image2)
            self.img2_label.config(image=image2)
            self.img2_label.image = image2

        # Réinitaliser les flags
        if self.new_image.get():
            self.__set_without_flag(var="new_image", value=False)

    def update_compare(self, *args):
        self.__draw_image()
        self.compare_button.config(text=self.__define_compare_button_text())

    def change_image(self):
        if not self.win.imgs[1]["imgs"]:
            self.win.init_page.open_file(img=2)
            self.__open_image(2)

            self.win.active_image.set(2)
            self.change_image_button.config(text="Afficher l'image 1")

            self.win.state.set("all_images_opened")

        else:
            if self.win.active_image.get() == 1:
                self.win.active_image.set(2)
                self.change_image_button.config(text="Afficher l'image 1")

            elif self.win.active_image.get() == 2:
                self.win.active_image.set(1)
                self.change_image_button.config(text="Afficher l'image 2")

    def __define_change_button_text(self) -> str:
        if not self.win.imgs[1]["imgs"]:
            return "Ouvrir une 2e image"

        else:
            return f"Ouvrir l'image {self.win.active_image.get()}"

    def __define_compare_button_text(self):
        if self.compare.get():
            return "Afficher une seule image"

        else:
            return "Comparer les images"

    def set_compare_mode(self):
        if not self.compare.get():
            if self.win.imgs[1]["imgs"]:
                self.compare.set(True)

        else:
            self.compare.set(False)

    def __set_edit_mode(self):
        self.win.view_mode.set(False)

    def create_page(self):
        self.main_frame.pack()
        self.img_label.grid(column=0, row=0)
        self.change_image_button = Button(self, text=self.__define_change_button_text(), command=self.change_image)
        self.change_image_button.pack()
        self.compare_button = Button(self, text=self.__define_compare_button_text(), command=self.set_compare_mode)
        self.compare_button.pack()
        self.set_edit_mode_button = Button(self, text="Mode Modifications", command=self.__set_edit_mode)
        self.set_edit_mode_button.pack()

    def manage_page(self):
        if self.first:
            self.create_page()

        self.__open_image()
        if self.first:
            if self.win.imgs[1]["imgs"]:
                self.win.active_image.set(2)
                self.__define_change_button_text()
                self.change_image()

            else:
                self.win.active_image.set(1)

            self.first = False

        self.__draw_image()

    def run(self):
        self.manage_page()


Win().run()