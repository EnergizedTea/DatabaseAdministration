# Practica para el segundo examen guia
import psycopg2

# Conectar a la base de datos empresa
conn = psycopg2.connect(
    dbname="empresa",
    user="postgres",
    password="1234",
    host="localhost"
)

# Crear un cursor
cur = conn.cursor()

# Conseguir datos del usuario
print("-------- Insertar Usuario y Pedido --------")
user = input("\nIngrese el Nombre del Usuario:  ")
email = input("\nIngrese el E-Mail del Usuario:  ")
producto = input("\nIngrese el producto a ordenar:  ")
cantidad = input("\nIngrese la cantidad a ordenar:  ")

# Insertar al nuevo usuario
query = (""" INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id; """) 
cur.execute(query, (user, email))
userId = cur.fetchone()[0]

# Inserción del Pedido
query = ("""INSERT INTO pedidos (id_usuario, producto, cantidad) VALUES (%s, %s, %s)""")
cur.execute(query, (userId, producto, cantidad))

# Confirmar las transacciones
conn.commit()

# Recuperación de todo registro de usuarios junto con sus pedidos
cur.execute("""
    SELECT usuarios.id, usuarios.nombre, usuarios.email, pedidos.id, pedidos.producto, pedidos.fecha_creacion
    FROM usuarios
    LEFT JOIN pedidos ON usuarios.id = pedidos.id_usuario;
""")

registros = cur.fetchall()

print("---------------- Resultados ----------------")
for registro in registros:
    print(f"Usuario ID: {registro[0]}, Nombre: {registro[1]}, Email: {registro[2]}, "
          f"Pedido ID: {registro[3]}, Producto: {registro[4]}, Fecha del Pedido: {registro[5]}")

# Cerrar el cursor y la conexión
cur.close()
conn.close()