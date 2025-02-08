from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class Inventario(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def widgets(self):
    # =============================================================
        canvas_article = tk.LabelFrame(self, text="Articulos", font="arial 14 bold", bg="#95c799")
        canvas_article.place(x=300, y=10, width=780, height=580)

        self.canvas = tk.Canvas(canvas_article, bg="#95c799")
        self.scrollbar = tk.Scrollbar(canvas_article, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#95c799")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        # ----- configuracion del scroll
        self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # ----- configuracion del canvas
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
    # =============================================================
    # ----- search
        lblframe_buscar = LabelFrame(self, text="Buscar", font="arial 14 bold", bg="#95c799")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)

        self.comboboxbuscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.comboboxbuscar.place(x=5, y=5, width=260, height=40)
    # =============================================================
    # ----- seleccion
        lblframe_selection = LabelFrame(self, text="Selección", font="arial 14 bold", bg="#95c799")
        lblframe_selection.place(x=10, y=95, width=280, height=190)

        self.label1 = tk.Label(lblframe_selection, text="Articulo: ", font="arial 12", bg="#95c799", wraplength=300)
        self.label1.place(x=5, y=5)
        self.label2 = tk.Label(lblframe_selection, text="Precio: ", font="arial 12", bg="#95c799")
        self.label2.place(x=5, y=40)
        self.label3 = tk.Label(lblframe_selection, text="Costo: ", font="arial 12", bg="#95c799")
        self.label3.place(x=5, y=70)
        self.label4 = tk.Label(lblframe_selection, text="Stock: ", font="arial 12", bg="#95c799")
        self.label4.place(x=5, y=100)
        self.label5 = tk.Label(lblframe_selection, text="Estado: ", font="arial 12", bg="#95c799")
        self.label5.place(x=5, y=130)
    # =============================================================
    # ----- Opciones
        lblframe_buttons = LabelFrame(self, text="Opciones", font="arial 14 bold", bg="#95c799")
        lblframe_buttons.place(x=10, y=290, width=280, height=300)

        btn1 = tk.Button(lblframe_buttons, text="Agregar", font="arial 14 bold")
        btn1.place(x=20, y=20, width=180, height=40)
        btn2 = tk.Button(lblframe_buttons, text="Editar", font="arial 14 bold")
        btn2.place(x=20, y=80, width=180, height=40)


