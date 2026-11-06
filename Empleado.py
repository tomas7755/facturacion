import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Guardar_Datos import guardar_empleado, modificar_empleado, eliminar_empleado

class ventana_empleado:
    def __init__(self, ventana_principal, volver_menu):
        self.ventana_principal = ventana_principal
        self.volver_menu = volver_menu

        self.id_empleado_seleccionado = None

        self.ventana = tk.Toplevel(self.ventana_principal)
        self.ventana.title("Datos del empleado: ")
        self.ventana.geometry("1020x650")

        self.ventana.protocol("WM_DELETE_WINDOW", volver_menu)

        self.crear_interfaz()

    def crear_interfaz(self):

        tk.Label(self.ventana, text="Nombre: ").grid(row=0, column=0, padx=5, pady=5)
        self.cajaNombre = tk.Entry(self.ventana, width=30)
        self.cajaNombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="Apellido: ").grid(row=1, column=0, padx=5, pady=5)
        self.cajaApellido = tk.Entry(self.ventana, width=30)
        self.cajaApellido.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="DNI: ").grid(row=2, column=0, padx=5, pady=5)
        self.cajaDNI = tk.Entry(self.ventana, width=30)
        self.cajaDNI.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="Fecha de nacimiento: ").grid(row=3, column=0, padx=5, pady=5)
        self.cajaFechaNacimiento = tk.Entry(self.ventana, width=30)
        self.cajaFechaNacimiento.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="Telefono: ").grid(row=4, column=0, padx=5, pady=5)
        self.cajaTelefono = tk.Entry(self.ventana, width=30)
        self.cajaTelefono.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="Email: ").grid(row=5, column=0, padx=5, pady=5)
        self.cajaEmail = tk.Entry(self.ventana, width=30)
        self.cajaEmail.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="Legajo: ").grid(row=6, column=0, padx=5, pady=5)
        self.cajaLegajo = tk.Entry(self.ventana, width=30)
        self.cajaLegajo.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="Puesto: ").grid(row=7, column=0, padx=5, pady=5)
        self.cajaPuesto = tk.Entry(self.ventana, width=30)
        self.cajaPuesto.grid(row=7, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="Salario: ").grid(row=8, column=0, padx=5, pady=5)
        self.cajaSalario = tk.Entry(self.ventana, width=30)
        self.cajaSalario.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(self.ventana, text="Fecha de Contratacion: ").grid(row=9, column=0, padx=5, pady=5)
        self.fecha_label = tk.Label(self.ventana, text="", bg="white", width=25, relief="sunken")
        self.fecha_label.grid(row=9, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.ventana)
        frame_botones.grid(row=11, column=0, columnspan=2, pady=10)

        botonGuardar = tk.Button(frame_botones, text = "Guardar", command=self.guardar_empleado, bg="lightblue", width=15)
        botonGuardar.pack(side = "left", padx=5)

        botonEliminar = tk.Button(frame_botones, text="eliminar venta", command=self.eliminar_empleado)
        botonEliminar.pack(side="left", padx=5)

        botonModificar = tk.Button(frame_botones, text="modificar venta", command=self.modificar_empleado)
        botonModificar.pack(side="left", padx=5)

        botonVolver = tk.Button(frame_botones, text = "Volver", command=self.volver, bg="lightblue", width=15)
        botonVolver.pack(side="left", padx=5)

        columnas = ("ID",
                    "Nombre",
                    "Apellido",
                    "Dni",
                    "Fecha de nacimiento",
                    "Telefono",
                    "Email",
                    "Legajo",
                    "Puesto",
                    "Salario",
                    "Fecha de Contratacion"
                    )

        self.tabla = ttk.Treeview(self.ventana, columns=columnas, show="headings", height=11)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=100)

        self.tabla.column("ID", width=0, stretch=False)
        self.tabla.heading("ID", text="")

        self.tabla.grid(row=10, column=0, columnspan=2, padx=11, pady=11)

        self.tabla.bind("<<TreeviewSelect>>", lambda event: self.seleccionar_empleado())


    def guardar_empleado(self):
        nombre = self.cajaNombre.get()
        apellido = self.cajaApellido.get()
        dni = self.cajaDNI.get()
        fechaNacimiento = self.cajaFechaNacimiento.get()
        telefono = self.cajaTelefono.get()
        email = self.cajaEmail.get()
        legajo = self.cajaLegajo.get()
        puesto = self.cajaPuesto.get()
        salario = self.cajaSalario.get()
        fecha_contratacion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.fecha_label.config(text=fecha_contratacion)

        datos = (
            nombre,
            apellido,
            dni,
            fechaNacimiento,
            telefono,
            email,
            legajo,
            puesto,
            salario,
            fecha_contratacion
        )

        idEmpleado = guardar_empleado(datos)

        self.tabla.insert("", "end", values=(
            idEmpleado,
            nombre,
            apellido,
            dni,
            fechaNacimiento,
            telefono,
            email,
            legajo,
            puesto,
            salario,
            fecha_contratacion
        ))

        self.cajaNombre.delete(0, tk.END)
        self.cajaApellido.delete(0, tk.END)
        self.cajaDNI.delete(0, tk.END)
        self.cajaFechaNacimiento.delete(0, tk.END)
        self.cajaTelefono.delete(0, tk.END)
        self.cajaEmail.delete(0, tk.END)
        self.cajaLegajo.delete(0, tk.END)
        self.cajaPuesto.delete(0, tk.END)
        self.cajaSalario.delete(0, tk.END)

        self.limpiar_cajas()

    def eliminar_empleado(self):

        seleccion = self.tabla.selection()

        if seleccion:

            confirmar = messagebox.askyesno("Eliminar cliente", "¿Esta seguro que desea eliminar al empleado?")

            if confirmar:

                eliminar_empleado(self.id_empleado_seleccionado)

                self.tabla.delete(seleccion)

                self.limpiar_cajas()

                self.id_empleado_seleccionado = None


    def seleccionar_empleado(self):

        seleccion = self.tabla.selection()

        if seleccion:

            valores = self.tabla.item(seleccion[0], "values")

            self.id_empleado_seleccionado = valores[0]
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
            self.cajaLegajo.delete(0, tk.END)
            self.cajaLegajo.insert(0, valores[7])
            self.cajaPuesto.delete(0, tk.END)
            self.cajaPuesto.insert(0, valores[8])
            self.cajaSalario.delete(0, tk.END)
            self.cajaSalario.insert(0, valores[9])
            self.fecha_label.config(text = valores[10])

            return seleccion


    def modificar_empleado(self):

        seleccion = self.tabla.selection()

        if seleccion:
            nombre = self.cajaNombre.get()
            apellido = self.cajaApellido.get()
            dni = self.cajaDNI.get()
            fechaNacimiento = self.cajaFechaNacimiento.get()
            telefono = self.cajaTelefono.get()
            email = self.cajaEmail.get()
            legajo = self.cajaLegajo.get()
            puesto = self.cajaPuesto.get()
            salario = self.cajaSalario.get()

            datos = (
                nombre,
                apellido,
                dni,
                fechaNacimiento,
                telefono,
                email,
                legajo,
                puesto,
                salario
            )

            modificar_empleado(self.id_empleado_seleccionado, datos)

            self.tabla.item(seleccion[0], values=(
                self.id_empleado_seleccionado,
                nombre,
                apellido,
                dni,
                fechaNacimiento,
                telefono,
                email,
                legajo,
                puesto,
                salario,
                self.fecha_label.cget("text")
            ))

            self.limpiar_cajas()

            self.id_empleado_seleccionado = None

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
        self.cajaLegajo.delete(0, tk.END)
        self.cajaPuesto.delete(0, tk.END)
        self.cajaSalario.delete(0, tk.END)
