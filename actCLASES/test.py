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
    cur.execute("INSERT INTO Estudiantes (nombre, edad) VALUES")

conn.commit()
cur.close()
conn.close()