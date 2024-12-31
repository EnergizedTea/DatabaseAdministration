import psycopg2

# Conectar a la base de datos empresa
conn = psycopg2.connect(
    dbname="empresa",
    user="psycopg2",
    password="1234",
    host="localhost"
)

# Crear un cursor
cur = conn.cursor()

# Insertar un nuevo usuario
query = ("""
    INSERT INTO usuarios (nombre, email)
    VALUES (%s, %s)
    RETURNING id;
""") 
cur.execute(query, ('Nuevo Usuario', 'nuevo_usuario@example.com'))

# Obtener el ID del nuevo usuario insertado
nuevo_usuario_id = cur.fetchone()[0]

# Insertar un nuevo pedido relacionado con el usuario recién agregado
cur.execute("""
    INSERT INTO pedidos (id_usuario, producto, fecha_creacion)
    VALUES (%s, %s, CURRENT_DATE);
""", (nuevo_usuario_id, 'Nuevo Producto'))

# Confirmar las transacciones
conn.commit()

# Recuperar y mostrar todos los registros de usuarios junto con sus pedidos
cur.execute("""
    SELECT u.id, u.nombre, u.email, p.id AS pedido_id, p.producto, p.fecha_creacion
    FROM usuarios u
    LEFT JOIN pedidos p ON u.id = p.id_usuario;
""")

# Obtener todos los resultados
resultados = cur.fetchall()

# Mostrar los resultados
for fila in resultados:
    print(f"Usuario ID: {fila[0]}, Nombre: {fila[1]}, Email: {fila[2]}, "
          f"Pedido ID: {fila[3]}, Producto: {fila[4]}, Fecha del Pedido: {fila[5]}")

# Cerrar el cursor y la conexión
cur.close()
conn.close()
