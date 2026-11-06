import mysql.connector

def conectar():

    conexion = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="1234",
        database="menu"
    )

    return conexion