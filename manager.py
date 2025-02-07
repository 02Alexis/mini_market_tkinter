# ------------ Información principal del proyecto

from tkinter import *
from tkinter import ttk
from login import Login
from login import Registro
from container import Container
import sys
import os

class Manager(Tk):
    def __init_(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Mini Market")
        self.geometry("1100x650+120+120")
        self.resizable(False, False) # ----- No se podra redimencionar

        container = Frame(self)
        container.pack(side=TOP, fill=BOTH, expand=True)
        container.configure(bg="008f39")

        self.frame = {}
        for i in (Login, Registro, Container):
            frame = i(container, self)
            self.frames[i] = frame
            
        self.show_frame(Login)

        self.style = ttk.Style()
        self.style.theme_use("clam")

    def show_frame(self, container):
        frame = self.frame (container)
        frame.tkraise()

def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()