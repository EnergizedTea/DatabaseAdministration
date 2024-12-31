import psycopg2

# Conexión a la base de datos (ajustar según tu configuración)
conn = psycopg2.connect(
    dbname="tarea4_diegopacheco",
    user="postgres",
    password="1234",
    host= "localhost"
    )

cur = conn.cursor()

# Creación de las tablas
cur.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL NOT NULL,
    stock INT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    email VARCHAR(100) NOT NULL UNIQUE
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    cliente_id INT NOT NULL REFERENCES clientes(id),
    fecha TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total DECIMAL NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS detalles_pedido (
    id SERIAL PRIMARY KEY,
    pedido_id INT NOT NULL REFERENCES pedidos(id),
    producto_id INT NOT NULL REFERENCES productos(id),
    cantidad INT NOT NULL,
    precio DECIMAL NOT NULL
);
""")

conn.commit()  # Guardar los cambios en la base de datos

def crear_pedido(cliente_id, productos):
    try:
        conn = psycopg2.connect("dbname=nombre_basedatos user=usuario password=password")
        cur = conn.cursor()

        # Iniciar la transacción
        cur.execute("BEGIN;")

        # Calcular el total del pedido
        total_pedido = 0

        # Insertar en la tabla de pedidos
        cur.execute("INSERT INTO pedidos (cliente_id, total) VALUES (%s, %s) RETURNING id", (cliente_id, total_pedido))
        pedido_id = cur.fetchone()[0]

        # Insertar en la tabla de detalles_pedido
        for producto in productos:
            producto_id = producto['id']
            cantidad = producto['cantidad']
            precio_unitario = producto['precio']

            cur.execute("""
                INSERT INTO detalles_pedido (pedido_id, producto_id, cantidad, precio)
                VALUES (%s, %s, %s, %s)
            """, (pedido_id, producto_id, cantidad, precio_unitario))

            # Actualizar el stock del producto
            cur.execute("UPDATE productos SET stock = stock - %s WHERE id = %s", (cantidad, producto_id))

            # Calcular el total del pedido
            total_pedido += cantidad * precio_unitario

        # Actualizar el total en la tabla de pedidos
        cur.execute("UPDATE pedidos SET total = %s WHERE id = %s", (total_pedido, pedido_id))

        # Commit de la transacción
        conn.commit()
        print("Pedido creado exitosamente.")

    except Exception as e:
        # Rollback en caso de error
        conn.rollback()
        print(f"Error al crear el pedido: {e}")

    finally:
        # Cerrar la conexión
        if conn:
            conn.close()
