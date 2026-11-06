import tkinter as tk
from tkinter import ttk, messagebox
from Guardar_Datos import guardar_proveedor, modificar_proveedor, eliminar_proveedor

class ver_proovedor:
    def __init__(self, ventana_principal, volver_menu):

        self.ventana_principal = ventana_principal
        self.volver_menu = volver_menu

        self.id_proveedor_seleccionado = None

        self.ventana = tk.Toplevel(self.ventana_principal)
        self.ventana.title('Datos proovedor')
        self.ventana.geometry('1020x650')

        self.ventana.protocol("WM_DELETE_WINDOW", self.volver_menu)

        self.crear_interfaz()

    def crear_interfaz(self):

        tk.Label(self.ventana, text = "Nombre del Trabajador").grid(row=0, column=0, padx=10, pady=10)
        self.cajaNombreProveedor = tk.Entry(self.ventana, width=20)
        self.cajaNombreProveedor.grid(row=0, column=1, padx=10, pady=10)

        frame_botones = tk.Frame(self.ventana)
        frame_botones.grid(row=11, column=0, columnspan=2, pady=10)

        Boton_guardar = tk.Button(frame_botones, text="Guardar", command=self.guardar_proveedor, bg = "lightblue", width = 15)
        Boton_guardar.pack(side = "left", pady=10)

        Boton_Eliminar = tk.Button(frame_botones, text = "Eliminar", command = self.eliminar_Proveedor, bg = "lightblue", width = 15)
        Boton_Eliminar.pack(side = "left", pady=10)

        Boton_Modificar = tk.Button(frame_botones, text = "Modificar", command = self.modificar_proveedor, bg = "lightblue", width = 15)
        Boton_Modificar.pack(side = "left", pady=10)

        Boton_volver = tk.Button(frame_botones, text = "Volver", command = self.volver, bg = "lightblue", width = 15)
        Boton_volver.pack(side = "left", pady=10)

        columnas = (
            "ID",
            "Nombre del proveedor"
        )

        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=15)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())

            self.tabla.column(col, width=105)

        self.tabla.column("ID", width=0, stretch=False)
        self.tabla.heading("ID", text="")

        self.tabla.grid(row=10, column=1, columnspan=2, pady=11)

        self.tabla.bind("<<TreeviewSelect>>", lambda event: self.seleccionar_proveedor())

    def guardar_proveedor(self):
        nombreProveedor = self.cajaNombreProveedor.get()

        datos = (
            nombreProveedor,
        )

        idProveedor = guardar_proveedor(datos)

        self.tabla.insert("", "end", values=(
            idProveedor,
            nombreProveedor
        )
        )

        self.cajaNombreEmpleado.delete(0, "end")

        self.limpiar_cajas()

    def modificar_proveedor(self):

        seleccion = self.tabla.selection()

        if seleccion:
            nombreProveedor = self.cajaNombreProveedor.get()

            datos = (
                nombreProveedor,
            )

            modificar_proveedor(self.id_proveedor_seleccionado, datos)

            self.tabla.item(seleccion[0], values=(
                self.id_proveedor_seleccionado,
                nombreProveedor
            ))

            self.limpiar_cajas()
            self.id_proveedor_seleccionado = None

    def seleccionar_proveedor(self):

        seleccion = self.tabla.selection()

        if seleccion:

            valores = self.tabla.item(seleccion[0], "values")

            self.id_proveedor_seleccionado = valores[0]
            self.cajaNombreProveedor.delete(0, tk.END)
            self.cajaNombreProveedor.insert(0, valores[1])

            return seleccion

    def eliminar_Proveedor(self):

        seleccion = self.tabla.selection()

        if seleccion:

            confirmar = messagebox.askyesno("Eliminar Proveedor", "¿Esta seguro que desea eliminar proveedor?")

            if confirmar:

                eliminar_proveedor(self.id_proveedor_seleccionado)

                self.tabla.delete(seleccion)

                self.limpiar_cajas()

                self.id_proveedor_seleccionado = None

    def volver (self):
        self.ventana.destroy()
        self.volver_menu()

    def limpiar_cajas(self):

        self.cajaNombreProveedor.delete(0, tk.END)
