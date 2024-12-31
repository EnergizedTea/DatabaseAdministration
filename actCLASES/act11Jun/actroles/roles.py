import psycopg2

conn = psycopg2.connect(
    dbname = "integridad",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

cur = conn.cursor()

# Crear los roles
cur.execute("CREATE ROLE admin1;")
cur.execute("CREATE ROLE lector1;")

# Asignar permisos a los roles
cur.execute("GRANT ALL PRIVILEGES ON DATABASE integridad TO admin1;")
cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO lector1")

# Crear usuarios y asignar roles
cur.execute("CREATE USER usuario_admin WITH PASSWORD 'admin123';")
cur.execute("CREATE USER usuario_lector WITH PASSWORD 'lector123';")

# Asignacion de Rol a Usuario
cur.execute("GRANT admin1 TO usuario_admin;")
cur.execute("GRANT lector1 TO usuario_lector;")

conn.commit()

print("Roles y permisos asignados correctamente")


cur.close()
conn.close()