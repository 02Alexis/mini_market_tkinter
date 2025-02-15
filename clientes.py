import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox

class Clientes(tk.Frame):
    db_name = "database.db"

    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        self.load_records()

    def validate_field(self):
        if not self.name.get() or not self.document.get() or not self.phone.get() or not self.address.get() or not self.email.get():
            messagebox.showerror("Error", "Todos los campos son requeridos.")
            return False
        return True
    
    def register(self):
        if not self.validate_field():
            return
        
        name = self.name.get()
        document = self.document.get()
        phone = self.phone.get()
        address = self.address.get()
        email = self.email.get()

        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO clientes (name, document, phone, address, email) VALUES (?,?,?,?,?)",
                           (name, document, phone, address, email))
            conn.commit()
            conn.close()
            messagebox.showinfo("Exito", "Cliente registrado correctamente")
            self.clean_treeview()
            self.clean_fields()
            self.load_records()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

    def load_records(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes")
            rows = cursor.fetchall()
            for row in rows:
                self.tre.insert("", "end", values=row)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

    def clean_treeview(self):
        for item in self.tre.get_children():
            self.tre.delete(item)

    def clean_fields(self):
        self.name.delete(0, END)
        self.document.delete(0, END)
        self.phone.delete(0, END)
        self.address.delete(0, END)
        self.email.delete(0, END)

    def modify(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Por favor seleccione un cliente para modificar.")
            return
        
        item = self.tre.selection()[0]
        id_client = self.tre.item(item, "values")[0]
    
        current_name = self.tre.item(item, "values")[1]
        current_document = self.tre.item(item, "values")[2]
        current_phone = self.tre.item(item, "values")[3]
        current_address = self.tre.item(item, "values")[4]
        current_email = self.tre.item(item, "values")[5]

        top_modify = tk.Toplevel(self)
        top_modify.title("Modificar Cliente")
        top_modify.geometry("400x400+400+50")
        top_modify.configure(bg="#95c799")
        top_modify.resizable(False, False)
        top_modify.transient(self.master)
        top_modify.grab_set()
        top_modify.focus_set()
        top_modify.lift()

        tk.Label(top_modify, text="Nombre", font="sans 14 bold", bg="#95c799").grid(row=0, column=0, padx=10, pady=5)
        new_name = tk.Entry(top_modify, font="sans 14 bold")
        new_name.insert(0, current_name)
        new_name.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top_modify, text="Cédula", font="sans 14 bold", bg="#95c799").grid(row=1, column=0, padx=10, pady=5)
        new_document = tk.Entry(top_modify, font="sans 14 bold")
        new_document.insert(0, current_document)
        new_document.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top_modify, text="Telefono", font="sans 14 bold", bg="#95c799").grid(row=2, column=0, padx=10, pady=5)
        new_phone = tk.Entry(top_modify, font="sans 14 bold")
        new_phone.insert(0, current_phone)
        new_phone.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(top_modify, text="Dirección", font="sans 14 bold", bg="#95c799").grid(row=3, column=0, padx=10, pady=5)
        new_address = tk.Entry(top_modify, font="sans 14 bold")
        new_address.insert(0, current_address)
        new_address.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(top_modify, text="Correo", font="sans 14 bold", bg="#95c799").grid(row=4, column=0, padx=10, pady=5)
        new_email = tk.Entry(top_modify, font="sans 14 bold")
        new_email.insert(0, current_email)
        new_email.grid(row=4, column=1, padx=10, pady=5)

        def save_modifys():
            name_new = new_name.get()
            document_new = new_document.get()
            phone_new = new_phone.get()
            address_new = new_address.get()
            email_new = new_email.get()

            try:
                conn = sqlite3.connect(self.db_name)
                cursor = conn.cursor()
                cursor.execute("""UPDATE clientes SET name = ?, document = ?, phone = ?, address = ?, email = ? WHERE id = ? """,
                               (name_new, document_new, phone_new, address_new, email_new, id_client))
                conn.commit()
                conn.close()
                messagebox.showinfo("Exito", "Cliente modificado correctamente.")
                self.clean_treeview()
                self.load_records()
                top_modify.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se puedo modificar el cliente: {e}")

        btn_save = tk.Button(top_modify, text="Guardar cambios", command=save_modifys, font="sans 14 bold")
        btn_save.grid(row=5, column=0, columnspan=2, pady=20)
    
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

        btn1 = Button(self.labelframe, fg="Black", text="Guardar", font="sans 16 bold", command=self.register)
        btn1.place(x=10, y=420, width=220, height=40)

        btn2 = Button(self.labelframe, fg="Black", text="Modificar", font="sans 16 bold", command=self.modify)
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
