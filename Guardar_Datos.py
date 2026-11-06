from unittest import result

import mysql.connector
import tkinter as tk
from tkinter import ttk
from Conectar import conectar

##Para clientes:

def guardar_clientes(datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombre = datos[0]
    apellido = datos[1]
    dni = datos[2]
    fecha_nacimiento = datos[3]
    telefono = datos[4]
    email = datos[5]
    direccion = datos[6]
    ciudad = datos[7]
    provincia = datos[8]
    codigo_postal = datos[9]
    fecha_registro = datos[10]

    sql = """INSERT INTO persona(nombre, apellido, dni, fecha_nacimiento) VALUES (%s, %s, %s, %s)"""

    cursor.execute(sql, (nombre, apellido, dni, fecha_nacimiento))

    idPersona = cursor.lastrowid

    sql = """INSERT INTO cliente (id_persona, fecha_registro) VALUES (%s, %s)"""

    cursor.execute(sql, (idPersona, fecha_registro))

    idCliente = cursor.lastrowid

    sql = """INSERT INTO telefono (id_persona, telefono) VALUES (%s, %s)"""

    cursor.execute(sql, (idPersona, telefono))

    sql = """INSERT INTO email (id_persona, mail) VALUES (%s, %s)"""

    cursor.execute(sql, (idPersona, email))

    sql = """SELECT id FROM paises WHERE pais = %s"""

    cursor.execute(sql, ("Argentina",))

    resultado = cursor.fetchone()

    if resultado:

        id_paises = resultado[0]

    else:

        sql = """INSERT INTO paises (pais) VALUES (%s)"""

        cursor.execute(sql, ("Argentina",))

        id_paises = cursor.lastrowid

    sql = """SELECT id FROM provincias WHERE provincia = %s AND id_pais = %s"""

    cursor.execute(sql, (provincia, id_paises))

    resultado = cursor.fetchone()

    if resultado:

        id_provincias = resultado[0]

    else:

        sql = """INSERT INTO provincias (provincia, id_pais) VALUES (%s, %s)"""

        cursor.execute(sql, (provincia, id_paises))

        id_provincias = cursor.lastrowid

    sql = """SELECT id FROM ciudades WHERE ciudad = %s AND id_provincia = %s"""

    cursor.execute(sql, (ciudad, id_provincias))

    resultado = cursor.fetchone()

    if resultado:

        id_ciudades = resultado[0]

    else:

        sql = """INSERT INTO ciudades (ciudad, id_provincia) VALUES (%s, %s)"""

        cursor.execute(sql, (ciudad, id_provincias))

        id_ciudades = cursor.lastrowid

    sql = """INSERT INTO direccion (direccion, codigoPostal, id_ciudad) VALUES (%s, %s, %s)"""

    cursor.execute(sql, (direccion, codigo_postal, id_ciudades))

    id_direccion = cursor.lastrowid

    sql = """INSERT INTO personaxubicaciones (idPersona, id_direccion) VALUES (%s, %s)"""

    cursor.execute(sql, (idPersona, id_direccion))

    conexion.commit()

    cursor.close()
    conexion.close()

    return idCliente

def cargar_tabla_cliente(tabla):

    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT 
    cliente.id, 
    persona.nombre, 
    persona.apellido, 
    persona.dni, 
    persona.fechaNacimiento, 
    telefono.telefono, 
    email.mail, 
    direccion.direccion, 
    ciudades.ciudad, 
    provincias.provincia, 
    direccion.codigoPostal, 
    cliente.fecha_registro
    
    FROM cliente
    
    INNER JOIN personas ON cliente.id_persona = persona.id 
    
    LEFT JOIN telefono  ON persona.id = telefono.id_persona
    
    LEFT JOIN email  ON persona.id = email.id_persona
    
    LEFT JOIN personaxubicaciones ON persona.id = personaxubicaciones.id_persona
    
    LEFT JOIN direccion ON personaxubicaciones.id_direccion = direccion.id
    
    LEFT JOIN ciudades ON direccion.id_ciudad = ciudades.id
    
    LEFT JOIN provincias ON ciudades.id_provincia = provincias.id
    
    ORDER BY id_cliente"""

    cursor.execute(sql)

    registros = cursor.fetchall()

    for registros in registros:

        tabla.insert("", "end", values = registros)

    cursor.close()
    conexion.close()

def modificar_cliente(id_cliente, datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombre = datos[0]
    apellido = datos[1]
    dni = datos[2]
    fechaNacimiento = datos[3]
    telefono = datos[4]
    email = datos[5]
    direccion = datos[6]
    ciudad = datos[7]
    provincia = datos[8]
    codigoPostal = datos[9]

    sql = """SELECT id FROM clientes WHERE id = %s"""

    cursor.execute(sql, (id_cliente,))

    resultado = cursor.fetchone()

    if resultado is None:

        cursor.close()
        conexion.close()
        return

    id_persona = resultado[0]

    sql = """UPDATE persona SET nombre = %s, apellido = %s, dni = %s, fechaNacimiento = %s WHERE id = %s"""

    cursor.execute(sql, (nombre, apellido, dni, fechaNacimiento, id_persona))

    sql = """UPDATE telefono SET telefono = %s WHERE id = %s"""

    cursor.execute(sql, (telefono, id_persona))

    sql = """UPDATE email SET email = %s WHERE id = %s"""

    cursor.execute(sql, (email, id_persona))

    sql = """SELECT id_direccion FROM personaxubicaciones WHERE id_persona = %s AND habilitado = 1"""

    cursor.execute(sql, (id_persona,))

    resultado = cursor.fetchone()

    if resultado:

        id_direccion = resultado[0]

    sql = """SELECT id FROM provincias WHERE provincia = %s"""

    cursor.execute(sql, (provincia,))

    resultado = cursor.fetchone()

    if resultado:

        id_provincia = resultado[0]

    else:

        sql = """INSERT INTO provincias (provincia, id_pais) VALUES (%s, %s)"""

        cursor.execute(sql, (provincia, 1))

        id_provincia = cursor.lastrowid

    sql = """SELECT id FROM ciudades WHERE ciudad = %s AND id_provincia = %s"""

    cursor.execute(sql, (ciudad, id_provincia))

    resultado = cursor.fetchone()

    if resultado:

        id_ciudades = resultado[0]

    else:

        sql = """INSERT INTO ciudades (ciudad, id_provincia) VALUES (%s, %s)"""

        cursor.execute(sql, (ciudad, id_provincia))

        id_ciudades = cursor.lastrowid

    sql = """UPDATE direccion SET direccion = %s, codigoPostal = %s, id_ciudad = %s WHERE id = %s"""

    cursor.execute(sql, (direccion, codigoPostal, id_ciudades, id_direccion))

    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_cliente(id_cliente):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT id_persona FROM clientes WHERE id = %s"""

    cursor.execute(sql, (id_cliente,))

    resultado = cursor.fetchone()

    if resultado is None:

        cursor.close()
        conexion.close()
        return

    id_persona = resultado[0]

    sql = """SELECT id_direccion FROM personaxubicaciones WHERE id_persona = %s"""

    cursor.execute(sql, (id_persona,))

    resultado = cursor.fetchone()

    id_direccion = None

    if resultado:

        id_direccion = resultado[0]

    sql = """DELETE FROM personaxubicaciones WHERE id_persona = %s"""

    cursor.execute(sql, (id_persona,))

    sql = """DELETE FROM telefono WHERE id_persona = %s"""

    cursor.execute(sql, (id_persona,))

    sql = """DELETE FROM email WHERE id_persona = %s"""

    cursor.execute(sql, (id_persona,))

    if id_direccion is not None:

        sql = """DELETE FROM direccion WHERE id = %s"""

        cursor.execute(sql, (id_direccion,))

    sql = """DELETE FROM cliente WHERE id = %s"""

    cursor.execute(sql, (id_cliente,))

    sql = """DELETE FROM persona WHERE id = %s"""

    cursor.execute(sql, (id_cliente,))

    conexion.commit()
    cursor.close()
    conexion.close()

##Para empleados:

def guardar_empleado(datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombre = datos[0]
    apellido = datos[1]
    dni = datos[2]
    fechaNacimiento = datos[3]
    telefono = datos[4]
    email = datos[5]
    legajo = datos[6]
    puesto = datos[7]
    salario = datos[8]
    fechaContratacion = datos[9]

    sql = """INSERT INTO persona (nombre, apellido, dni, fechaNacimiento) VALUES (%s, %s, %s, %s)"""

    cursor.execute(sql, (nombre, apellido, dni, fechaNacimiento))

    id_persona = cursor.lastrowid

    sql = """INSERT INTO empleado (id_persona, legajo, puesto, salario, fechaContratacion) VALUES (%s, %s, %s, %s, %s)"""

    cursor.execute(sql, (id_persona, legajo, puesto, salario, fechaContratacion))

    id_empleado = cursor.lastrowid

    sql =  """INSERT INTO telefono (id_persona, telefono) VALUES (%s, %s)"""

    cursor.execute(sql, (id_persona, telefono))

    sql = """INSERT INTO email (id_persona, email) VALUES (%s, %s)"""

    cursor.execute(sql, (id_persona, email))

    cursor.close()
    conexion.close()

    return id_empleado

def cargar_tabla_empleado(tabla):

    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT 
        empleado.id,
        persona.nombre,
        persona.apellido,
        persona.dni,
        persona.fechaNacimiento,
        telefono.telefono,
        email.email,
        empleado.legajo,
        empleado.puesto,
        empleado.salario,
        empleado.fechaContratacion
        
        FROM empleados 
        
        INNER JOIN persona ON empleado.id_persona = persona.id
        
        LEFT JOIN telefono ON persona.id = telefono.id_persona
        
        LEFT JOIN email ON persona.id = email.id_persona
        
        ORDER BY empleado.id"""

    cursor.execute(sql)
    registros = cursor.fetchall()

    for registro in registros:

        tabla.insert("", "end", values = registro)

    cursor.close()
    conexion.close()

def modificar_empleado(id_empleado, datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombre = datos[0]
    apellido = datos[1]
    dni = datos[2]
    fechaNacimiento = datos[3]
    telefono = datos[4]
    email = datos[5]
    legajo = datos[6]
    puesto = datos[7]
    salario = datos[8]

    sql = """SELECT id_persona FROM empleado WHERE id = %s"""

    cursor.execute(sql, (id_empleado,))

    resultado = cursor.fetchone()

    if resultado is None:

        cursor.close()
        conexion.close()
        return

    id_persona = resultado[0]

    sql = """UPDATE persona SET nombre = %s, dni = %s, fechaNacimiento = %s WHERE id = %s"""

    cursor.execute(sql, (nombre, dni, fechaNacimiento, id_persona))

    sql = """UPDATE telefono SET telefono = %s WHERE id_persona = %s"""

    cursor.execute(sql, (telefono, id_persona))

    sql = """UPDATE email SET email = %s WHERE id_persona = %s"""

    cursor.execute(sql, (email, id_persona))

    sql = """UPDATE empleado SET legajo = %s, puesto = %s, salario = %s WHERE id = %s"""

    cursor.execute(sql, (legajo, puesto, salario, id_persona))

    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_empleado(id_empleado):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT id_persona FROM empleado WHERE id = %s"""

    cursor.execute(sql, (id_empleado,))

    resultado = cursor.fetchone()

    if resultado is None:

        cursor.close()
        conexion.close()
        return

    id_persona = resultado[0]

    sql = """DELETE FROM telefono WHERE id_persona = %s"""

    cursor.execute(sql, (id_persona,))

    sql = """DELETE FROM email WHERE id_persona = %s"""

    cursor.execute(sql, (id_persona,))

    sql = """DELETE FROM empleado WHERE id_persona = %s"""

    cursor.execute(sql, (id_persona,))

    sql = """DELETE FROM persona WHERE id = %s"""

    cursor.execute(sql, (id_persona,))

    conexion.commit()
    cursor.close()
    conexion.close()

##para stock:

def guardar_stock (datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombre_producto = datos[0]
    cantidad = datos[1]
    precio = datos[2]
    proveedor = datos[3]
    marca = datos[4]
    fecha_ingreso = datos[5]

    sql = """SELECT id FROM proveedor WHERE nombre = %s"""

    cursor.execute(sql, (nombre_producto,))

    resultado = cursor.fetchone()

    if resultado:

        id_proveedor = resultado[0]

    else:

        sql = """INSERT INTO proveedor (nombre) VALUES (%s)"""

        cursor.execute(sql, (nombre_producto,))

        id_proveedor = cursor.lastrowid

    sql = """INSERT INTO productos (nombreProducto, precio, marca, id_proveedor) VALUES (%s, %s, %s, %s)"""

    cursor.execute(sql, (nombre_producto, precio, marca, id_proveedor))

    id_producto = cursor.lastrowid

    sql = """INSERT INTO stock (id_producto, cantidad, fecha_ingreso) VALUES (%s, %s, %s)"""

    cursor.execute(sql, (id_producto, cantidad, fecha_ingreso))

    id_stock = cursor.lastrowid

    cursor.close()
    conexion.close()

    return id_stock

def cargar_tabla_stock(tabla):

    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT 
        stock.id, 
        productos.nombreProducto, 
        stock.cantidad,
        productos.precio,
        proveedor.nombre,
        productos.marca, 
        stock.fecha_ingreso
        
        FROM stock 
        
        INNER JOIN productos ON stock.id_producto = productos.id
        
        LEFT JOIN proveedor ON productos.id_proveedor = proveedor.id
        
        ORDER BY stock.id"""

    cursor.execute(sql)
    registros = cursor.fetchall()

    for registro in registros:

        tabla.insert("", "end", values = registro)

    cursor.close()
    conexion.close()

def modificar_stock(id_stock, datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombre_producto = datos[0]
    cantidad = datos[1]
    precio = datos[2]
    proveedor = datos[3]
    marca = datos[4]

    sql = """SELECT id_producto FROM id WHERE id = %s"""

    cursor.execute(sql, (id_stock,))

    resultado = cursor.fetchone()

    if resultado is None:

        conexion.close()
        cursor.close()

        return

    id_producto = resultado[0]

    sql = """SELECT id FROM proveedor WHERE nombre = %s"""

    cursor.execute(sql, (nombre_producto,))

    resultado = cursor.fetchone()

    if resultado:

        id_proveedor = resultado[0]

    else:

        sql = """INSERT INTO proveedor (nombre) VALUES (%s)"""

        cursor.execute(sql, (nombre_producto,))

        id_proveedor = cursor.lastrowid

    sql = """UPDATE productos SET nombreProducto = %s, precio = %s, marca = %s, id_proveedor = %s WHERE id = %s"""

    cursor.execute(sql(nombre_producto, precio, marca, id_proveedor, id_producto))

    sql = """UPDATE stock SET cantidad = %s WHERE id = %s"""

    cursor.execute(sql, (cantidad, id_stock))

    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_stock(id_stock):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT id_producto FROM stock WHERE id = %s"""

    cursor.execute(sql, (id_stock,))

    resultado = cursor.fetchone()

    if resultado is None:

        conexion.close()
        cursor.close()
        return

    id_producto = resultado[0]

    sql = """DELETE FROM stock WHERE id = %s"""

    cursor.execute(sql, (id_stock,))

    sql = """DELETE FROM productos WHERE id = %s"""

    cursor.execute(sql, (id_producto,))

    conexion.commit()
    cursor.close()
    conexion.close()

##para proveedor:

def guardar_proveedor (datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombreProvedor = datos[0]

    sql = """INSERT INTO proveedor (nombre) VALUES (%s)"""

    cursor.execute(sql, (nombreProvedor,))

    id_proveedor = cursor.lastrowid

    conexion.commit()
    cursor.close()
    conexion.close()

    return id_proveedor

def cargar_tabla_proveedor(tabla):

    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT id, nombreProveedor from proveedor WHERE habilitado = 1 ORDER BY id"""

    cursor.execute(sql)

    registros = cursor.fetchall()

    for registro in registros:
        tabla.insert ("","end", values = registro)

    cursor.close()
    conexion.close()

def  modificar_proveedor(id_proveedor, datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombre = datos[0]

    sql = """UPDATE proveedor SET nombre = %s WHERE id = %s"""

    cursor.execute(sql, (nombre, id_proveedor))

    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_proveedor(id_proveedor):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """DELETE FROM proveedor SET habilitado = 0 WHERE ID = %s"""

    cursor.execute(sql, (id_proveedor,))

    conexion.commit()
    cursor.close()
    conexion.close()

##para factura:

def cargar_clientes_factura():

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT 
        cliente.id, 
        persona.nombre, 
        persona.apellido, 
        persona.dni, 
        
        FROM cliente 
        
        INNER JOIN persona ON cliente.id_persona = persona.id
        
        WHERE persona.habilitado = 1
        
        ORDER BY persona.apellido, persona.nombre"""

    cursor.execute(sql)

    registros = cursor.fetchall()

    cursor.close()
    conexion.close()

    return registros

def cargar_formas_pago():

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT  id, formaPago FROM formaPago WHERE habilitado = 1 ORDER BY id"""

    cursor.execute(sql)

    registros = cursor.fetchall()

    cursor.close()
    conexion.close()

    return registros

def cargar_productos_factura():

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT productos.id, productos.nombreProducto, productos.precio FROM productos WHERE productos.habilitado = 1 ORDER BY productos.nombreProducto"""

    cursor.execute(sql)

    registros = cursor.fetchall()

    cursor.close()
    conexion.close()

    return registros

def cargar_facturas():

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT id, codigoFacturacion FROM factura WHERE habilitado = 1 ORDER BY id DESC"""

    cursor.execute(sql)

    registros = cursor.fetchall()

    cursor.close()
    conexion.close()

    return registros

def guardar_factura(datos):

    conexion = conectar()
    cursor = conexion.cursor()

    codigoFactura = datos[0]
    idCliente = datos[1]
    idFormaPago = datos[2]
    subtotal = datos[3]
    descuento = datos[4]
    total = datos[5]

    sql = """INSERT INTO factura (codigoFacturacion, id_cliente, id_formaPago, subtotal, descuento, total) VALUES (%s, %s, %s, %s, %s, %s)"""

    cursor.execute(sql, (codigoFactura, idCliente, idFormaPago, subtotal, descuento, total))

    idFactura = cursor.lastrowid

    conexion.commit()

    cursor.close()
    conexion.close()

    return idFactura

def guadar_detalle_factura(datos):

    conexion = conectar()
    cursor = conexion.cursor()

    id_factura = datos[0]
    id_producto = datos[1]
    cantidad = datos[2]
    precioUnitario = datos[3]
    descuento = datos[4]
    subtotal = datos[5]

    sql = """INSERT INTO detalleFactura (idFactura, idProducto, cantidad, precioUnitario, descuento, subtotal) VALUES (%s, %s, %s, %s, %s, %s)"""

    cursor.execute(sql, (id_factura, id_producto, cantidad, precioUnitario, descuento, subtotal))

    idDetalle = cursor.lastrowid

    conexion.commit()
    cursor.close()
    conexion.close()

    return idDetalle

def cargar_tabla_factura(tabla):

    for fila in tabla.get_children():
        tabla.delete(fila)

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT ID, nombre, apellido, dni, precio, codigoFacturacion, email, descuento from factura """

    cursor.execute(sql)

    registros = cursor.fetchall()

    for registro in registros:
        tabla.insert ("","end", values = registro)

    cursor.close()
    conexion.close()

def modificar_factura(id_factura, datos):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """UPDATE factura 
    SET nombre = %s,
    apellido = %s,
    dni = %s,
    precio = %s,
    codigoFacturacion = %s,
    email = %s,
    descuento = %s
    WHERE ID = %s"""

    cursor.execute(sql, datos + (id_factura,))

    conexion.commit()
    cursor.close()
    conexion.close()

def modificar_detalle_factura(id_detalle, datos):

    conexion = conectar()
    cursor = conexion.cursor()

    cantidad = datos[0]
    precioUnitario = datos[1]
    descuento = datos[2]
    subtotal = datos[3]

    sql = """UPDATE detalleFactura SET cantidad = %s, precioUnitario = %s, descuento = %s, subtotal %s WHERE ID = %s"""

    cursor.execute(sql, (cantidad, precioUnitario, descuento, id_detalle))

    conexion.commit()

    cursor.close()
    conexion.close()

def eliminar_factura(id_factura):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """DELETE FROM factura WHERE ID = %s"""

    cursor.execute(sql, (id_factura,))

    conexion.commit()
    cursor.close()
    conexion.close()

def eliminar_detalle_factura(id_detalle):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """DELETE FROM detalleFactura SET habilitado = 0 WHERE ID = %s"""

    cursor.execute(sql, (id_detalle,))

    conexion.commit()
    cursor.close()
    conexion.close()

def actualizar_factura_total(id_factura, subtotal, descuento, total):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """UPDATE factura SET subtotal = %s, descuento = %s, total = %s WHERE id = %s"""

    cursor.execute(sql, (subtotal, descuento, total, id_factura))

    conexion.commit()
    cursor.close()
    conexion.close()

def cargar_detalles_facturas(idFactura):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT 
            detalleFactura.id,
            productos.id, 
            productos.nombreProducto,
            detalleFactura.cantidad,
            detalleFactura.precioUnitario,
            detalleFactura.descuento,
            detalleFactura.subtotal
            
            FROM detalleFactura
            
            INNER JOIN productos ON detalleFactura.idproducto = productos.id
            
            WHERE detalleFactura.idproducto = productos.id
            
            AND detalleFactura.habilitado = 1"""

    cursor.execute(sql, (idFactura,))

    registros = cursor.fetchall()

    cursor.close()
    conexion.close()

    return registros

##para usuarios:

def guardar_usuarios (datos):

    conexion = conectar()
    cursor = conexion.cursor()

    nombre = datos[0]
    apellido = datos[1]
    usuario = datos[2]
    contrasenia = datos[3]
    rol = datos[4]

    sql = """INSERT INTO persona(nombre, apellido) VALUES (%s, %s)"""

    cursor.execute(sql, (nombre, apellido))

    id_persona = cursor.lastrowid

    sql = """INSERT INTO usuarios(id_persona, usuario, contraseña) VALUES (%s, %s, %s)"""

    cursor.execute(sql, (id_persona, usuario, contrasenia))

    id_usuario = cursor.lastrowid

    sql = """SELECT id FROM roles WHERE rol = %s AND habilitado = 1"""

    cursor.execute(sql, (rol,))

    resultado = cursor.fetchone()

    if resultado is None:

        cursor.close()
        conexion.close()
        return

    id_rol = resultado[0]

    sql = """INSERT INTO usuxroles (idUsuario, idRoles) VALUES (%s, %s)"""

    cursor.execute(sql, (id_usuario, id_rol))

    conexion.commit()

    cursor.close()
    conexion.close()

    return True

def buscar_usuario(usuario):

    conexion = conectar()
    cursor = conexion.cursor()

    sql = """SELECT 
            usuarios.usuario,
            usuarios.contraseña, 
            roles.rol
            
            FROM usuarios 
            
            INNER JOIN usuxroles ON usuarios.id = usuxroles.idUsuario 
            
            INNER JOIN roles ON usuxroles.idRoles = roles.id 
            
            WHERE usuarios.usuario = %s 
            
            AND usuarios.habilitado = 1
            AND usuxroleS.habilitado = 1
            AND roles.habilitado = 1"""

    cursor.execute(sql, (usuario,))

    resultado = cursor.fetchone()

    cursor.close()
    conexion.close()

    return resultado
