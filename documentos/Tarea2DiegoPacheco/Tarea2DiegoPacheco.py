# Tarea 2 realizada el 8 de Junio del 2023

import pandas as pd
from sklearn.linear_model import LinearRegression
import sqlalchemy as sa
import psycopg2
import subprocess

conn = psycopg2.connect(
    dbname = "ProductoPrediccion",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

cur = conn.cursor()

# - C - Función para agregar un nuevo producto
def agregarProducto(nombre, precio, presupuesto, ventas):
    query = "INSERT INTO Productos (nombre, precio, presu, ventas) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (nombre, precio, presupuesto, ventas))
    conn.commit()
    print("Producto agregado exitosamente.")

# - R - Función para leer todos los productos
def leerVentas():
    cur.execute("SELECT * FROM Productos")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# - U - Función para actualizar un producto
def actualizarProducto(id, nombre = None, precio = None, presupuesto = None, ventas = None):
    dictionary = {'nombre': nombre, 'precio': precio, 'presu': presupuesto, 'ventas': ventas}
    
    for key in dictionary:
        if dictionary[key] is not None:
            query = f"UPDATE Productos SET {key} = %s WHERE id = %s"
            cur.execute(query, (dictionary[key], id))
    conn.commit()
    print(f"Producto con ID {id} actualizado")

# - D - Función para borrar un producto
def eliminarProducto(id):
    cur.execute("DELETE FROM Productos WHERE id = %s", (id,))
    conn.commit()
    print("Producto eliminado exitosamente.")

# - P - Función para realizar producción
def realizarPrediccion(NPrecio, NPresu):
    engine = sa.create_engine(
        "postgresql://postgres:1234@localhost:5432/ProductoPrediccion"
    )

    # lectura de datos de la tabla "Productos" en un Dataframe de pandas.
    df = pd.read_sql_table("productos", engine)

    # Seleccion de las columnas "precio" y "publicidad" como caracteristicas
    X = df[["precio", "presu"]]

    # Seleccion de la columna "ventas" como variable objetivo
    # la dependiente son las ventas
    y = df["ventas"]

    # Creación y Entrenamiento del Modelo de regresión linbeal

    model = LinearRegression() #instancia de la clase linearRegression
    model.fit(X, y)

    # Realizar predicción
    nuevo_precio = NPrecio
    nueva_publicidad = NPresu # presupuesto de publicidad del nuevo producto

    prediction = model.predict([[nuevo_precio, nueva_publicidad]])

    # Impresión de la Predicción de venta para el nuevo producto
    print("Ventas predichas para el nuevo producto:     ", prediction)

def Menu():
    print(" --------- Menu de Opciones --------- \n\n")
    print("(1)  Crear Producto\n")
    print("(2)  Mostrar Productos\n")
    print("(3)  Actualizar Producto\n")
    print("(4)  Eliminar Producto\n")
    print("(5)  Realizar Predicción\n")
    print("(6)  Cerrar sesión\n")

'''ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        try:
            nombre = input("Introduzca el nombre del producto: ")
            precio = float(input("Introduzca el precio del producto: "))
            presu = float(input("Introduzca el presupuesto: "))
            ventas = int(input("Introduzca las ventas del producto: "))

            agregarProducto(nombre, precio, presu, ventas)
            conn.commit()
        except subprocess.CalledProcessError as e:
            print(f"Error al realizar el metodo: {e}")

    elif op == 2:
        leerVentas()
    
    elif op == 3:
        try:
            idp = int(input("Introduzca el id del producto a modificar:"))

            nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
            nombre = nombre if nombre != '' else None

            precio = input("Introduzca el nuevo precio del producto (o deje en blanco para no cambiar): ")
            precio = float(precio) if precio != '' else None

            presu = input("Introduzca el nuevo presupuesto del producto (o deje en blanco para no cambiar): ")
            presu = float(presu) if presu != '' else None

            ventas = input("Introduzca las ventas del producto (o deje en blanco para no cambiar): ")
            ventas = int(ventas) if ventas != '' else None

            actualizarProducto(idp, nombre, precio, presu, ventas)
            conn.commit()

        except subprocess.CalledProcessError as e:
            print(f"Error al realizar el metodo: {e}")

    elif op == 4:
        id = int(input("Introduzca el ID del producto a eliminar: "))
        eliminarProducto(id)
        conn.commit()

    elif op == 5:
        precio = float(input("Introduzca el precio del producto: "))
        presu = float(input("Introduzca el presupuesto: "))

        realizarPrediccion(precio, presu)

    elif op == 6:
        ex = True
    else:
        print("Opción no válida. Por favor, elija una opción del 1 al 6.")'''

#Ruta del Pg dump

pg_dump_path = r'"/opt/homebrew/Cellar/postgresql@16/16.3/bin/pg_dump"'

def backup_database():
    # comando para hacer una copia de seguridad de una BD
    backup_command = f'{pg_dump_path} -U postgres -F c -b -v -f "Tarea2DiegoPacheco.backup" ProductoPrediccion'

    try:
        subprocess.run(backup_command, check = True, shell=True)
        print("Copia de seguridad realizada con exito")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar la copia de seguridad: {e}")

backup_database()

# Cerrar conexión
cur.close()
conn.close()