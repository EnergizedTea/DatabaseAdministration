# Actividad realizada en clase el 3 de junio del 2024
import psycopg2

conn = psycopg2.connect(
    dbname = "escuela",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

cur = conn.cursor()

cur.execute("INSERT INTO Estudiantes (nombre, edad) VALUES (%s, %s) RETURNING id", ("Dado", 20))
id_juan = cur.fetchone()[0]

cur.execute("INSERT INTO Cursos (nombre) VALUES (%s) RETURNING id", ("Bases de Datos",))
id_curso = cur.fetchone()[0]

cur.execute("INSERT INTO Inscripciones (estudiante_id, curso_id) VALUES (%s, %s)", (id_juan, id_curso))

conn.commit()

cur.execute("SELECT * FROM Estudiantes")
print(cur.fetchall())

# CARACTERISTICAS DE LOS DBMS

# Mostrar los roles en la BD
cur.execute("SELECT rolname FROM pg_roles")
print("Roles:   ")
roles = cur.fetchall()
for role in roles:
    print(role[0])

# Mostrar los indices de las tablas
cur.execute("SELECT tablename, indexname FROM pg_indexes WHERE schemaname = 'public'")
print("Indices:")
indexes = cur.fetchall()
for index in indexes:
    print(index[0], "-", index[1])

# Estadistica de tablas
cur.execute("SELECT relname, seq_scan, seq_tup_read, idx_scan, idx_tup_fetch FROM pg_stat_user_tables")
estadistica = cur.fetchall()
for stat in estadistica:
    print(stat[0], "-", "Seq Scan:", stat[1], "Seq Tup Read:", stat[2], "idx_scan:", stat[3], "Idx_tup_fetch:", stat[4])

# Cerrar conexión
cur.close()
conn.close()
