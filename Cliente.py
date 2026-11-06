import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from Guardar_Datos import guardar_clientes, modificar_cliente, eliminar_cliente

class ventanaClientes:
    def __init__(self, ventana_principal, volver_menu):
        self.ventana_principal = ventana_principal
        self.volver_menu = volver_menu

        self.id_cliente_seleccionado =  None

        self.ventana = tk.Toplevel(self.ventana_principal)
        self.ventana.title("Datos del Cliente")
        self.ventana.geometry("1125x700")

        self.ventana.protocol("WM_DELETE_WINDOW", self.volver)
        self.crear_interfaz()

    def crear_interfaz(self):
        tk.Label(self.ventana, text="Nombre: ").grid(row = 0, column = 0, padx = 5, pady = 5)
        self.cajaNombre = tk.Entry(self.ventana, width = 30)
        self.cajaNombre.grid(row = 0, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Apellido: ").grid(row = 1, column = 0, padx = 5, pady = 5)
        self.cajaApellido = tk.Entry(self.ventana, width = 30)
        self.cajaApellido.grid(row = 1, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="DNI: ").grid(row = 2, column = 0, padx = 5, pady = 5)
        self.cajaDNI = tk.Entry(self.ventana, width = 30)
        self.cajaDNI.grid(row = 2, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Fecha de nacimiento: ").grid(row = 3, column = 0, padx = 5, pady = 5)
        self.cajaFechaNacimiento = tk.Entry(self.ventana, width = 30)
        self.cajaFechaNacimiento.grid(row = 3, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Telefono: ").grid(row = 4, column = 0, padx = 5, pady = 5)
        self.cajaTelefono = tk.Entry(self.ventana, width = 30)
        self.cajaTelefono.grid(row = 4, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Email: ").grid(row = 5, column = 0, padx = 5, pady = 5)
        self.cajaEmail = tk.Entry(self.ventana, width = 30)
        self.cajaEmail.grid(row = 5, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Direccion: ").grid(row = 6, column = 0, padx = 5, pady = 5)
        self.cajaDireccion = tk.Entry(self.ventana, width = 30)
        self.cajaDireccion.grid(row = 6, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Ciudad: ").grid(row = 7, column = 0, padx = 5, pady = 5)
        self.cajaCiudad = tk.Entry(self.ventana, width = 30)
        self.cajaCiudad.grid(row = 7, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Provincia: ").grid(row = 8, column = 0, padx = 5, pady = 5)
        self.cajaProvincia = tk.Entry(self.ventana, width = 30)
        self.cajaProvincia.grid(row = 8, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Cod Postal: ").grid(row = 9, column = 0, padx = 5, pady = 5)
        self.cajaCodPostal = tk.Entry(self.ventana, width = 30)
        self.cajaCodPostal.grid(row = 9, column = 1, padx = 5, pady = 5)

        tk.Label(self.ventana, text="Fecha de Registro: ").grid(row = 10, column = 0, padx = 5, pady = 5)
        self.fecha_label = tk.Label(self.ventana, text = "", bg = "white", width = 25, relief = "sunken")
        self.fecha_label.grid(row = 10, column = 1, padx = 5 , pady = 5)

        frame_botones = tk.Frame(self.ventana)
        frame_botones.grid(row = 11, column = 0, columnspan= 2, pady = 10)

        botonGuardar = tk.Button(frame_botones, text = "Guardar", command = self.guardar_cliente, bg = "lightblue", width=15)
        botonGuardar.pack(side = "left", padx = 5)

        botonEliminar = tk.Button(frame_botones, text = "eliminar cliente", command = self.eliminar_cliente)
        botonEliminar.pack(side = "left", padx = 5)

        botonModificar = tk.Button(frame_botones, text = "modificar cliente", command = self.modificar_Cliente)
        botonModificar.pack(side = "left", padx = 5)

        boton_volver = tk.Button(frame_botones, text = "Volver", command = self.volver, width = 15)
        boton_volver.pack(side = "left", padx = 5)

        columnas = (
                    "ID",
                    "Nombre",
                    "Apellido",
                    "Dni",
                    "fecha_nacimiento",
                    "Telefono",
                    "Email",
                    "Direccion",
                    "Ciudad",
                    "Provincia",
                    "Codigo Postal",
                    "Fecha de registro"
                    )

        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=11)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=100)

        self.tabla.column("ID", width=0, stretch=False)
        self.tabla.heading("ID", text="")

        self.tabla.grid(row = 12, column = 0, columnspan = 2, padx = 11, pady = 11)

        self.tabla.bind("<<TreeviewSelect>>", lambda event: self.seleccionar_cliente())


    def guardar_cliente(self):

        nombre = self.cajaNombre.get()
        apellido = self.cajaApellido.get()
        dni = self.cajaDNI.get()
        fecha_nacimiento = self.cajaFechaNacimiento.get()
        telefono = self.cajaTelefono.get()
        email = self.cajaEmail.get()
        direccion = self.cajaDireccion.get()
        ciudad = self.cajaCiudad.get()
        provincia = self.cajaProvincia.get()
        codPostal = self.cajaCodPostal.get()

        partes = fecha_nacimiento.split("/")
        if len(partes) == 3:
            fecha_nacimiento = partes[2] + "-" + partes[1] + "-" + partes[0]
        fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.fecha_label.config(text = fecha_registro)

        datos = (
            nombre,
            apellido,
            dni,
            fecha_nacimiento,
            telefono,
            email,
            direccion,
            ciudad,
            provincia,
            codPostal,
            fecha_registro
        )

        idClientes = guardar_clientes(datos)

        self.tabla.insert("", "end", values=(
            idClientes,
            nombre,
            apellido,
            dni,
            fecha_nacimiento,
            telefono,
            email,
            direccion,
            ciudad,
            provincia,
            codPostal,
            fecha_registro
        ))

        self.cajaNombre.delete(0, tk.END)
        self.cajaApellido.delete(0, tk.END)
        self.cajaDNI.delete(0, tk.END)
        self.cajaFechaNacimiento.delete(0, tk.END)
        self.cajaTelefono.delete(0, tk.END)
        self.cajaEmail.delete(0, tk.END)
        self.cajaDireccion.delete(0, tk.END)
        self.cajaCiudad.delete(0, tk.END)
        self.cajaProvincia.delete(0, tk.END)
        self.cajaCodPostal.delete(0, tk.END)

        self.limpiar_cajas()


    def eliminar_cliente(self):

        seleccion = self.tabla.selection()

        if seleccion:

            confirmar = messagebox.askyesno("Eliminar cliente", "¿Estas seguro de eliminar al cliente?")

            if confirmar:

                eliminar_cliente(self.id_cliente_seleccionado)

                self.tabla.delete(seleccion)

                self.limpiar_cajas()

                self.id_cliente_seleccionado = None

    def seleccionar_cliente(self):

        seleccion = self.tabla.selection()

        if seleccion:

            valores = self.tabla.item(seleccion[0], "values")

            self.id_cliente_seleccionado = valores[0]
            self.cajaNombre.delete(0, tk.END)
            self.cajaNombre.insert(0, valores[1])
            self.cajaApellido.delete(0, tk.END)
            self.cajaApellido.insert(0, valores[2])
            self.cajaDNI.delete(0, tk.END)
            self.cajaDNI.insert(0, valores[3])
            self.cajaFechaNacimiento.delete(0, tk.END)
            self.cajaFechaNacimiento.insert(0, valores[4])
            self.cajaTelefono.delete(0, tk.END)
            self.cajaTelefono.insert(0, valores[5])
            self.cajaEmail.delete(0, tk.END)
            self.cajaEmail.insert(0, valores[6])
            self.cajaDireccion.delete(0, tk.END)
            self.cajaDireccion.insert(0, valores[7])
            self.cajaCiudad.delete(0, tk.END)
            self.cajaCiudad.insert(0, valores[8])
            self.cajaProvincia.delete(0, tk.END)
            self.cajaProvincia.insert(0, valores[9])
            self.cajaCodPostal.delete(0, tk.END)
            self.cajaCodPostal.insert(0, valores[10])
            self.fecha_label.config(text = valores[11])

            return seleccion


    def modificar_Cliente(self):

        seleccion = self.tabla.selection()

        if seleccion:
            nombre = self.cajaNombre.get()
            apellido = self.cajaApellido.get()
            dni = self.cajaDNI.get()
            fecha_nacimiento = self.cajaFechaNacimiento.get()
            telefono = self.cajaTelefono.get()
            email = self.cajaEmail.get()
            direccion = self.cajaDireccion.get()
            ciudad = self.cajaCiudad.get()
            provincia = self.cajaProvincia.get()
            codPostal = self.cajaCodPostal.get()

            datos = (
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                telefono,
                email,
                direccion,
                ciudad,
                provincia,
                codPostal,
            )

            modificar_cliente(self.id_cliente_seleccionado, datos)

            self.tabla.item(seleccion[0], values=(
                self.id_cliente_seleccionado,
                nombre,
                apellido,
                dni,
                fecha_nacimiento,
                telefono,
                email,
                direccion,
                ciudad,
                provincia,
                codPostal,
                self.fecha_label.cget("text")
            ))
            self.limpiar_cajas()

            self.id_cliente_seleccionado = None

    def volver(self):
        self.ventana.destroy()
        self.volver_menu()

    def limpiar_cajas(self):

        self.cajaNombre.delete(0, tk.END)
        self.cajaApellido.delete(0, tk.END)
        self.cajaDNI.delete(0, tk.END)
        self.cajaFechaNacimiento.delete(0, tk.END)
        self.cajaTelefono.delete(0, tk.END)
        self.cajaEmail.delete(0, tk.END)
        self.cajaDireccion.delete(0, tk.END)
        self.cajaCiudad.delete(0, tk.END)
        self.cajaProvincia.delete(0, tk.END)
        self.cajaCodPostal.delete(0, tk.END)