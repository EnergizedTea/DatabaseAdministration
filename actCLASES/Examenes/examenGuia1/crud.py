# Actividad realizada en clase el 6 de junio del 2024 en preparación para el examen del viernes
import psycopg2

conn = psycopg2.connect(
    dbname = "Guia1",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

cur = conn.cursor()

def leerCategorias():
    cur.execute("SELECT * FROM Categorias")
    rows = cur.fetchall()
    print("Categorias:")
    for row in rows:
        print(row)

def leerPedidos():
    cur.execute("SELECT * FROM Pedidos")
    rows = cur.fetchall()
    print("Pedidos:")
    for row in rows:
        print(row)


# - C - Función para crear una nueva categoría
def crearCategoria(nombre):
    query = "INSERT INTO Categorias (nombre) VALUES (%s)"
    cur.execute(query, (nombre,))
    conn.commit()
    print("Categoría creada exitosamente.")

# - C - Función para crear un nuevo producto
def crearProducto(nombre, precio, id_categoria):
    cur.execute("INSERT INTO Productos (nombre, precio, id_categoria) VALUES (%s, %s, %s)", (nombre, precio, id_categoria))
    conn.commit()
    print(f"Producto {nombre} creado exitosamente.")

# - C - Función para crear un nuevo pedido
def crearPedido(id_producto, fecha_pedido, cantidad):
    query = "INSERT INTO Pedidos (id_producto, fecha_pedido, cantidad) VALUES (%s, %s, %s)"
    cur.execute(query, (id_producto, fecha_pedido, cantidad))
    conn.commit()
    print("Pedido creado exitosamente.")

# - R - Función para leer todos los productos
def leerProductos():
    cur.execute("SELECT * FROM Productos")
    rows = cur.fetchall()
    for row in rows:
        print(row)

# - U - Función para actualizar un producto
def actualizarProducto(id, nombre=None, precio=None, id_categoria=None):
    dictionary = {'nombre': nombre, 'precio': precio, 'id_categoria': id_categoria}
    
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

def Menu():
    print(" --------- Menu de Opciones --------- \n\n")
    print("(1)  Crear Categoria\n")
    print("(2)  Crear Producto\n")
    print("(3)  Leer Productos\n")
    print("(4)  Actualizar Producto\n")
    print("(5)  Eliminar Producto\n")
    print("(6)  Generar Reporte\n")
    print("(7)  Crear Pedido\n")
    print("(12)  Cerrar sesión\n")

def generarReporte():
    # Define the SQL query
    query = """
    SELECT 
        c.nombre AS categoria,
        SUM(ped.cantidad) AS total_productos_vendidos,
        SUM(ped.cantidad * prod.precio) AS total_ingresos
    FROM 
        Categorias c
    JOIN 
        Productos prod ON c.id = prod.id_categoria
    JOIN 
        Pedidos ped ON prod.id = ped.id_producto
    GROUP BY 
        c.nombre;
    """
    # Execute the SQL query
    cur.execute(query)
    rows = cur.fetchall()

    # Print the report
    print(f"{'Categoría':<20} {'Total Productos Vendidos':<25} {'Total Ingresos':<15}")
    print("-" * 60)
    for row in rows:
        categoria, total_productos_vendidos, total_ingresos = row
        print(f"{categoria:<20} {total_productos_vendidos:<25} {total_ingresos:<15.2f}")

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        nombre = input("Introduzca el nombre de la categoría: ")
        crearCategoria(nombre)
        conn.commit()
    elif op == 2:
        nombre = input("Introduzca el nombre del producto: ")
        precio = float(input("Introduzca el precio del producto: "))
        id_categoria = int(input("Introduzca el ID de la categoría del producto: "))
        crearProducto(nombre, precio, id_categoria)
        conn.commit()
    elif op == 3:
        leerProductos()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerCategorias()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerPedidos()
    elif op == 4:
        idp = int(input("Introduzca el id del producto a modificar:"))

        nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
        nombre = nombre if nombre != '' else None

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        nombre = input("Introduzca el nombre de la categoría: ")
        crearCategoria(nombre)
        conn.commit()
    elif op == 2:
        nombre = input("Introduzca el nombre del producto: ")
        precio = float(input("Introduzca el precio del producto: "))
        id_categoria = int(input("Introduzca el ID de la categoría del producto: "))
        crearProducto(nombre, precio, id_categoria)
        conn.commit()
    elif op == 3:
        leerProductos()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerCategorias()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerPedidos()
    elif op == 4:
        idp = int(input("Introduzca el id del producto a modificar:"))

        nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
        nombre = nombre if nombre != '' else None

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        nombre = input("Introduzca el nombre de la categoría: ")
        crearCategoria(nombre)
        conn.commit()
    elif op == 2:
        nombre = input("Introduzca el nombre del producto: ")
        precio = float(input("Introduzca el precio del producto: "))
        id_categoria = int(input("Introduzca el ID de la categoría del producto: "))
        crearProducto(nombre, precio, id_categoria)
        conn.commit()
    elif op == 3:
        leerProductos()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerCategorias()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerPedidos()
    elif op == 4:
        idp = int(input("Introduzca el id del producto a modificar:"))

        nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
        nombre = nombre if nombre != '' else None

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        nombre = input("Introduzca el nombre de la categoría: ")
        crearCategoria(nombre)
        conn.commit()
    elif op == 2:
        nombre = input("Introduzca el nombre del producto: ")
        precio = float(input("Introduzca el precio del producto: "))
        id_categoria = int(input("Introduzca el ID de la categoría del producto: "))
        crearProducto(nombre, precio, id_categoria)
        conn.commit()
    elif op == 3:
        leerProductos()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerCategorias()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerPedidos()
    elif op == 4:
        idp = int(input("Introduzca el id del producto a modificar:"))

        nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
        nombre = nombre if nombre != '' else None

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        nombre = input("Introduzca el nombre de la categoría: ")
        crearCategoria(nombre)
        conn.commit()
    elif op == 2:
        nombre = input("Introduzca el nombre del producto: ")
        precio = float(input("Introduzca el precio del producto: "))
        id_categoria = int(input("Introduzca el ID de la categoría del producto: "))
        crearProducto(nombre, precio, id_categoria)
        conn.commit()
    elif op == 3:
        leerProductos()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerCategorias()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerPedidos()
    elif op == 4:
        idp = int(input("Introduzca el id del producto a modificar:"))

        nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
        nombre = nombre if nombre != '' else None

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        nombre = input("Introduzca el nombre de la categoría: ")
        crearCategoria(nombre)
        conn.commit()
    elif op == 2:
        nombre = input("Introduzca el nombre del producto: ")
        precio = float(input("Introduzca el precio del producto: "))
        id_categoria = int(input("Introduzca el ID de la categoría del producto: "))
        crearProducto(nombre, precio, id_categoria)
        conn.commit()
    elif op == 3:
        leerProductos()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerCategorias()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerPedidos()
    elif op == 4:
        idp = int(input("Introduzca el id del producto a modificar:"))

        nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
        nombre = nombre if nombre != '' else None

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        nombre = input("Introduzca el nombre de la categoría: ")
        crearCategoria(nombre)
        conn.commit()
    elif op == 2:
        nombre = input("Introduzca el nombre del producto: ")
        precio = float(input("Introduzca el precio del producto: "))
        id_categoria = int(input("Introduzca el ID de la categoría del producto: "))
        crearProducto(nombre, precio, id_categoria)
        conn.commit()
    elif op == 3:
        leerProductos()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerCategorias()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerPedidos()
    elif op == 4:
        idp = int(input("Introduzca el id del producto a modificar:"))

        nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
        nombre = nombre if nombre != '' else None

ex = False
while not ex:
    Menu()
    try:
        op = int(input("\nIntroduzca su opción: "))
    except ValueError:
        print("Por favor, introduzca un número válido.")
        continue

    if op == 1:
        nombre = input("Introduzca el nombre de la categoría: ")
        crearCategoria(nombre)
        conn.commit()
    elif op == 2:
        nombre = input("Introduzca el nombre del producto: ")
        precio = float(input("Introduzca el precio del producto: "))
        id_categoria = int(input("Introduzca el ID de la categoría del producto: "))
        crearProducto(nombre, precio, id_categoria)
        conn.commit()
    elif op == 3:
        leerProductos()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerCategorias()
        print("-.-.-.-.-.-.-.-.-.-.-.-.-.-.-")
        leerPedidos()
    elif op == 4:
        idp = int(input("Introduzca el id del producto a modificar:"))

        nombre = input("Introduzca el nuevo nombre del producto (o deje en blanco para no cambiar): ")
        nombre = nombre if nombre != '' else None

        precio = input("Introduzca el nuevo precio del producto (o deje en blanco para no cambiar): ")
        precio = float(precio) if precio != '' else None

        id_categoria = input("Introduzca el nuevo ID de la categoría del producto (o deje en blanco para no cambiar): ")
        id_categoria = int(id_categoria) if id_categoria != '' else None

        actualizarProducto(idp, nombre, precio, id_categoria)
        conn.commit()
    elif op == 5:
        id = int(input("Introduzca el ID del producto a eliminar: "))
        eliminarProducto(id)
        conn.commit()
    elif op == 6:
        generarReporte()

    elif op == 7:
        id_Producto = int(input("Introduzca el id del producto: "))
        fecha = input("Introduzca la fecha del pedido (YYYY-MM-DD): ")
        cantidad = int(input("Introduzca la cantidad de productos: "))
        crearPedido(id_Producto, fecha, cantidad)
        conn.commit()

    elif op == 12:
        ex = True
    else:
        print("Opción no válida. Por favor, elija una opción del 1 al 6.")

# Cerrar conexión
cur.close()
conn.close()
