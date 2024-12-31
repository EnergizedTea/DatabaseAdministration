# Parte de python del Primer Ejercicio
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

# Inserción de productos
p1N = "producto1"
p1des = "desc1"
pp1 = 14.00

p2N = "producto2"
p2des = "desc2"
pp2 = 7.00

cur.execute("""
    INSERT INTO productos (nombre, descripcion, precio)
    VALUES (%s, %s, %s), (%s, %s, %s)
""", (p1N, p1des, pp1, p2N, p2des, pp2))

conn.commit()

# Inserción de Clientes
c1N = "clien1"
c1C = "co1@gmail.com"

c2N = "clien2"
c2C = "co2@gmail.com"

cur.execute("""
    INSERT INTO clientes (nombre, email)
    VALUES (%s, %s), (%s, %s)
""", (c1N, c1C, c2N,c2C))

conn.commit()

# insercion de ventas

v1cl = 1
v1p = 1
v1c = 134

v2cl = 2
v2p = 2
v2c = 134

cur.execute("""
    INSERT INTO ventas (id_cliente, id_producto, cantidad)
    VALUES (%s, %s, %s), (%s, %s, %s)
""", (v1cl, v1p, v1c, v2cl, v2p, v2c))

conn.commit()

try:
    # Insertar un nuevo cliente
    cName = input("Introduzca el Nombre del Nuevo Cliente:  ")
    cEmail = input("Introduzca el Correo del Nuevo Cliente:     ")

    cur.execute("""
        INSERT INTO clientes (nombre, email)
        VALUES (%s, %s)
        RETURNING id
    """, (cName, cEmail))

    cId = cur.fetchone()[0]
    print(f"Nuevo cliente insertado con ID: {cId}")

    # Insertar una venta asociada al cliente y a uno de los productos
    vpID = int(input("Introduzca el ID del Producto para la Venta:  "))
    vC = int(input("Introduzca la Cantidad Vendida:     "))

    cur.execute("""
        INSERT INTO ventas (id_cliente, id_producto, cantidad)
        VALUES (%s, %s, %s)
    """, (cId, vpID, vC))

    # Commit de la transacción
    conn.commit()

except psycopg2.Error as e:
    # Revertir la transacción si ocurre algún error
    conn.rollback()
    print(f"Error durante la transacción: {e}")
    print("Transacción revertida.")

finally:
    # Cerrar cursor y conexión
    cur.close()
    conn.close()

