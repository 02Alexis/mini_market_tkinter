from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class Ventas(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def widgets(self):
        labelframe = tk.LabelFrame(self, font="sans 12 bold", bg="#95c799")
        labelframe.place(x=25, y=30, width=1045, height=180)

        label_client = tk.Label(labelframe, text="Cliente: ", font="sans 14 bold", bg="#95c799")
        label_client.place(x=10, y=11)
        self.entry_client = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_client.place(x=120, y=8, width=260, height=40)

        label_product = tk.Label(labelframe, text="Producto: ", font="sans 14 bold", bg="#95c799")
        label_product.place(x=10, y=70)
        self.entry_product = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_product.place(x=120, y=66, width=260, height=40)

        label_quantity = tk.Label(labelframe, text="Cantidad: ", font="sans 14 bold", bg="#95c799")
        label_quantity.place(x=500, y=11)
        self.entry_quantity = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_quantity.place(x=610, y=8, width=100, height=40)

        self.label_stock = tk.Label(labelframe, text="Stock: ", font="sans 14 bold", bg="#95c799")
        self.label_stock.place(x=500, y=70)

        label_factura = tk.Label(labelframe, text="Factura: ", font="sans 14 bold", bg="#95c799")
        label_factura.place(x=750, y=11)

        add_button = tk.Button(labelframe, text="Agregar Articulo", font="sans 14 bold")
        add_button.place(x=90, y=120, width=200, height=40)

        delet_button = tk.Button(labelframe, text="Eliminar Articulo", font="sans 14 bold")
        delet_button.place(x=310, y=120, width=200, height=40)

        edit_button = tk.Button(labelframe, text="Editar Articulo", font="sans 14 bold")
        edit_button.place(x=530, y=120, width=200, height=40)

        clean_button = tk.Button(labelframe, text="Limpiar Lista", font="sans 14 bold")
        clean_button.place(x=750, y=120, width=200, height=40)

        treFrame = tk.Frame(self, bg="white")
        treFrame.place(x=70, y=220, width=980, height=300)

        scrol_y = ttk.Scrollbar(treFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Cliente", text="Cliente")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("Cantidad", text="Cantidad")
        self.tre.heading("Total", text="Total")

        self.tre.column("Factura", width=70, anchor="center")
        self.tre.column("Cliente", width=250, anchor="center")
        self.tre.column("Producto", width=250, anchor="center")
        self.tre.column("Precio", width=120, anchor="center")
        self.tre.column("Cantidad", width=120, anchor="center")
        self.tre.column("Total", width=150, anchor="center")

        self.label_total_price = tk.Label(self, text="Precio a pagar: $ 0", bg="#95c799", font="sans 18 bold")
        self.label_total_price.place(x=680, y=550)

        pay_button = tk.Button(self, text="Pagar", font="sans 14 bold")
        pay_button.place(x=70, y=550, width=180, height=40)

        see_sale_button = tk.Button(self, text="Ver ventas realizadas", font="sans 14 bold")
        see_sale_button.place(x=290, y=550, width=280, height=40)
