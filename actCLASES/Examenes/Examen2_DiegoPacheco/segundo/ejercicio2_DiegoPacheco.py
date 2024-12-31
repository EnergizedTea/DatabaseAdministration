# Segundo Intento del Examen realizado por Diego Pacheco Valdez
import psycopg2

# Conectarse a la base de datos
conn = psycopg2.connect(
    dbname="almacen",
    user="postgres",
    password="1234",
    host="localhost"
)

# Crear cursor
cur = conn.cursor()

print("\n---------- Inserción de un Nuevo Producto -----------")
pNombre = input("\nIntroduzca el Nombre del Producto:     ")
pDesc = input("\nIntroduzca la Descripción del Producto:     ")
pPrecio = float(input("\nIntroduzca el Precio del Producto:     "))

cur.execute("""
    INSERT INTO productos (nombre, descripcion, precio)
    VALUES (%s, %s, %s)
    RETURNING id
""", (pNombre, pDesc, pPrecio))

# Acceder al id del Producto
idProducto = cur.fetchone()[0]

print(f"Producto con ID {idProducto} Creado Correctamente")

# Guardar el nuevo Producto
conn.commit()

print("\n---------- Inserción de un Nuevo Cliente -----------")
cNombre = input("\nIntroduzca el Nombre del Cliente:     ")
cEmail = input("\nIntroduzca el Correo del Cliente:     ")

cur.execute("""
    INSERT INTO clientes (nombre, email)
    VALUES (%s, %s)
    RETURNING id
""", (cNombre, cEmail))

# Acceder al id del Cliente
idCliente = cur.fetchone()[0]

print(f"Cliente con ID {idCliente} Agregado Correctamente")

# Guardar el nuevo Cliente
conn.commit()

print("\n---------- Recuperar y Mostrar Registros de la Tabla Productos -----------")
# Se selecciona todo lo que hay en productos
cur.execute("SELECT * FROM productos")

# Almacenamos lo seleccionados en productos
productos = cur.fetchall()

# Se imprime producto por producto
for producto in productos:
    print(producto)

print("\n---------- Recuperar y Mostrar Registros de la Tabla Clientes -----------")
# Se selecciona todo lo que hay en clientes
cur.execute("SELECT * FROM clientes")

# Almacenamos lo seleccionados en clientes
clientes = cur.fetchall()

# Se imprime cliente por cliente
for cliente in clientes:
    print(cliente)

print("\n---------- Inserción de una Nueva Venta -----------")
vCliente = input("\nIntroduzca el id del Cliente:     ")
vProducto = input("\nIntroduzca el id del Producto:     ")
vCantidad = int(input("\nIntroduzca la Cantidad de la Orden:     "))

cur.execute("""
    INSERT INTO ventas (id_cliente, id_producto, cantidad)
    VALUES (%s, %s, %s)
    RETURNING id
""", (vCliente, vProducto, vCantidad))

# Acceder al id de la Venta
idVenta = cur.fetchone()[0]

print(f"Venta con ID {idVenta} Realizada Correctamente")

# Guardar la nueva venta
conn.commit()

# Recuperar y mostrar registros de la tabla ventas con join para incluir nombres de clientes y productos
print("\n---------- Recuperar y mostrar registros de la tabla ventas -----------")
print("\n-------------------- con join para incluir nombres --------------------")
print("\n---------------------- de clientes y productos ------------------------")

# En este execute se consiguen los datos a mostrar
cur.execute("""
    SELECT ventas.id, clientes.nombre, productos.nombre, ventas.fecha_ventas
    FROM ventas
    JOIN clientes ON ventas.id_cliente = clientes.id
    JOIN productos ON ventas.id_producto = productos.id
""")

# Ahora que ya tenemos el join, lo capturamos con el cur.fetchall() y lo almacenamos en ventas

ventas = cur.fetchall()
for venta in ventas:
    print(venta)

# Cerramos las conexiones :D
cur.close()
conn.close()