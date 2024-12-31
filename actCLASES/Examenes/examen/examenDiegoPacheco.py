# Primer Examen Parcial del Curso en Administración de Bases de Datos Verano 2024, Realizado por Diego Pacheco Valdez
import psycopg2
import subprocess

conn = psycopg2.connect(
    dbname = "biblioteca",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

cur = conn.cursor()

# - C - Función para agregar un nuevo autor
def crearAutor(nombre, nacionalidad):
    query = "INSERT INTO Autores (nombre, nacionalidad) VALUES (%s, %s)"
    cur.execute(query, (nombre,nacionalidad))
    conn.commit()
    print("Autor agregado exitosamente.")

# - C - Función para agregar un nuevo libro
def crearLibro(titulo, genero, precio, id_autor):
    query = "INSERT INTO Libros (titulo, genero, precio, id_autor) VALUES (%s, %s, %s, %s)"
    cur.execute(query, (titulo, genero, precio, id_autor))
    conn.commit()
    print("Libro agregado exitosamente.")

# - C - Función para agregar una nueva venta
def crearVenta(id_libro, fecha_venta, cantidad):
    query = "INSERT INTO Ventas (id_libro, fecha_venta, cantidad) VALUES (%s, %s, %s)"
    cur.execute(query, (id_libro, fecha_venta, cantidad))
    conn.commit()
    print("Venta agregada exitosamente.")

# - R - Función para leer todos los libros
def leerLibros():
    cur.execute("SELECT * FROM Libros")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# - U - Función para actualizar un libro
def actualizarLibro(id, titulo=None, genero=None, precio=None, id_autor=None):
    dictionary = {'titulo': titulo, 'genero': genero, 'precio': precio, 'id_autor': id_autor}
    
    for key in dictionary:
        if dictionary[key] is not None:
            query = f"UPDATE Libros SET {key} = %s WHERE id = %s"
            cur.execute(query, (dictionary[key], id))
    conn.commit()
    print(f"Libro con ID {id} actualizado")

# - D - Función para borrar un libro
def eliminarLibro(id):
    cur.execute("DELETE FROM Libro WHERE id = %s", (id,))
    conn.commit()
    print("Libro eliminado exitosamente.")

def Menu():
    print(" --------- Menu de Opciones --------- \n\n")
    print("(1)  Crear Autor\n")
    print("(2)  Crear Libro\n")
    print("(3)  Crear Venta\n")
    print("(4)  Mostrar Libros\n")
    print("(5)  Actualizar Libro\n")
    print("(6)  Eliminar Libro\n")
    print("(8)  Cerrar sesión\n")

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        try:
            nombre = input("Introduzca el nombre del autor: ")
            nacionalidad = input("Introduzca la nacionalidad del autor: ")
            crearAutor(nombre, nacionalidad)
            conn.commit()
        except subprocess.CalledProcessError as e:
            print(f"Error al realizar el metodo: {e}")

    elif op == 2:
        try:
            titulo = input("Introduzca el titulo del libro: ")
            genero = input("Introduzca el genero del libro: ")
            precio = float(input("Introduzca el precio del libro: "))
            id_autor = int(input("Introduzca el id del autor del libro: "))
            crearLibro(titulo, genero, precio, id_autor)
            conn.commit()
        except subprocess.CalledProcessError as e:
            print(f"Error al realizar el metodo: {e}")

    elif op == 3:
        try:
            id_libro = int(input("Introduzca el id del libro: "))
            fecha_venta = input("Introduzca la fecha de la venta (YYYY-MM-DD): ")
            cantidad = input("Introduzca la cantidad de libros adquiridos: ")
            crearVenta(id_libro, fecha_venta, cantidad)
            conn.commit()
        except subprocess.CalledProcessError as e:
            print(f"Error al realizar el metodo: {e}")
    elif op == 4:
        leerLibros()
    elif op == 5:
        idp = int(input("Introduzca el id del libro a modificar:"))

        titulo = input("Introduzca el nuevo titulo del libro (o deje en blanco para no cambiar): ")
        titulo = titulo if titulo != '' else None

        genero = input("Introduzca el nuevo genero del libro (o deje en blanco para no cambiar): ")
        genero = genero if genero != '' else None

        precio = input("Introduzca el nuevo precio del libro (o deje en blanco para no cambiar): ")
        precio = float(precio) if precio != '' else None

        id_autor = input("Introduzca el nuevo ID del autor del libro (o deje en blanco para no cambiar): ")
        id_autor = int(id_autor) if id_autor != '' else None

        actualizarLibro(idp, titulo, genero, precio, id_autor)
        conn.commit()
    elif op == 6:
        id = int(input("Introduzca el ID del libro a eliminar: "))
        eliminarLibro(id)
        conn.commit()

    elif op == 7:
        print("WORK IN PROGRESS")

    elif op == 8:
        ex = True
    else:
        print("Opción no válida. Por favor, elija una opción del 1 al 6.")

#Ruta del Pg dump

'''pg_dump_path = r'"/opt/homebrew/Cellar/postgresql@16/16.3/bin/pg_dump"'

def backup_database():
    # comando para hacer una copia de seguridad de una BD
    backup_command = f'{pg_dump_path} -U postgres -F c -b -v -f "examenDiegoPacheco.backup" biblioteca'

    try:
        subprocess.run(backup_command, check = True, shell=True)
        print("Copia de seguridad realizada con exito")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar la copia de seguridad: {e}")

backup_database()'''

# Cerrar conexión
cur.close()
conn.close()


