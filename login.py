from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Login(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()

    def widgets(self):
        background =tk.Frame(self, bg="#95c799")
        background.pack()
        background.place(x=0, y=0, width=1100, height=650)

        self.bg_image = Image.open("images/background.jpg")
        self.bg_image = self.bg_image.resize((1100, 650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ttk.Label(background, image=self.bg_image)
        self.bg_label.place(x=0, y=0, width=1100, height=650)

        frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)
        frame1.place(x=350, y=70, width=400, height=560)

        user = ttk.Label(frame1, text="Nombre de Usuario", font="arial 16 bold", background="#FFFFFF")
        user.place(x=100, y=250)
        self.username = ttk.Entry(frame1, font="arial 16 bold")
        self.username.place(x=80, y=290, width=240, height=40)

        pas = ttk.Label(frame1, text="Contraseña", font="arial 16 bold", background="#FFFFFF")
        pas.place(x=100, y=340)
        self.password = ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.password.place(x=80, y=380, width=240, height=40)

        btn = tk.Button(frame1, text="Iniciar", font="arial 16 bold",)
        btn.place(x=80, y=440, width=240, height=40)

        btn2 = tk.Button(frame1, text="Registrar", font="arial 16 bold",)
        btn2.place(x=80, y=500, width=240, height=40)

class Registro(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()

    def widgets(self):
        background =tk.Frame(self, bg="#95c799")
        background.pack()
        background.place(x=0, y=0, width=1100, height=650)

        self.bg_image = Image.open("images/background.jpg")
        self.bg_image = self.bg_image.resize((1100, 650))
        self.bg_image = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = ttk.Label(background, image=self.bg_image)
        self.bg_label.place(x=0, y=0, width=1100, height=650)

        frame1 = tk.Frame(self, bg="#FFFFFF", highlightbackground="black", highlightthickness=1)
        frame1.place(x=350, y=10, width=400, height=630)

        user = ttk.Label(frame1, text="Nombre de Usuario", font="arial 16 bold", background="#FFFFFF")
        user.place(x=100, y=250)
        self.username = ttk.Entry(frame1, font="arial 16 bold")
        self.username.place(x=80, y=290, width=240, height=40)

        pas = ttk.Label(frame1, text="Contraseña", font="arial 16 bold", background="#FFFFFF")
        pas.place(x=100, y=340)
        self.password = ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.password.place(x=80, y=380, width=240, height=40)

        key = ttk.Label(frame1, text="Codigo de Registro", font="arial 16 bold", background="#FFFFFF")
        key.place(x=100, y=250)
        self.key = ttk.Entry(frame1, show="*", font="arial 16 bold")
        self.key.place(x=80, y=470, width=240, height=40)

        btn3 = tk.Button(frame1, text="Registrar", font="arial 16 bold",)
        btn3.place(x=80, y=500, width=240, height=40)

        btn4 = tk.Button(frame1, text="Regresar", font="arial 16 bold",)
        btn4.place(x=80, y=570, width=240, height=40)