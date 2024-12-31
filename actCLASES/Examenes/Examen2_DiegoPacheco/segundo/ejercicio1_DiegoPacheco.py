# Parte de python del Primer Ejercicio, pero Reloaded y ya bien chida como buscaba desde un Principio
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

print("\n-------Inserción de registros-------")

# Inserción de productos
print("\n------- Productos -------")
p1Name = input("\nIntroduzca el Nombre del Primer Producto: ")
p1Desc = input("\nIntroduzca la Descripción del Primer Producto: ")
p1Price = float(input("\nIntroduzca el Precio del Primer Producto: "))

cur.execute("""
    INSERT INTO productos (nombre, descripcion, precio)
    VALUES (%s, %s, %s)
    RETURNING id
""", (p1Name, p1Desc, p1Price))

# Capturamos el id del producto para mostrarlo y confirmar que correctamente se haya guardado
producto1_id = cur.fetchone()[0]
print(f"Producto 1 insertado con ID: {producto1_id}")
conn.commit()


p2Name = input("\nIntroduzca el Nombre del Segundo Producto: ")
p2Desc = input("\nIntroduzca la Descripción del Segundo Producto: ")
p2Price = float(input("\nIntroduzca el Precio del Segundo Producto: "))

cur.execute("""
    INSERT INTO productos (nombre, descripcion, precio)
    VALUES (%s, %s, %s)
    RETURNING id
""", (p2Name, p2Desc, p2Price))

# Capturamos el id del producto para mostrarlo y confirmar que correctamente se haya guardado
producto2_id = cur.fetchone()[0]
print(f"Producto 2 insertado con ID: {producto2_id}")
conn.commit()

# Inserción de clientes
print("\n------- Clientes -------")
c1Name = input("\nIntroduzca el Nombre del Primer Cliente: ")
c1Email = input("\nIntroduzca el Correo del Primer Cliente: ")

cur.execute("""
    INSERT INTO clientes (nombre, email)
    VALUES (%s, %s)
    RETURNING id
""", (c1Name, c1Email))

# Capturamos el id del cliente para mostrarlo y confirmar que correctamente se haya guardado
cliente1_id = cur.fetchone()[0]
print(f"Cliente 1 insertado con ID: {cliente1_id}")
conn.commit()

c2Name = input("\nIntroduzca el Nombre del Segundo Cliente: ")
c2Email = input("\nIntroduzca el Correo del Segundo Cliente: ")

cur.execute("""
    INSERT INTO clientes (nombre, email)
    VALUES (%s, %s)
    RETURNING id
""", (c2Name, c2Email))

# Capturamos el id del cliente para mostrarlo y confirmar que correctamente se haya guardado
cliente2_id = cur.fetchone()[0]
print(f"Cliente 2 insertado con ID: {cliente2_id}")
conn.commit()

# Inserción de ventas
print("\n------- Venta 1 -------")
v1cl = int(input("\nIntroduzca el ID de un Cliente para Venta 1: "))
v1p = int(input("\nIntroduzca el ID de un Producto para Venta 1: "))
v1c = int(input("\nIntroduzca la Cantidad Vendida para Venta 1: "))

cur.execute("""
    INSERT INTO ventas (id_cliente, id_producto, cantidad)
    VALUES (%s, %s, %s)
""", (v1cl, v1p, v1c))

print("Venta 1 insertada correctamente.")

print("\n------- Venta 2 -------")
v2cl = int(input("\nIntroduzca el ID de un Cliente para Venta 2: "))
v2p = int(input("\nIntroduzca el ID de un Producto para Venta 2: "))
v2c = int(input("\nIntroduzca la Cantidad Vendida para Venta 2: "))

cur.execute("""
    INSERT INTO ventas (id_cliente, id_producto, cantidad)
    VALUES (%s, %s, %s)
""", (v2cl, v2p, v2c))

print("Venta 2 insertada correctamente.")

conn.commit()

print("\n------- La Transacción -------")

# Insertar un nuevo cliente y asociar una venta con un producto
cName = input("\nIntroduzca el Nombre del Cliente para la nueva venta: ")
cEmail = input("\nIntroduzca el Correo del Cliente para la nueva venta: ")
pId = int(input("\nIntroduzca el ID del Producto para la nueva venta: "))
vC = int(input("\nIntroduzca la Cantidad Vendida para la nueva venta: "))

try:
    # Insertar un nuevo cliente
    cur.execute("""
        INSERT INTO clientes (nombre, email)
        VALUES (%s, %s)
        RETURNING id
    """, (cName, cEmail))
    
    cliente_id = cur.fetchone()[0]
    print(f"\nCliente insertado con ID: {cliente_id}")

    # Insertar una venta asociada al nuevo cliente y al producto especificado
    cur.execute("""
        INSERT INTO ventas (id_cliente, id_producto, cantidad)
        VALUES (%s, %s, %s)
    """, (cliente_id, pId, vC))
    
    print("Nueva venta insertada correctamente.")

    conn.commit()
    print("Transacción completada exitosamente.")

except Exception as e:
    # Si ocurre un error, revertir la transacción
    conn.rollback()
    print(f"Error durante la transacción: {e}")
    print("Transacción revertida.")
finally:    
    cur.close()
    conn.close()
