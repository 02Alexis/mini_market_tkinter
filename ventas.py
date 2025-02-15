import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import threading
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import sys
import os

class Ventas(tk.Frame):
    db_name = 'database.db'

    def __init__(self, padre):
        super().__init__(padre)
        self.number_invoice = self.get_numer_current_invoice()
        self.selected_products = []
        self.widgets()
        self.load_products()
        self.load_clients()
        self.timer_product = None
        self.timer_client = None

    def get_numer_current_invoice(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT MAX(factura) FROM ventas")
            last_invoice_number = c.fetchone()[0]
            conn.close()
            return last_invoice_number + 1 if last_invoice_number is not None else 1
        except sqlite3.Error as e:
            print("Error obteniendo el numero de factura actual:", e)
            return 1

    def load_products(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT article FROM articulos")
            self.products = [product[0] for product in c.fetchall()]
            self.entry_product["values"] = self.products
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando productos:", e)

    def load_clients(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT name FROM clientes")
            clients = c.fetchall()
            self.clients = [client[0] for client in clients]
            self.entry_client["values"] = self.clients
            conn.close()
        except sqlite3.Error as e:
            print("Error cargando clientes:", e)

    def filter_products(self, event):
        if self.timer_product:
            self.timer_product.cancel()
        self.timer_product = threading.Timer(0.5, self.filter_products_)
        self.timer_product.start()

    def filter_products_(self):
        typed = self.entry_product.get()

        if typed == '':
            data = self.products
        else:
            data = [item for item in self.products if typed.lower() in item.lower()]

        if data:
            self.entry_product['values'] = data
            self.entry_product.event_generate('<Down>')
        else:
            self.entry_product['values'] = ["No se encontraron resultados"]
            self.entry_product.event_generate('<Down>')
            self.entry_product.delete(0, tk.END)
            
    def filter_clientes(self, event):
        if self.timer_client:
            self.timer_client.cancel()
        self.timer_client = threading.Timer(0.5, self.filter_clients_)
        self.timer_client.start()

    def filter_clients_(self):
        typed = self.entry_client.get()

        if typed == '':
            data = self.clients
        else:
            data = [item for item in self.clients if typed.lower() in item.lower()]

        if data:
            self.entry_client['values'] = data
            self.entry_client.event_generate('<Down>')
        else:
            self.entry_client['values'] = ["No se encontraron resultados"]
            self.entry_client.event_generate('<Down>')
            self.entry_client.delete(0, tk.END)
            
    def add_article(self):
        client = self.entry_client.get()
        product = self.entry_product.get()
        quantity = self.entry_quantity.get()

        if not client:
            messagebox.showerror("Error", "Por favor seleccione un cliente")

        if not product:
            messagebox.showerror("Error", "Por favor seleccione un producto")

        if not quantity.isdigit() or int(quantity) <= 0:
            messagebox.showerror("Error", "Por favor ingrese una cantidad valida")
            return

        quantity = int(quantity)
        client = self.entry_client.get()          

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT price, cost, stock FROM articulos WHERE article =?", (product,))
            resultado = c.fetchone()

            if resultado is None:
                messagebox.showerror("Error", "Producto no encontrado.")
                return
            price, cost, stock = resultado

            if quantity > stock:
                messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles")

            total = price * quantity
            total_cop = "{:,.0f}".format(total)

            self.tre.insert("", "end", values=(self.number_invoice, client, product, "{:,.0f}".format(price), quantity, total_cop))
            self.selected_products.append((self.number_invoice, client, product, price, quantity, total_cop, cost))
            print(f"Factura: {self.number_invoice}")
            conn.close()

            self.entry_product.set('')
            self.entry_quantity.delete(0, 'end')
        except sqlite3.Error as e:
            print("Error al agregar articulo", e)

        self.calculate_total_price()

    def calculate_total_price(self):
        total_pay = sum(float(str(self.tre.item(item)["values"][-1]).replace(" ", "").replace(",", "")) for item in self.tre.get_children())
        total_pay_cop = "{:,.0f}".format(total_pay)
        self.label_total_price.config(text=f"Precio a pagar: $ {total_pay_cop}")

    def update_stock(self, event=None):
        selected_product = self.entry_product.get()

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM articulos WHERE article =?", (selected_product,))
            stock = c.fetchone()[0]
            conn.close()

            self.label_stock.config(text=f"Stock: {stock}")
        except sqlite3.Error as e:
            print("Error al obtener el stock del producto", e)

    def Make_payment(self):
        if not self.tre.get_children():
            messagebox.showerror("Error", "No hay productos seleccionados para realizar el pago")
            return

        Total_sale = sum(float(item[5].replace(" ", "").replace(",", "")) for item in self.selected_products)
        total_format = "{:,.0f}".format(Total_sale)

        payment_window = tk.Toplevel(self)
        payment_window.title("Realizar pago")
        payment_window.geometry("400x400+450+80")
        payment_window.configure(bg="#95c799")
        payment_window.resizable(False, False)
        payment_window.transient(self.master)
        payment_window.grab_set()
        payment_window.focus_set()
        payment_window.lift()

        label_title = tk.Label(payment_window, text="Realizar pago", font="sans 30 bold", bg="#95c799")
        label_title.place(x=70, y=10)

        label_total = tk.Label(payment_window, text=f"Total a pagar: {total_format}", font="sans 14 bold", bg="#95c799")
        label_total.place(x=80, y=100)

        label_mont = tk.Label(payment_window, text="Ingrese el monto pagado: ", font="sans 14 bold", bg="#95c799")
        label_mont.place(x=80, y=160)

        entry_mont = ttk.Entry(payment_window, font="sans 14 bold")
        entry_mont.place(x=80, y=210, width=240, height=40)

        btn_confirm_payment = tk.Button(payment_window, text="Confirmar pago", font="sans 14 bold", command=lambda: self.process_payment(entry_mont.get(), payment_window, Total_sale))
        btn_confirm_payment.place(x=80, y=270, width=240, height=40)

    def process_payment(self, pait_quantity, payment_window, total_sale):
        pait_quantity = float(pait_quantity)
        client = self.entry_client.get()

        if pait_quantity < total_sale:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
            return
        
        cambio = pait_quantity - total_sale

        total_format = "{:,.0f}".format(total_sale)

        message = f"Total: {total_format} \nCantidad pagada: {pait_quantity:,.0f} \nCambio: {cambio:,.0f}"
        messagebox.showinfo("Pago realizado", message)

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()

            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            current_hour = datetime.datetime.now().strftime("%H:%M:%S")

            for item in self.selected_products:
                factura, client, product, price, quantity, total, cost = item
                c.execute("INSERT INTO ventas (factura, client, article, price, quantity, total, cost, date, hour) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (factura, client, product, price, quantity, total.replace(" ", "").replace(",", ""), cost * quantity, current_date, current_hour))
                c.execute("UPDATE articulos SET stock = stock - ? WHERE article =?", (quantity, product))

            conn.commit()
            
            self.generate_pdf_invoice(total_sale, client)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")

        self.number_invoice += 1
        self.label_number_invoice.config(text=str(self.number_invoice))

        self.selected_products = []
        self.clean_fields()

        payment_window.destroy()

    def clean_fields(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_total_price.config(text="Precio a pagar: $ 0 ")

        self.entry_product.set('')
        self.entry_quantity.delete(0, 'end')

    def clean_list(self):
        self.tre.delete(*self.tre.get_children())
        self.selected_products.clear()
        self.calculate_total_price()
    
    def delete_article(self):
        item_selected = self.tre.selection()
        if not item_selected:
            messagebox.showerror("Error", "No hay ningun articulo seleccionado")
            return
        
        item_id = item_selected[0]
        values_item = self.tre.item(item_id)["values"]
        factura, client, article, price, quantity, total = values_item

        self.tre.delete(item_id)

        self.selected_products = [product for product in self.selected_products if product[2] != article]

        self.calculate_total_price()

    def edit_article(self):
        selected_item = self.tre.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor seleccione un articulo para editar")
            return
        
        item_values = self.tre.item(selected_item[0], 'values')
        if not item_values:
            return
        
        current_product = item_values[2]
        current_quantity = item_values[4]

        new_quantity = simpledialog.askinteger("Editar articulo", "Ingrese la nueva cantidad:", initialvalue=current_quantity)

        if new_quantity is not None:
            try:
                conn = sqlite3.connect(self.db_name)
                c = conn.cursor()
                c.execute("SELECT price, cost, stock FROM articulos WHERE article =?", (current_product,))
                resultado = c.fetchone()

                if resultado is None:
                    messagebox.showerror("Error", "Producto no encontrado")

                price, cost, stock = resultado

                if new_quantity > stock:
                    messagebox.showerror("Error", f"Stock insuficiente. Solo hay {stock} unidades disponibles") 
                    return
                
                total = price * new_quantity
                total_cop = "{:,.0f} ".format(total)

                self.tre.item(selected_item[0], values=(self.number_invoice, self.entry_client.get(), current_product, "{:,.0f} ".format(price), new_quantity, total_cop))

                for idx, product in enumerate(self.selected_products):
                    if product[2] == current_product:
                        self.selected_products[idx] = (self.number_invoice, self.entry_client.get(), current_product, price, new_quantity, total_cop, cost)
                        break
                
                conn.close()

                self.calculate_total_price()

            except sqlite3.Error as e:
                print("Error al editar el articulo: ", e) 

    def see_sales_made(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            ventas = c.fetchall()
            conn.close()
            print("#1 Datos recuperados de la base de datos:", ventas)

            window_sales = tk.Toplevel(self)
            print("Ventana 'window_sales' creada correctamente.") 
            window_sales.title("Ventas realizadas")
            window_sales.geometry("1100x650+120+20")
            window_sales.configure(bg="#95c799")
            window_sales.resizable(False, False)
            window_sales.transient(self.master)
            window_sales.grab_set()
            window_sales.focus_set()
            window_sales.lift()

            def filter_sales():
                invoice_search = entry_invoice.get()
                client_search = entry_client.get()
                for item in tree.get_children():
                    tree.delete(item)

                filtered_sales = [
                    venta for venta in ventas
                    if (str(venta[0]) == invoice_search or not invoice_search) and
                    (venta[1].lower() == client_search.lower() or not client_search)
                ]

                for venta in filtered_sales:
                    venta = list(venta)
                    venta[3] = "{:,.0f}".format(venta[3])
                    venta[5] = "{:,.0f}".format(venta[5])
                    venta[6] = datetime.datetime.strptime(venta[6], "%Y-%m-%d").strftime("%d-%m-%Y")
                    tree.insert("", "end", values=venta)

            label_sales_made = tk.Label(window_sales, text="Ventas realizadas", font="sans 26 bold", bg="#95c799")
            print("Label 'Ventas realizadas' creado correctamente.")
            label_sales_made.place(x=350, y=20)

            filter_frame = tk.Frame(window_sales, bg="#95c799")
            filter_frame.place(x=20, y=60, width=1060, height=60)

            label_invoice = tk.Label(filter_frame, text="Numero de factura", bg="#95c799", font="sans 14 bold")
            label_invoice.place(x=10, y=15)

            entry_invoice = ttk.Entry(filter_frame, font="sans 14 bold")
            entry_invoice.place(x=200, y=10, width=200, height=40)
            
            label_client = tk.Label(filter_frame, text="Cliente", bg="#95c799", font="sans 14 bold")
            label_client.place(x=420, y=15)

            entry_client = ttk.Entry(filter_frame, font="sans 14 bold")
            entry_client.place(x=620, y=10, width=200, height=40)

            btn_filter = tk.Button(filter_frame, text="Filtar", font="sans 14 bold", command=filter_sales)
            btn_filter.place(x=840, y=10)

            tree_frame = tk.Frame(window_sales, bg="white")
            tree_frame.place(x=20, y=130, width=1060, height=500)

            scrol_y = ttk.Scrollbar(tree_frame)
            scrol_y.pack(side=RIGHT, fill=Y)

            scrol_x = ttk.Scrollbar(tree_frame, orient=HORIZONTAL)
            scrol_x.pack(side=BOTTOM, fill=X)

            tree = ttk.Treeview(tree_frame, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora"), show="headings")
            tree.pack(expand=True, fill=BOTH)

            scrol_y.config(command=tree.yview)
            scrol_x.config(command=tree.xview)

            tree.heading("Factura", text="Factura")
            tree.heading("Cliente", text="Cliente")
            tree.heading("Producto", text="Producto")
            tree.heading("Precio", text="Precio")
            tree.heading("Cantidad", text="Cantidad")
            tree.heading("Total", text="Total")
            tree.heading("Fecha", text="Fecha")
            tree.heading("Hora", text="Hora")

            tree.column("Factura", width=60, anchor="center")
            tree.column("Cliente", width=120, anchor="center")
            tree.column("Producto", width=120, anchor="center")
            tree.column("Precio", width=80, anchor="center")
            tree.column("Cantidad", width=80, anchor="center")
            tree.column("Total", width=80, anchor="center")
            tree.column("Fecha", width=80, anchor="center")
            tree.column("Hora", width=80, anchor="center")

            print("#2 Datos recuperados de la base de datos:", ventas)  # Verificar los datos antes del bucle
            if not ventas:
                print("La lista 'ventas' está vacía.")
            for venta in ventas:
                venta = list(venta)
                venta[3] = "{:,.0f}".format(venta[3])
                venta[5] = "{:,.0f}".format(venta[5])
                venta[6] = datetime.datetime.strptime(venta[6], "%Y-%m-%d").strftime("%d-%m-%Y")
                print("Datos a insertar:", venta)
                tree.insert("", "end", values=venta)      

        except sqlite3.Error as e:
            messagebox.showerror("Error", "Error al obtener las ventas: {e}")
    
    def generate_pdf_invoice(self, total_sale, client):
        try:
            invoice_path = f"invoices/Factura_{self.number_invoice}.pdf"
            c = canvas.Canvas(invoice_path, pagesize=letter)

            company_name = "Mini Market"
            company_address = "Porton de la vega"
            company_phone = "+57 1234567890"
            company_email = "minimarket@gmail.com"
            company_website = "www.marketplace.com"

            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.darkgreen)
            c.drawCentredString(300, 750, "Factura de Servicios")

            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 710, f"{company_name}")
            c.setFont("Helvetica", 12)
            c.drawString(50, 690, f"Dirección: {company_address}")
            c.drawString(50, 670, f"Teléfono: {company_phone}")
            c.drawString(50, 650, f"Email: {company_email}")
            c.drawString(50, 630, f"Website: {company_website}")

            c.setLineWidth(0.5)
            c.setStrokeColor(colors.gray)
            c.line(50, 620, 550, 620)

            c.setFont("Helvetica", 12)
            c.drawString(50, 600, f"Número de factura {self.number_invoice}")
            c.drawString(50, 580, f"Fecha {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

            c.line(50, 560, 550, 560)

            c.drawString(50, 540, f"Cliente: {client}")
            c.drawString(50, 520, "Descripción de productos:")

            y_offset = 500
            c.setFont("Helvetica-Bold", 12)
            c.drawString(70, y_offset, "Producto")
            c.drawString(270, y_offset, "Cantidad")
            c.drawString(370, y_offset, "Precio")
            c.drawString(470, y_offset, "Total")

            c.line(50, y_offset - 10, 550, y_offset - 10)
            y_offset -= 30
            c.setFont("Helvetica-Bold", 12)      
            for item in self.selected_products:
                factura, client, product, price, quantity, total, cost = item
                c.drawString(70, y_offset, product)
                c.drawString(270, y_offset, str(quantity))
                c.drawString(370, y_offset, "${:,.0f}".format(price))
                c.drawString(470, y_offset, total)
                y_offset -= 20

            c.line(50, y_offset, 550, y_offset)
            y_offset -= 20

            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.darkgreen)
            c.drawString(50, y_offset, f"Total a pagar: $ {total_sale:,.0f}")
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 12)

            y_offset -= 20
            c.line(50, y_offset, 550, y_offset)

            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, y_offset - 60, "Gracias por su compra")
            
            y_offset -= 100
            c.setFont("Helvetica-Bold", 10)
            c.drawString(50, y_offset, "Términos y Condiciones:")
            c.drawString(50, y_offset - 20, "1. Los productos comprados no tienen devolución")
            c.drawString(50, y_offset - 40, "2. Conserve esta factura como comprobante de su compra")
            c.drawString(50, y_offset - 60, "3. Para más información, visite nuestro sitio web o contacte a servicio al cliente")

            c.save()

            messagebox.showinfo("Factura generada", f"Se ha generado la factura en: {invoice_path}")

            os.startfile(os.path.abspath(invoice_path))

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"No se pudo generar la factura: {e}")
    
    def widgets(self):
        labelframe = tk.LabelFrame(self, font="sans 12 bold", bg="#95c799")
        labelframe.place(x=25, y=30, width=1045, height=180)

        label_client = tk.Label(labelframe, text="Cliente: ", font="sans 14 bold", bg="#95c799")
        label_client.place(x=10, y=11)
        self.entry_client = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_client.place(x=120, y=8, width=260, height=40)
        self.entry_client.bind('<KeyRelease>', self.filter_clientes)

        label_product = tk.Label(labelframe, text="Producto: ", font="sans 14 bold", bg="#95c799")
        label_product.place(x=10, y=70)
        self.entry_product = ttk.Combobox(labelframe, font="sans 14 bold")
        self.entry_product.place(x=120, y=66, width=260, height=40)
        self.entry_product.bind('<KeyRelease>', self.filter_products)

        label_quantity = tk.Label(labelframe, text="Cantidad: ", font="sans 14 bold", bg="#95c799")
        label_quantity.place(x=500, y=11)
        self.entry_quantity = ttk.Entry(labelframe, font="sans 14 bold")
        self.entry_quantity.place(x=610, y=8, width=100, height=40)

        self.label_stock = tk.Label(labelframe, text="Stock: ", font="sans 14 bold", bg="#95c799")
        self.label_stock.place(x=500, y=70)
        self.entry_product.bind("<<ComboboxSelected>>", self.update_stock)

        label_factura = tk.Label(labelframe, text="Númer de Factura: ", font="sans 14 bold", bg="#95c799")
        label_factura.place(x=750, y=11)

        self.label_number_invoice = tk.Label(labelframe, text=f"{self.number_invoice}", font="sans 14 bold", bg="#95c799")
        self.label_number_invoice.place(x=950, y=11)

        add_button = tk.Button(labelframe, text="Agregar Articulo", font="sans 14 bold", command=self.add_article)
        add_button.place(x=90, y=120, width=200, height=40)

        delet_button = tk.Button(labelframe, text="Eliminar Articulo", font="sans 14 bold", command=self.delete_article)
        delet_button.place(x=310, y=120, width=200, height=40)

        edit_button = tk.Button(labelframe, text="Editar Articulo", font="sans 14 bold", command=self.edit_article)
        edit_button.place(x=530, y=120, width=200, height=40)

        clean_button = tk.Button(labelframe, text="Limpiar Lista", font="sans 14 bold", command=self.clean_list)
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

        pay_button = tk.Button(self, text="Pagar", font="sans 14 bold", command=self.Make_payment)
        pay_button.place(x=70, y=550, width=180, height=40)

        see_sale_button = tk.Button(self, text="Ver ventas realizadas", font="sans 14 bold", command=self.see_sales_made)
        see_sale_button.place(x=290, y=550, width=280, height=40)
