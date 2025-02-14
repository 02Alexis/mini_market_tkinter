from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Clientes(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()

    def widgets(self):
        self.labelframe = tk.LabelFrame(self, text="Clientes", font="sans 20 bold", bg="#95c799")
        self.labelframe.place(x=20, y=20, width=250, height=560)

        lblname = tk.Label(self.labelframe, text="Nombre: ", font="sans 12 bold", bg="#95c799")
        lblname.place(x=10, y=20)
        self.name = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.name.place(x=10, y=50, width=220, height=40)

        lbldocument  = tk.Label(self.labelframe, text="Cédula: ", font="sans 12 bold", bg="#95c799")
        lbldocument.place(x=10, y=100)
        self.document  = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.document.place(x=10, y=130, width=220, height=40)

        lblphone  = tk.Label(self.labelframe, text="Telefono: ", font="sans 12 bold", bg="#95c799")
        lblphone.place(x=10, y=180)
        self.phone  = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.phone.place(x=10, y=210, width=220, height=40)

        lbladdress  = tk.Label(self.labelframe, text="Dirección: ", font="sans 12 bold", bg="#95c799")
        lbladdress.place(x=10, y=260)
        self.address  = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.address.place(x=10, y=290, width=220, height=40)

        lblemail  = tk.Label(self.labelframe, text="Correo: ", font="sans 12 bold", bg="#95c799")
        lblemail.place(x=10, y=340)
        self.email  = ttk.Entry(self.labelframe, font="sans 14 bold")
        self.email.place(x=10, y=370, width=220, height=40)

        btn1 = Button(self.labelframe, fg="Black", text="Guardar", font="sans 16 bold")
        btn1.place(x=10, y=420, width=220, height=40)

        btn2 = Button(self.labelframe, fg="Black", text="Modificar", font="sans 16 bold")
        btn2.place(x=10, y=470, width=220, height=40)

        treeFrame = Frame(self, bg="white")
        treeFrame.place(x=280, y=20, width=800, height=560)

        scrol_y = ttk.Scrollbar(treeFrame)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x = ttk.Scrollbar(treeFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tre = ttk.Treeview(treeFrame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=("ID", "Nombre", "Cédula", "Telefono", "Dirección", "Correo"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)

        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)

        self.tre.heading("ID", text="ID")
        self.tre.heading("Nombre", text="Nombre")
        self.tre.heading("Cédula", text="Cédula")
        self.tre.heading("Telefono", text="Telefono")
        self.tre.heading("Dirección", text="Dirección")
        self.tre.heading("Correo", text="Correo")

        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("Nombre", width=150, anchor="center")
        self.tre.column("Cédula", width=120, anchor="center")
        self.tre.column("Telefono", width=120, anchor="center")
        self.tre.column("Dirección", width=200, anchor="center")
        self.tre.column("Correo", width=200, anchor="center")
