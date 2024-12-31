import psycopg2
import subprocess

contraseña = "1234"

# funcion para crear la base de datos y la tabla (instalar y configurar)
def crear_db_y_tabla():
    try:
        #conectarnos
        conn = psycopg2.connect(dbname = 'postgres', user = 'postgres', password = contraseña, host = 'localhost')
        conn.autocommit = True
        cur = conn.cursor()
        
        # Crear la base de datos
        cur.execute("CREATE DATABASE testdb")
        print("Base de datos 'testdb creada")

        # conectar a la nueva BD
        conn.close()
        conn = psycopg2.connect(dbname = 'testdb', user = 'postgres', password = contraseña, host = 'localhost')
        cur = conn.cursor()

        # Crear tabla
        cur.execute("""
            CREATE TABLE empleados(
                id SERIAL PRIMARY KEY,
                nombre VARCHAR(100),
                puesto VARCHAR(100),
                salario DECIMAL
            );
        """)
        conn.commit()
        print("Tabla 'empleados' creada en la BD")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Funcion para asignar roles y permisos
def asignar_roles_y_permisos():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(dbname = 'testdb', user = 'postgres', password = contraseña, host = 'localhost')
        cur = conn.cursor()

        # Crear rol
        cur.execute("CREATE ROLE analista;")

        # Asignar permisos
        cur.execute("GRANT CONNECT ON DATABASE testdb TO analista;")
        cur.execute("GRANT USAGE ON SCHEMA public TO analista;")
        cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO analista;")
        conn.commit()
        print("Rol 'analista' creado y permisos asignados")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

# Realizar respaldo
def realizar_respaldo():
    try:
        backup_file = "testdb_backup.backup"
        comando = f"pg_dump -U postgres -F c -b -v -f {backup_file} testdb"
        subprocess.run(comando, shell = True)
        print(f"Respaldo de la base de datos 'testdb' almacenado en {backup_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar el respaldo: {e}")
    

# Funcion para ejecutar la consulta y optimizarla
def optimizar_consulta():
    conn = None
    cur = None
    try:
        # conectar a la base de datos testdb
        conn = psycopg2.connect(dbname = "testdb", user = "postgres", password = contraseña, host = "localhost")
        cur = conn.cursor()

        #Insertar datos
        cur.execute("""
            INSERT INTO empleados (nombre, puesto, salario) VALUES
            ('Moises Rodriguez', 'DBA', 80000) ,
            ('Antia Barron', 'CEO', 10000),
            ('Diego Valdez', 'Monstruo Come Galletas', 1000000);
        """)
        conn.commit()

        # Ejecutar y optimizar la consulta
        cur.execute("EXPLAIN ANALYZE SELECT * FROM empleados WHERE puesto = 'DBA';")
        resultado = cur.fetchall()
        for row in resultado:
            print(row)
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

crear_db_y_tabla()
asignar_roles_y_permisos()
realizar_respaldo()
optimizar_consulta()
