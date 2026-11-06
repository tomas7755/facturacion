import tkinter as tk
from tkinter import ttk, messagebox
from Guardar_Datos import guardar_stock, modificar_stock, eliminar_stock
from datetime import datetime

class ver_stock:

    def __init__(self, ventana_principal, volver_menu):

        self.ventana_principal = ventana_principal
        self.volver_menu = volver_menu

        self.id_stock_seleccionado = None

        self.ventana = tk.Toplevel(self.ventana_principal)
        self.ventana.title("Datos stock")
        self.ventana.geometry("1020x650")

        self.ventana.protocol("WM_DELETE_WINDOW", self.volver)

        self.crear_interfaz()

    def crear_interfaz(self):

        tk.Label(self.ventana,text="Nombre del producto: ").grid(row = 0, column = 0, padx = 5, pady = 5)
        self.cajaNombreProducto = tk.Entry(self.ventana, width = 30)
        self.cajaNombreProducto.grid(row = 0, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Cantidad en stock: ").grid(row = 1, column = 0, padx = 5, pady = 5)
        self.cajaCantidad = tk.Entry(self.ventana, width = 30)
        self.cajaCantidad.grid(row = 1, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Precio: ").grid(row = 2, column = 0, padx = 5, pady = 5)
        self.cajaPrecio = tk.Entry(self.ventana, width = 30)
        self.cajaPrecio.grid(row = 2, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana,text="Proveedor:").grid(row = 3, column = 0, padx = 5, pady = 5)
        self.cajaProveedor = tk.Entry(self.ventana,width = 30)
        self.cajaProveedor.grid(row = 3,column = 1,padx = 5,pady = 5)

        tk.Label(self.ventana,text="Marca:").grid(row = 4, column = 0, padx = 5, pady = 5)
        self.cajaMarca = tk.Entry(self.ventana,width = 30)
        self.cajaMarca.grid(row = 4,column = 1,padx = 5,pady = 5)

        frame_botones = tk.Frame(self.ventana)

        frame_botones.grid(row = 11,column = 0,columnspan = 2,pady = 10)

        botonGuardar = tk.Button(frame_botones,text = "Guardar",command = self.guardar_stock,bg = "lightblue",width = 15)
        botonGuardar.pack(side = "left", padx = 5)

        botonEliminar = tk.Button(frame_botones, text = "Eliminar stock",command = self.eliminar_stock)
        botonEliminar.pack(side = "left",padx = 5)

        botonModificar = tk.Button(frame_botones, text = "Modificar stock", command = self.modificar_stock)
        botonModificar.pack( side = "left", padx = 5)

        botonVolver = tk.Button(frame_botones, text = "Volver", command = self.volver, bg = "lightblue", width = 15)
        botonVolver.pack(side = "left", padx = 5)

        columnas = (
            "ID",
            "Nombre de producto",
            "Cantidad",
            "Precio",
            "Proveedor",
            "Marca",
            "Fecha de ingreso"
        )

        self.tabla = ttk.Treeview(self.ventana, columns = columnas, show = "headings", height = 15)

        for col in columnas:

            self.tabla.heading(col,text = col.capitalize())
            self.tabla.column(col,width = 100)

        self.tabla.column("ID", width=0, stretch=False)
        self.tabla.heading("ID", text="")

        self.tabla.grid(row = 10,column = 0,columnspan = 2,pady = 11)

        self.tabla.bind("<<TreeviewSelect>>",lambda event: self.seleccionar_stock())

    def guardar_stock(self):

        nombreProducto = self.cajaNombreProducto.get()
        cantidad = self.cajaCantidad.get()
        precio = self.cajaPrecio.get()
        proveedor = self.cajaProveedor.get()
        marca = self.cajaMarca.get()

        fecha_ingreso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        datos = (
            nombreProducto,
            cantidad,
            precio,
            proveedor,
            marca,
            fecha_ingreso
        )

        idStock = guardar_stock(datos)

        self.tabla.insert("","end",values=(
                idStock,
                nombreProducto,
                cantidad,
                precio,
                proveedor,
                marca,
                fecha_ingreso
            )
        )

        self.limpiar_cajas()

    def seleccionar_stock(self):

        seleccion = self.tabla.selection()

        if seleccion:

            valores = self.tabla.item(seleccion[0],"values")

            self.id_stock_seleccionado = valores[0]

            self.cajaNombreProducto.delete(0,tk.END)
            self.cajaNombreProducto.insert(0,valores[1])

            self.cajaCantidad.delete(0,tk.END)
            self.cajaCantidad.insert(0,valores[2])

            self.cajaPrecio.delete(0,tk.END)
            self.cajaPrecio.insert(0,valores[3])

            self.cajaProveedor.delete(0,tk.END)
            self.cajaProveedor.insert(0,valores[4])

            self.cajaMarca.delete(0,tk.END)
            self.cajaMarca.insert(0,valores[5])

            return seleccion

    def modificar_stock(self):

        seleccion = self.tabla.selection()

        if seleccion:

            valores_actuales = self.tabla.item(seleccion[0],"values")

            nombreProducto = self.cajaNombreProducto.get()
            cantidad = self.cajaCantidad.get()
            precio = self.cajaPrecio.get()
            proveedor = self.cajaProveedor.get()
            marca = self.cajaMarca.get()
            fecha_ingreso = valores_actuales[6]

            datos = (
                nombreProducto,
                cantidad,
                precio,
                proveedor,
                marca,
                fecha_ingreso
            )

            modificar_stock(self.id_stock_seleccionado, datos)

            self.tabla.item(
                seleccion[0],
                values=(
                    self.id_stock_seleccionado,
                    nombreProducto,
                    cantidad,
                    precio,
                    proveedor,
                    marca,
                    fecha_ingreso
                )
            )

            self.limpiar_cajas()
            self.id_stock_seleccionado = None

    def volver(self):

        self.ventana.destroy()
        self.volver_menu()

    def eliminar_stock(self):

        seleccion = self.tabla.selection()

        if seleccion:

            confirmar = messagebox.askyesno("Eliminar Stock", "¿Esta seguro de eliminar el stock?")

            if confirmar:

                eliminar_stock(self.id_stock_seleccionado)

                self.tabla.delete(seleccion)

                self.limpiar_cajas()

                self.id_stock_seleccionado = None

    def limpiar_cajas(self):

        self.cajaNombreProducto.delete(0,tk.END)

        self.cajaCantidad.delete(0,tk.END)

        self.cajaPrecio.delete(0,tk.END)

        self.cajaProveedor.delete(0,tk.END)

        self.cajaMarca.delete(0,tk.END)