# Actividad #4 Diego Pacheco Valdez
import psycopg2
import time
import subprocess

conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

conn.autocommit = True

cur = conn.cursor()

cur.execute("DROP DATABASE IF EXISTS bd_transacciones;")
cur.execute("CREATE DATABASE bd_transacciones;")
#print("Base de datos 'bd_transacciones' creada exitosamente")

cur.close()
conn.close()
#print("Conexión cerrada")

# Conectar a la nueva base de datos
conn = psycopg2.connect(
    dbname = "bd_transacciones",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

# Crear el cursor
cur = conn.cursor()

# Crear tabla "Cuentas"
cur.execute("""
CREATE TABLE IF NOT EXISTS Cuentas (
    id SERIAL PRIMARY KEY,
    saldo DECIMAL NOT NULL
    );
""")
#print("Tabla 'Cuentas' creada en la BD")

# Comenzar con dos cuentas hechas
cur.execute("INSERT INTO Cuentas (saldo) VALUES (1000), (2000)")
            
# Confirmar transacciones
conn.commit()

# Función para abrir cuentas
def abrir_cuenta(saldo):
    cur.execute("INSERT INTO Cuentas (saldo) VALUES (%s)", (saldo,))
    print(f"Cuenta creada con {saldo}.")
    # Confirmar transacciones
    conn.commit()

# Función para realizar el retiro de un monto especifico de dinero
def retiro(id_cuenta, monto):
    max_intentos = 3
    intento = 0
    while intento < max_intentos:
        try:
            intento += 1
            cur.execute("BEGIN;")
            # Obtener saldo actual y bloquear la fila para evitar modificaciones concurrentes
            cur.execute("SELECT saldo FROM Cuentas WHERE id = %s FOR UPDATE;", (id_cuenta,))
            saldo_actual = cur.fetchone()[0]
            nuevo_saldo = saldo_actual - monto
            if nuevo_saldo < 0:
                raise Exception("Saldo insuficiente.")
            # Actualizar el saldo de la cuenta
            cur.execute("UPDATE Cuentas SET saldo = %s WHERE id = %s;", (nuevo_saldo, id_cuenta))
            cur.execute("COMMIT;")
            print(f"Transacción completada exitosamente.")
            print(f"El nuevo saldo es: {nuevo_saldo}")
            break
        except Exception as e:
            cur.execute("ROLLBACK;")
            print(f"Error en la transacción: {e}")
            if intento == max_intentos:
                print(f"Transacción fallida después de {max_intentos} intentos.")
            else: 
                decision = int(input("¿Desea cambiar el monto? Sí (1) o No (2): "))
                if decision == 1:
                    monto = int(input("Inserte el nuevo monto: "))
                    print(f"Reintentando transacción (intento {intento})")
                elif decision == 2:
                    print(f"Reintentando transacción (intento {intento})")
                    time.sleep(1)
                else:
                    print("Inserte una opción válida, los intentos siguen contando.")

# Función para realizar un depósito de dinero
def deposito(id_cuenta, monto):
    max_intentos = 3
    intento = 0
    max_limite = 30000
    while intento < max_intentos:
        try:
            intento += 1
            cur.execute("BEGIN;")
            # Obtener saldo actual y bloquear la fila para evitar modificaciones concurrentes
            cur.execute("SELECT saldo FROM Cuentas WHERE id = %s FOR UPDATE;", (id_cuenta,))
            saldo_actual = cur.fetchone()[0]
            nuevo_saldo = saldo_actual + monto
            if nuevo_saldo > max_limite:
                raise Exception("Límite rebasado.")
            # Actualizar el saldo de la cuenta
            cur.execute("UPDATE Cuentas SET saldo = %s WHERE id = %s;", (nuevo_saldo, id_cuenta))
            cur.execute("COMMIT;")
            print(f"Transacción completada exitosamente.")
            print(f"El nuevo saldo es: {nuevo_saldo}")
            break
        except Exception as e:
            cur.execute("ROLLBACK;")
            print(f"Error en la transacción: {e}")
            if intento == max_intentos:
                print(f"Transacción fallida después de {max_intentos} intentos.")
            else:
                decision = int(input("¿Desea cambiar el monto? Sí (1) o No (2): "))
                if decision == 1:
                    monto = int(input("Inserte el nuevo monto: "))
                    print(f"Reintentando transacción (intento {intento})")
                elif decision == 2:
                    print(f"Reintentando transacción (intento {intento})")
                    time.sleep(1)
                else:
                    print("Inserte una opción válida, los intentos siguen contando.")

# Función para probar los diferentes niveles de aislamiento
def probar_aislamiento(nivel_aislamiento):
    try:
        cur.execute(f"SET TRANSACTION ISOLATION LEVEL {nivel_aislamiento};")
        cur.execute("BEGIN;")
        cur.execute("SELECT saldo FROM Cuentas WHERE id = 1;")
        saldo_actual = cur.fetchone()[0]
        print(f"Saldo actual (nivel {nivel_aislamiento}): {saldo_actual}")
        cur.execute("COMMIT;")
    except Exception as e:
        cur.execute("ROLLBACK;")
        print(f"Error en la transacción: {e}")

'''# Probar los niveles de aislamiento
niveles_aislamiento = ["READ UNCOMMITTED", "READ COMMITTED", "REPEATABLE READ", "SERIALIZABLE"]
for nivel in niveles_aislamiento:
    probar_aislamiento(nivel)'''

'''# Ejemplo de detección y resolución de deadlocks
def transaccion_a():
    try:
        cur.execute("BEGIN;")
        cur.execute("LOCK TABLE Cuentas IN EXCLUSIVE MODE;")
        # Simular trabajo adicional
        time.sleep(5)
        cur.execute("COMMIT;")
        print("Transacción A completada exitosamente.")
    except Exception as e:
        cur.execute("ROLLBACK;")
        print(f"Transacción A fallida: {e}")

def transaccion_b():
    try:
        cur.execute("BEGIN;")
        cur.execute("LOCK TABLE Cuentas IN EXCLUSIVE MODE;")
        # Simular trabajo adicional
        time.sleep(5)
        cur.execute("COMMIT;")
        print("Transacción B completada exitosamente.")
    except Exception as e:
        cur.execute("ROLLBACK;")
        print(f"Transacción B fallida: {e}")

# Ejecutar transacciones A y B en paralelo para simular un deadlock
thread_a = threading.Thread(target = transaccion_a)
thread_b = threading.Thread(target = transaccion_b)
thread_a.start()
thread_b.start()
thread_a.join()
thread_b.join()'''

# Función para mostrar un menu y redireccionar a las operaciones
def menu():
    while True:
        print()
        print(" --------- Menu de Opciones ---------")
        print("1. Abrir una cuenta")
        print("2. Realizar Retiro")
        print("3. Realizar Deposito")
        print("4. Salir")
        print(" ------------------------------------")
        opcion = int(input("Inserte una opción: "))
        print(" ------------------------------------")
        if opcion == 1:
            saldo = int(input("Saldo inicial de la cuenta: "))
            abrir_cuenta(saldo)
        elif opcion == 2:
            id_cuenta = int(input("Ingrese el ID de su Cuenta: "))
            monto = int(input("Ingrese monto a retirar: "))
            retiro(id_cuenta, monto)
        elif opcion == 3:
            id_cuenta = int(input("Ingrese el ID de su Cuenta: "))
            monto = int(input("Ingrese monto a depositar: "))
            deposito(id_cuenta, monto)
        elif opcion == 4:
            break
        else:
            print("Opción no válida. Por favor, elija una opción del 1 al 4.")

menu()

'''pg_dump_path = r'"/opt/homebrew/Cellar/postgresql@16/16.3/bin/pg_dump"'

def backup_database():
    # comando para hacer una copia de seguridad de una BD
    backup_command = f'{pg_dump_path} -U postgres -F c -b -v -f "act4DiegoPacheco.backup" bd_transacciones'

    try:
        subprocess.run(backup_command, check = True, shell=True)
        print("Copia de seguridad realizada con exito")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar la copia de seguridad: {e}")

backup_database()'''

# Cerrar conexión
cur.close()
conn.close()
print("Conexión cerrada")