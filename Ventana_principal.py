import tkinter as tk
from tkinter import messagebox
from Cliente import ventanaClientes
from Empleado import ventana_empleado
from Factura import facturacion
from Stock import ver_stock
from Proovedor import ver_proovedor

class menu_principal:
    def __init__(self, ventana_login, rol):
        self.ventana_login = ventana_login
        self.rol = rol
        self.ventana = tk.Toplevel(ventana_login)
        self.ventana.title("Sistema de gestion - Menu Principal")
        self.ventana.geometry("1000x1000")
        self.ventana.resizable(False, False)
        self.centrar_ventana()
        self.crear_menu()

    def centrar_ventana(self):
        self.ventana.update_idletasks()
        width = 1000
        height = 700
        x = (self.ventana.winfo_screenwidth() // 2) - (width // 2)
        y = (self.ventana.winfo_screenheight() // 2) - (height // 2)
        self.ventana.geometry(f'{width}x{height}+{x}+{y}')

    def crear_menu(self):

        titulo = tk.Label(
            self.ventana,
            text="Sistema de gestion - Menu Principal: ",
            font = ("Arial", 20, "bold"),
            fg = "black"
        )
        titulo.pack(pady=30)

        subtitulo = tk.Label(
            self.ventana,
            text=f"Usuario conectado - Rol: {self.rol}",
            font=("Arial", 14)
        )

        subtitulo.pack(pady=10)

        #frame para los botones:
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=30)

        #boton clientes:
        btn_cliente = tk.Button(
            frame_botones,
            text="Gestionar Clientes:",
            font = ("Arial", 14),
            bg = "black",
            fg="white",
            width= 25,
            height= 2,
            command = self.abrir_clientes,
            cursor = "hand2")
        btn_cliente.pack(pady=10)

        #boton empleados:
        btn_empleado = tk.Button(
            frame_botones,
            text="Gestionar Empleados:",
            font= ("Arial", 14),
            bg = "black",
            fg = "white",
            width= 25,
            height= 2,
            command = self.abrir_empleados,
            cursor = "hand2"
        )
        btn_empleado.pack(pady=10)

        #boton stock:
        btn_stock = tk.Button(
            frame_botones,
            text="Gestionar Stocks:",
            font= ("Arial", 14),
            bg = "black",
            fg = "white",
            width= 25,
            height= 2,
            command = self.abrir_stock,
            cursor = "hand2"
        )
        btn_stock.pack(pady=10)

        #boton proveedor:

        btn_proveedor = tk.Button(
            frame_botones,
            text="Gestionar Proveedor:",
            font=("Arial", 14),
            bg="black",
            fg="white",
            width=25,
            height=2,
            command=self.abrir_proveedor,
            cursor="hand2"
        )
        btn_proveedor.pack(pady=10)

        #boton facturacion:
        btn_facturacion = tk.Button(
            frame_botones,
            text="Gestionar Facturacion:",
            font = ("Arial", 14),
            bg = "black",
            fg = "white",
            width= 25,
            height= 2,
            command = self.abrir_facturacion,
            cursor = "hand2"
        )
        btn_facturacion.pack(pady=10)

        #boton salir:
        btn_sair = tk.Button(
            self.ventana,
            text="Salir",
            font = ("Arial", 12),
            bg = "black",
            fg = "white",
            width= 25,
            height= 2,
            command = self.salir,
            cursor = "hand2"
        )
        btn_sair.pack(pady=10)

        #barra de estado:
        self.estado = tk.Label(
            self.ventana,
            text="Listo",
            font = ("Arial", 12),
            fg = "green",
            relief = "sunken",
            anchor = "w"
        )
        self.estado.pack(side = "bottom", fill = 'x', padx=10, pady=5)

        if self.rol == "Gerente":

            btn_empleado.config(
                state = "disabled"
            )

        if self.rol == "Vendedor":

            btn_empleado.config(
                state = "disabled"
            )
            btn_stock.config(
                state = "disabled"
            )
            btn_proveedor.config(
                state = "disabled"
            )

    def abrir_clientes(self):
        self.estado.config( text="Abriendo gestor de clientes..." )
        self.ventana.withdraw()
        ventanaClientes( self.ventana, self.volver_menu )

    def abrir_empleados(self):
        self.estado.config(text = "Abriendo gestor de empleados...")
        self.ventana.withdraw()
        ventana_empleado(self.ventana, self.volver_menu)

    def abrir_facturacion(self):
        self.estado.config(text = "Abriendo facturacion...")
        self.ventana.withdraw()
        facturacion( self.ventana, self.volver_menu)

    def abrir_stock(self):
        self.estado.config(text = "Abriendo stocks...")
        self.ventana.withdraw()
        ver_stock( self.ventana, self.volver_menu)

    def abrir_proveedor(self):
        self.estado.config(text = "Abriendo proveedor...")
        self.ventana.withdraw()
        ver_proovedor( self.ventana, self.volver_menu)

    def volver_menu(self):
        self.ventana.deiconify()
        self.estado.config(text = "listo")

    def salir(self):
        if messagebox.askyesno("salir", "Estas seguro que quieres salir?"):

            self.ventana.destroy()
            self.ventana_login.destroy()