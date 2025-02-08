import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sys
import os

class Inventario(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.articles_combobox()

        self.image_folder = "images/folder"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)

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

        btn1 = tk.Button(lblframe_buttons, text="Agregar", font="arial 14 bold", command=self.add_article)
        btn1.place(x=20, y=20, width=180, height=40)
        btn2 = tk.Button(lblframe_buttons, text="Editar", font="arial 14 bold")
        btn2.place(x=20, y=80, width=180, height=40)

    def load_image(self):
        file_path = filedialog.askopenfilename()    
        if file_path:
            image = Image.open(file_path)
            image = image.resize((200, 200), Image.LANCZOS)
            image_name = os.path.basename(file_path)
            image_save_path = os.path.join(self.image_folder, image_name)
            image.save(image_save_path)

            self.image_tk = ImageTk.PhotoImage(image)

            self.product_image = self.image_tk
            self.image_path = image_save_path

            img_lavel = tk.Label(self.frameImg, image = self.image_tk)
            img_lavel.place(x=0, y=0, width=200, height=200)

    def articles_combobox (self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.cur.execute("SELECT article FROM articulos")
        self.articulos = [row[0] for row in self.cur.fetchall()]
        self.comboboxbuscar['values'] = self.articulos
   
    def add_article(self):
        top = tk.Toplevel(self)
        top.title("Agregar articulo")
        top.geometry("700x400+200+50")
        top.config(bg="#95c799")
        top.resizable(False, False)

        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()

        tk.Label(top, text="Articulos: ", font="arial 12 bold", bg="#95c799").place(x=20, y=20, width=80, height=25)
        entry_article = tk.Entry(top, font="arial 12 bold")
        entry_article.place(x=120, y=20, width=250, height=30)
        tk.Label(top, text="Precio: ", font="arial 12 bold", bg="#95c799").place(x=20, y=60, width=80, height=25)
        entry_price = tk.Entry(top, font="arial 12 bold")
        entry_price.place(x=120, y=60, width=250, height=30)
        tk.Label(top, text="Costo: ", font="arial 12 bold", bg="#95c799").place(x=20, y=100, width=80, height=25)
        entry_cost = tk.Entry(top, font="arial 12 bold")
        entry_cost.place(x=120, y=100, width=250, height=30)
        tk.Label(top, text="Stock: ", font="arial 12 bold", bg="#95c799").place(x=20, y=140, width=80, height=25)
        entry_stock = tk.Entry(top, font="arial 12 bold")
        entry_stock.place(x=120, y=140, width=250, height=30)
        tk.Label(top, text="Stado: ", font="arial 12 bold", bg="#95c799").place(x=20, y=180, width=80, height=25)
        entry_status = tk.Entry(top, font="arial 12 bold")
        entry_status.place(x=120, y=180, width=250, height=30)

        self.frameImg = tk.Frame(top, bg="white", highlightbackground="gray", highlightthickness=1)
        self.frameImg.place(x=440, y=30, width=200, height=200)

        btnImage = tk.Button(top, text="Cargar imagen", font="arial 12 bold", command=self.load_image)
        btnImage.place(x=470, y=260, width=150, height=40)

        def save_article():
            article = entry_article.get()
            price = entry_price.get()
            cost = entry_cost.get()
            stock = entry_stock.get()
            status = entry_status.get()

            if not article or not price or not cost or not stock or not status:
                messagebox.showerror("Error", "Todos los campos deben de estar completos")
                return
            
            try:
                price = float(price)
                cost = float(cost)
                stock = float(stock)
            except ValueError:
                messagebox.showerror("Error", "Precio, Costo y Stock deben de ser numeros validos")
                return
            
            if hasattr(self, 'image_path'):
                image_path = self.image_path
            else:
                image_path = (r"folder/default.png")

            try:
                self.cur.execute("INSERT INTO articulos (article, price, cost, stock, status, image_path) VALUES (?,?,?,?,?,?)",
                                 (article, price, cost, stock, status, image_path))
                self.con.commit()
                messagebox.showinfo("Exito", "Articulo agregado correctamente")
                top.destroy()
            except sqlite3.Error as e:
                print("Error al cargar el articulo:", e)
                messagebox.showerror("Error", "Error al agregar el articulo")

        tk.Button(top, text="Guardar", font="arial, 12 bold", command=save_article).place(x=50, y=260, width=150, height=40)
        tk.Button(top, text="Cancelar", font="arial, 12 bold", command=top.destroy).place(x=260, y=260, width=150, height=40)
