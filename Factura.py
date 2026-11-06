import tkinter as tk
from tkinter import ttk, messagebox
from Guardar_Datos import (actualizar_factura_total, cargar_detalles_facturas, cargar_facturas, guardar_factura, guadar_detalle_factura,modificar_factura, modificar_detalle_factura,eliminar_factura, eliminar_detalle_factura,cargar_clientes_factura,cargar_formas_pago,cargar_productos_factura)

class facturacion:

    def __init__(self, ventana_principal, volver_menu):

        self.ventana_principal = ventana_principal
        self.volver_menu = volver_menu

        self.id_detalle_seleccionado=  None

        self.ventana = tk.Toplevel(self.ventana_principal)
        self.ventana.title("Facturación")
        self.ventana.geometry("925x650")

        self.ventana.protocol("WM_DELETE_WINDOW", self.volver)

        self.subtotal = 0

        self.total = 0

        self.descuento = 0

        self.crear_interfaz()

    def crear_interfaz(self):

        tk.Label(self.ventana,text="Factura").grid(row=0, column=0, padx=5, pady=5)
        self.comboFactura = ttk.Combobox(self.ventana, width=30, state="readonly")
        self.comboFactura.grid(row=0, column=1, padx=5, pady=5)
        self.comboFactura.bind("<<ComboboxSelected>>", self.cargar_factura_seleccionada)

        tk.Label(self.ventana,text="Cliente").grid(row=1, column=0, padx=5, pady=5)
        self.comboCliente = ttk.Combobox(self.ventana, width = 30, state = "readonly")
        self.comboCliente.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.ventana,text="Forma de pago").grid(row=2, column=0, padx=5, pady=5)
        self.comboFormaPago = ttk.Combobox(self.ventana, width = 30, state = "readonly")
        self.comboFormaPago.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.ventana,text="Codigo de facturacion").grid(row=3, column=0, padx=5, pady=5)
        self.cajaCodigoFacturacion = tk.Entry(self.ventana)
        self.cajaCodigoFacturacion.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.ventana,text="Descuento").grid(row=4, column=0, padx=5, pady=5)
        self.cajaDescuento = tk.Entry(self.ventana)
        self.cajaDescuento.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(self.ventana,text="Producto").grid(row=5, column=0, padx=5, pady=5)
        self.comboProducto = ttk.Combobox(self.ventana, width = 30, state = "readonly")
        self.comboProducto.grid(row=5, column=1, padx=5, pady=5)
        self.comboProducto.bind("<<Comboboxselected>>",self.seleccionar_producto)

        tk.Label(self.ventana,text="Cantidad").grid(row=6, column=0, padx=5, pady=5)
        self.cajaCantidad = tk.Entry(self.ventana)
        self.cajaCantidad.grid(row=6, column=1, padx=5, pady=5)

        tk.Label(self.ventana,text="Precio unitario").grid(row=7, column=0, padx=5, pady=5)
        self.cajaPrecioUnitario = tk.Entry(self.ventana)
        self.cajaPrecioUnitario.grid(row=7, column=1, padx=5, pady=5)

        frame_botones = tk.Frame(self.ventana)
        frame_botones.grid(row=8,column=0,columnspan=2,pady=10)

        botonGuardar = tk.Button(frame_botones,text="Agregar producto",command=self.facturar,bg="lightblue",width=15)
        botonGuardar.pack(side="left", padx=5)

        botonEliminar = tk.Button(frame_botones,text="Eliminar Producto",command=self.eliminar,width=15)
        botonEliminar.pack(side="left", padx=5)

        botonModificar = tk.Button(frame_botones,text="Modificar producto agregado",command=self.modificarVenta,width=15)
        botonModificar.pack(side="left", padx=5)

        self.botonDescuento = tk.Button(frame_botones, text="Descuento del: 0%", command=self.descuento_subtotal, width=15)
        self.botonDescuento.pack(side="right", padx=5)

        botonVolver = tk.Button(frame_botones,text="Volver",command=self.volver,width=15)
        botonVolver.pack(side="left", padx=5)

        columnas = (
            "ID",
            "producto",
            "cantidad",
            "precio unitario",
            "descuento",
            "subtotal"
        )

        self.tabla = ttk.Treeview(self.ventana,columns=columnas,show="headings",height=10)

        for columna in columnas:

            self.tabla.heading(columna,text=columna)

            self.tabla.column(columna,width=150)

        self.tabla.column("ID", width=0, stretch=False)
        self.tabla.heading("ID", text="")

        self.tabla.grid(row=9,column=0,columnspan=6,padx=10,pady=20)

        self.tabla.bind("<<TreeviewSelect>>",lambda event: self.seleccionar_venta())

        self.labelSubtotal = tk.Label(self.ventana,text="Subtotal: $0.00",font=("Arial", 12, "bold"))

        self.labelSubtotal.grid(row=10,column=0,columnspan=4,pady=10)

        self.labelTotal = tk.Label(self.ventana,text="Total: $0.00", font = ("Arial", 12, "bold"))

        self.labelTotal.grid(row=11,column=0,columnspan=4,pady=10)

    def cargar_datos(self):

        facturas = cargar_facturas()

        lista_facturas = []

        for factura in facturas:
            
            id_factura = factura[0]
            codigo = factura[1]

            texto = f"{id_factura} - {codigo}"

            lista_facturas.append(texto)

        self.comboFactura["values"] = lista_facturas

        clientes = cargar_clientes_factura()

        lista_clientes = []

        for cliente in clientes:

            id_cliente = cliente[0]
            nombre = cliente[1]
            apellido = cliente[2]
            dni = cliente[3]

            texto = f"{id_cliente} - {nombre} {apellido} - DNI: {dni}"

            lista_clientes.append(texto)

        self.comboCliente["values"] = lista_clientes

        formas_pago = cargar_formas_pago()

        lista_formas_pago = []

        for forma in formas_pago:

            id_forma = forma[0]
            nombre_forma = forma[1]

            texto = f"{id_forma} - {nombre_forma}"

            lista_formas_pago.append(texto)

        self.comboFormaPago["values"] = lista_formas_pago

        productos = cargar_productos_factura()

        lista_productos = []

        for producto in productos:

            id_producto = producto[0]
            nombre_producto = producto[1]
            precio = producto[2]

            texto = f"{id_producto} - {nombre_producto} - ${precio}"

            lista_productos.append(texto)

        self.comboProducto["values"] = lista_productos

    def cargar_factura_seleccionada(self, event=None):

        factura = self.comboFactura.get()

        if factura == "":

            return

        partes = factura.split(" - ")

        id_factura = int(partes[0])

        self.id_factura_seleccionado = id_factura

        detalles = cargar_detalles_facturas(id_factura)

        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        for detalle in detalles:
            id_detalle = detalle[0]
            id_producto = detalle[1]
            nombre_producto = detalle[2]
            cantidad = detalle[3]
            precio = detalle[4]
            descuento = detalle[5]
            subtotal = detalle[6]

            producto = f"{id_producto} - {nombre_producto}"

            self.tabla.insert("","end",
                values=(
                    id_detalle,
                    producto,
                    cantidad,
                    precio,
                    descuento,
                    subtotal
                )
            )

        self.actualizarSubtotal()

    def actualizarSubtotal(self):

        self.subtotal = 0

        for venta in self.tabla.get_children():

            valores = self.tabla.item(venta, "values")

            try:
                cantidad = int(valores[2])
                precio = float(valores[3])
                descuento_venta = float(valores[4])

                subtotal_producto = cantidad * precio

                subtotal_producto = subtotal_producto * (1 - descuento_venta / 100)

                self.subtotal += subtotal_producto

            except ValueError:

                pass

        self.labelSubtotal.config(text=f"Subtotal: ${self.subtotal:.2f}")

        self.actualizarTotal()

    def descuento_subtotal(self):

        self.descuento += 5

        if self.descuento > 100:

            self.descuento = 0

        self.botonDescuento.config(text = f"Descuento del : {self.descuento}%")

        self.actualizarTotal()

    def actualizarTotal(self):

        self.total = self.subtotal * (1 - self.descuento / 100)

        self.labelTotal.config(text=f"Total: ${self.total:.2f}")

    def agregar_producto(self):

        producto = self.comboProducto.get()
        cantidad = self.cajaCantidad.get()
        precioUnitario = self.cajaPrecioUnitario.get()
        descuento = self.cajaDescuento.get()

        if producto == "":
            messagebox.showwarning("Producto","Seleccione un producto")
            return

        try:
            cantidad = int(cantidad)
            precioUnitario = float(precioUnitario)
            descuento = float(descuento)

            if cantidad <= 0:
                messagebox.showwarning("Cantidad","La cantidad debe ser mayor a 0")
                return

            if descuento < 0 or descuento > 100:
                messagebox.showwarning("Descuento","El descuento debe estar entre 0 y 100")
                return

        except ValueError:
            messagebox.showwarning("Datos inválidos","Cantidad, precio o descuento inválido")
            return

        subtotal = cantidad * precioUnitario

        subtotal = subtotal * (1 - descuento / 100)

        self.tabla.insert("","end",
            values=("",
                producto,
                cantidad,
                precioUnitario,
                descuento,
                subtotal
            )
        )

        self.actualizarSubtotal()

        self.comboProducto.set("")
        self.cajaCantidad.delete(0, tk.END)
        self.cajaPrecioUnitario.delete(0, tk.END)
        self.cajaDescuento.delete(0, tk.END)

    def facturar(self):

        cliente = self.comboCliente.get()
        formaPago = self.comboFormaPago.get()
        codigo = self.cajaCodigoFacturacion.get()
        descuento = self.cajaDescuento.get()

        if cliente == "":

            messagebox.showwarning("Cliente", "Seleccione un cliente")

            return

        if formaPago == "":

            messagebox.showwarning("Forma Pago", "Seleccione un forma pago")

            return

        if codigo == "":

            messagebox.showwarning("Codigo", "Ingrese el codigo de facturacion")

            return

        if len(self.tabla.get_children()) == 0:

            messagebox.showwarning("Producto", "Agregue al menos un producto")

            return

        try:

            descuento = float(descuento)

            if descuento < 0 or descuento > 100:

                messagebox.showwarning("Descuento", "El descuento debe estar entre 0 y 100")

                return

        except ValueError:

            descuento = 0

        partes_cliente = cliente.split(" - ")
        id_cliente = int(partes_cliente[0])

        partes_forma = formaPago.split(" - ")
        id_forma = int(partes_forma[0])

        subtotal = self.subtotal

        total = subtotal * (1 - descuento / 100)

        datos_factura = (
            codigo,
            id_cliente,
            id_forma,
            subtotal,
            descuento,
            total
        )

        id_factura = guardar_factura(datos_factura)

        self.id_factura_seleccionado = id_factura

        for venta in self.tabla.get_children():

            valores = self.tabla.item(venta, "values")

            producto = valores[1]
            cantidad = int (valores[2])
            precioUnitario = float (valores[3])
            descuento = float (valores[4])
            subtotal = float (valores[5])

            partes_producto = producto.split(" - ")

            id_producto = int(partes_producto[0])

            datos_detalle = (
                id_factura,
                id_producto,
                cantidad,
                precioUnitario,
                descuento,
                subtotal
            )

            id_detalle = guardar_factura(datos_detalle)

            self.tabla.item(venta, values = (
                id_detalle,
                producto,
                cantidad,
                precioUnitario,
                descuento,
                subtotal
            ))

        messagebox.showinfo("Factura", "Factura guardada correctamente")

        self.tabla.delete( *self.tabla.get_children())

        self.comboCliente.set("")

        self.comboFormaPago.set("")

        self.cajaCodigoFacturacion.delete(0, tk.END)

        self.cajaDescuento.delete(0, tk.END)

        self.comboProducto.set("")

        self.cajaCantidad.delete(0, tk.END)

        self.cajaPrecioUnitario.delete(0, tk.END)

        self.subtotal = 0
        self.total = 0
        self.descuento = 0

        self.labelSubtotal.config(text="Subtotal: $0.00")

        self.labelTotal.config(text="Total: $0.00")

        self.botonDescuento.config(text="Descuento del: 0%")

    def seleccionar_venta(self):

        seleccion = self.tabla.selection()

        if seleccion:
            valores = self.tabla.item(
                seleccion[0],
                "values"
            )

            self.id_detalle_seleccionado = valores[0]

            self.comboProducto.set(valores[1])

            self.cajaCantidad.delete(0, tk.END)
            self.cajaCantidad.insert(0, valores[2])

            self.cajaPrecioUnitario.delete(0, tk.END)
            self.cajaPrecioUnitario.insert(0, valores[3])

            self.cajaDescuento.delete(0, tk.END)
            self.cajaDescuento.insert(0, valores[4])

    def seleccionar_producto(self, event=None):

        producto = self.comboProducto.get()

        if producto == "":
            return

        partes = producto.split(" - ")

        precio = partes[2]

        precio = precio.replace("$", "")

        self.cajaPrecioUnitario.delete(0, tk.END)

        self.cajaPrecioUnitario.insert(
            0,
            precio
        )

    def eliminar(self):

        if self.id_detalle_seleccionado is None:

            messagebox.showwarning("Eliminar","Seleccione un producto de la factura")

            return

        confirmar = messagebox.askyesno("Eliminar","¿Está seguro de eliminar este producto?")

        if not confirmar:

            return

        eliminar_detalle_factura(self.id_detalle_seleccionado)

        seleccion = self.tabla.selection()

        if seleccion:

            self.tabla.delete(seleccion[0])

        self.id_detalle_seleccionado = None

        self.actualizarSubtotal()

        messagebox.showinfo("Eliminar","Producto eliminado correctamente")

    def modificarVenta(self):

        if self.id_detalle_seleccionado is None:
            messagebox.showwarning("Modificar","Seleccione un producto de la factura")
            return

        try:
            cantidad = int(self.cajaCantidad.get())
            precioUnitario = float(self.cajaPrecioUnitario.get())
            descuento = float(self.cajaDescuento.get())

            if cantidad <= 0:
                messagebox.showwarning("Cantidad","La cantidad debe ser mayor a 0")
                return

            if descuento < 0 or descuento > 100:
                messagebox.showwarning("Descuento","El descuento debe estar entre 0 y 100")
                return

        except ValueError:
            messagebox.showwarning("Datos inválidos","Cantidad, precio o descuento inválido")
            return

        subtotal = cantidad * precioUnitario

        subtotal = subtotal * (1 - descuento / 100)

        datos = (
            cantidad,
            precioUnitario,
            descuento,
            subtotal
        )

        modificar_detalle_factura(self.id_detalle_seleccionado, datos)

        seleccion = self.tabla.selection()

        if seleccion:
            self.tabla.item(
                seleccion[0],
                values=(
                    self.id_detalle_seleccionado,
                    self.comboProducto.get(),
                    cantidad,
                    precioUnitario,
                    descuento,
                    subtotal
                )
            )

        self.actualizarSubtotal()

        descuento_factura = self.descuento
        total_factura = self.total

        actualizar_factura_total(self.id_factura_seleccionado,self.subtotal, descuento_factura, total_factura)

        messagebox.showinfo("Modificar","Producto modificado correctamente")

    def volver(self):

        self.ventana.destroy()
        self.volver_menu()


    def limpiar_cajas(self):

        self.cajaProducto.delete(0,tk.END)

        self.cajaCantidad.delete(0,tk.END)

        self.cajaPrecioUnitario.delete(0,tk.END)

        self.cajaDescuento.delete(0,tk.END)

        self.cajaSubtotal.delete(0,tk.END)
