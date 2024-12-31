# Libreria para conexión con postges
import psycopg2

conn = psycopg2.connect(
    dbname = "BD.test",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

cur = conn.cursor()

#Crear tabla en la base datos con el nombre Estudiamtes
cur.execute("""
    CREATE TABLE IF NOT EXISTS Estudiantes(
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100),
        edad INT        
    )
""")

print("Tabla 'estudiantes' creada en la BD")

def insertarEstudiantes(nombre, edad):
    cur.execute("INSERT INTO Estudiantes (nombre, edad) VALUES (%s, %s)", (nombre, edad))
    print(f"Estudiante {nombre} insertado.")

def leerEstudiantes():
    cur.execute("SELECT * FROM Estudiantes")
    rows = cur.fetchall()
    for row in rows:
        print(row)

def actualizarEstudiante(id, nuevoNombre, nuevaEdad):
    cur.execute("UPDATE Estudiante SET nombre = %s, edad = %s WHERE id = %s", (nuevoNombre, nuevaEdad, id))
    print(f"Estudiante con ID {id} actualizado.")

def eliminarEstudiante(id):
    cur.execute("DELETE FROM Estudiantes WHERE id = %s", (id,))
    print(f"Estudiante con ID {id} eliminado.")

#Operaciones Crud
#Insertar datos
#insertarEstudiantes("Juan", 21)
#insertarEstudiantes("Maria", 22)

leerEstudiantes()

conn.commit()
cur.close()
conn.close()