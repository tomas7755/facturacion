import tkinter as tk
from email.mime import image
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os
from Ventana_principal import menu_principal
from Guardar_Datos import guardar_usuarios, buscar_usuario

class Login:
    def __init__(self):

        self.ventana = tk.Tk()
        self.ventana.title("Iniciar sesion")
        self.ventana.geometry("800x600")

        ruta = os.path.join(os.path.dirname(__file__), "fondo.jpg")

        imagen = Image.open(ruta)
        imagen = imagen.resize((800, 600))

        self.fondo = ImageTk.PhotoImage(imagen)

        label_fondo = tk.Label(self.ventana, image = self.fondo)
        label_fondo.place(x = 0, y = 0, relwidth = 1 , relheight = 1)

        self.panel = tk.Frame(self.ventana, bg = "white")
        self.panel.place(relx = 0.5, rely= 0.5, anchor = "center")

        tk.Label(self.panel, text="INICIAR SESIÓN",font=("Arial", 18, "bold"),bg="white").grid(row=0, column=0, columnspan=2, pady=20)

        tk.Label(self.panel, text= "Usuario",bg="white").grid(column=0 , row=1, padx=10, pady=10)
        self.usuario = ttk.Entry(self.panel, width=25)
        self.usuario.grid(row=1, column=0, padx=10, pady=10)

        tk.Label (self.panel, text = "Contraseña", bg="white").grid(column=0, row=2, padx=10, pady=10)
        self.contrasenia = ttk.Entry(self.panel, width=25, show ="*")
        self.contrasenia.grid(column=1, row=2, padx=10, pady=10)

        tk.Label (self.panel, text = "Rol", bg ="white").grid(column=0, row=3, padx=10, pady=10)
        self.rol = ttk.Combobox (self.panel, values = ["Administrador", "Gerente", "Vendedor"], state="readonly", width=22)
        self.rol.grid(column=1, row=3, padx=10, pady=10)

        ttk.Button(self.panel, text="Iniciar sesion", command = self.iniciarSesion).grid(column=0, row=4, columnspan=2, pady=10)

        ttk.Button(self.ventana, text = "registrarse", command = self.abrirRegistro).grid(column=0, row=5, columnspan=2,  pady=10)

        self.ventana.mainloop()

    def iniciarSesion(self):

        usuario = self.usuario.get()
        contraseña = self.contrasenia.get()
        rol = self.rol.get()

        if usuario == "" or contraseña == "" or rol == "":

            messagebox.showwarning( "Login", "Complete todos los datos" )

            return

        datos = buscar_usuario(usuario)

        if datos is not None:

            usuario_sql = datos[0]
            contraseña_sql = datos[1]
            rol_sql = datos[2]

            if contraseña_sql == contraseña and rol_sql == rol:

                messagebox.showinfo("Login", f"Bienvenido {usuario_sql}")

                self.ventana.withdraw()

                menu_principal(self.ventana, rol_sql)

            else:

                messagebox.showerror("Login", "Contraseña o rol incorrecto")

        else:

            messagebox.showerror("Login", "El usuario no existe")

    def abrirRegistro(self):

        ventanaRegistro = tk.Toplevel(self.ventana)
        ventanaRegistro.title("Registrar usuario")
        ventanaRegistro.geometry("350x300")

        ttk.Label (ventanaRegistro, text = "Nuevo Usuario").grid(column = 1, row = 1, padx = 10, pady = 10)
        nuevo_usuario = ttk.Entry(ventanaRegistro, width=20)
        nuevo_usuario.grid(column=2, row=1)

        ttk.Label (ventanaRegistro, text = "Nombre").grid(column = 1, row = 2, padx = 10, pady = 10)
        nuevo_nombre = ttk.Entry(ventanaRegistro, width=20)
        nuevo_nombre.grid(column=2, row=2)

        ttk.Label(ventanaRegistro, text="Apellido").grid(column=1, row=3, padx=10, pady=10)
        nuevo_apellido = ttk.Entry(ventanaRegistro, width=20)
        nuevo_apellido.grid(column=2, row=3)

        ttk.Label (ventanaRegistro, text = "Contraseña").grid(column = 1, row = 4, padx = 10, pady = 10)
        nueva_contraseña = ttk.Entry(ventanaRegistro, show = "*" , width = 20)
        nueva_contraseña.grid(column=2, row=4)

        ttk.Label (ventanaRegistro, text = "Rol").grid(column = 1, row = 6, padx = 10, pady = 10)
        nuevo_rol = ttk.Combobox(ventanaRegistro, values=["Administrador", "Gerente", "Vendedor"], state="readonly")
        nuevo_rol.grid(column=2, row=6)

        ttk.Button(ventanaRegistro, text = "registro", command = lambda : self.registrarUsuario(nuevo_usuario,nuevo_nombre, nuevo_apellido, nueva_contraseña, nuevo_rol, ventanaRegistro)).grid(column=2, row=7, pady=20)

    def registrarUsuario(self, nuevo_usuario, nuevo_nombre, nuevo_apellido, nueva_contraseña, nuevo_rol, ventanaRegistro):

        usuario = nuevo_usuario.get()
        nombre = nuevo_nombre.get()
        apellido = nuevo_apellido.get()
        contrasenia = nueva_contraseña.get()
        rol = nuevo_rol.get()

        if usuario == "" or nombre == "" or apellido == "" or contrasenia == "" or rol == "":

            messagebox.showwarning("Registro", "Complete los datos")

            return

        datos = (nombre, apellido, usuario, contrasenia, rol)

        resultado = guardar_usuarios(datos)

        if resultado:

            messagebox.showinfo("Registro", "Usuario registrado correctamente")

            ventanaRegistro.destroy()

        else:

            messagebox.showerror("Registro", "No se pudo registrar al usuario")

if __name__ == "__main__":
    app = Login()
