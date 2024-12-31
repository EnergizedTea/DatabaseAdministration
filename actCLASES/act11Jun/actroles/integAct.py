import psycopg2

conn = psycopg2.connect(
    dbname = "integridad",
    user = "postgres",
    password = "1234",
    host = "localhost",
)

cur = conn.cursor()

# Crear la tabla "Cursos"
cur.execute("""
    CREATE TABLE IF NOT EXISTS Cursos (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL
    )
""")
print("Tabla 'Cursos' creada en la BD")

# Crear la tabla "Estudiantes"
cur.execute("""
    CREATE TABLE IF NOT EXISTS Estudiantes (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(50) NOT NULL,
        edad INT CHECK (edad > 0),
        curso_id INT, 
        FOREIGN KEY (curso_id) REFERENCES Cursos(id)
    )
""")
print("Tabla 'Estudiantes' creada en la BD")

# Crear una función para validar la edad de los estudiantes
cur.execute("""
    CREATE OR REPLACE FUNCTION validar_edad() RETURNS TRIGGER as $$
    BEGIN
        IF NEW.edad <= 0 THEN
            RAISE EXCEPTION 'La edad debe ser mayor a 0';
        END IF;
    RETURN NEW;
    END;
    $$ LANGUAGE plpgsql
""")

# Eliminar el trigger si ya existe
cur.execute("""
    DROP TRIGGER IF EXISTS trigger_validar_edad ON Estudiantes;
""")

# Crear un trigger que utilice la función "validar_edad()"
cur.execute("""
    CREATE TRIGGER trigger_validar_edad
    BEFORE INSERT OR UPDATE ON Estudiantes
    FOR EACH ROW EXECUTE FUNCTION validar_edad();
""")

conn.commit()

def mostrar_menu():
    while True:
        print()
        print("1. Insertar datos")
        print("2. Leer datos")
        print("3. Actualizar datos")
        print("4. Eliminar datos")
        print("5. Salir")
        opcion = int(input("Inserte una opción: "))
        if opcion == 1:
            insertar_datos()
        elif opcion == 2:
            leer_datos()
        elif opcion == 3:
            actualizar_datos()
        elif opcion == 4:
            eliminar_datos()
        elif opcion == 5:
            break
        else:
            print("Favor de insertar una opción válida.")

def insertar_datos():
    nombre_curso = input("Inserte el nombre del curso: ")
    cur.execute("INSERT INTO Cursos (nombre) VALUES (%s) RETURNING id", (nombre_curso,))
    curso_id = cur.fetchone()[0]
    nombre_estudiante = input("Inserte el nombre del estudiante: ")
    edad_estudiante = int(input("Inserte la edad del estudiante: "))
    cur.execute("INSERT INTO Estudiantes (nombre, edad, curso_id) VALUES (%s, %s, %s)", (nombre_estudiante, edad_estudiante, curso_id))
    conn.commit()
    print("Datos insertados exitosamente :)")

def leer_datos():
    cur.execute("SELECT * FROM Estudiantes")
    estudiantes = cur.fetchall()
    print("\nEstudiantes:")
    for estudiante in estudiantes:
        print(estudiante)
    cur.execute("SELECT * FROM Cursos")
    cursos = cur.fetchall()
    print("\nCursos:")
    for curso in cursos:
        print(curso)

def actualizar_datos():
    nombre_estudiante = input ("Inserte el nombre del estudiante: ")
    nueva_edad = int (input ("Inserte la nueva edad del estudiante: "))
    cur. execute("UPDATE Estudiantes SET edad = %s WHERE nombre = %s", (nueva_edad, nombre_estudiante))
    conn.commit()
    print("Datos actualizados exitosamente :)")

def eliminar_datos():
    nombre_estudiante = input("Inserte el nombre del estudiante: ")
    cur.execute("SELECT curso_id FROM Estudiantes WHERE nombre = %s", (nombre_estudiante,))
    curso_id = cur.fetchone()[0]
    cur.execute("DELETE FROM Estudiantes WHERE nombre = %s", (nombre_estudiante,))
    cur. execute ("DELETE FROM Cursos WHERE id = %s", (curso_id,))
    conn.commit()
    print("Datos eliminados exitosamente :)")

mostrar_menu()

cur.close()
conn.close()