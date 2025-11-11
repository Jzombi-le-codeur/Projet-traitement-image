from tkinter import *
from tkinter import filedialog
import pathlib
from support import Support
from traitement import Traitement


class Win(Tk):
    def __init__(self):
        super().__init__()

        # Utils
        self.traitement = Traitement()

        # Sauvegardes
        self.img1 = {
            "filepath": pathlib.Path()
        }
        self.img2 = {
            "filepath": pathlib.Path()
        }

        # States
        self.started = BooleanVar()
        self.started.trace("w", self.manage_pages)
        self.editing = BooleanVar()
        self.editing.trace("w", self.manage_pages)

        # Pages
        self.init_page = InitPage(win=self)
        self.init_page.pack(fill="both", expand=True)

    def init_informations(self):
        self.title("Projet Traitement Image")
        self.geometry("1280x720")

    def manage_pages(self, *args):
        if self.started.get():
            if not self.editing.get():
                self.init_page.run()

            else:
                print('caca')

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
            filetypes=[("Images PNM", "*.ppm *.pgm *.pbm")]
        ))

        if img == 1:
            self.win.img1["filepath"] = filename
            self.state.set("file_opened")

        elif img == 2:
            self.win.img2["filepath"] = filename
            self.state.set("all_files_opened")

    def __close_page(self):
        for widget in self.winfo_children():
            widget.destroy()

    def __switch_page(self):
        self.__close_page()
        self.state.set("switch_page")

    def create_page(self):
        self.buttons_frame = Frame(self)
        self.buttons_frame.pack(expand=True)

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


Win().run()
