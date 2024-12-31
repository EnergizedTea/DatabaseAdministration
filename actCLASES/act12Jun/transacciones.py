import psycopg2
import time 
import threading

# Conectar a postgres
conn = psycopg2.connect(
    dbname = "postgres",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

conn.autocommit= True
cur = conn.cursor()

# Crear Base de Datos
cur.execute("DROP DATABASE IF EXISTS transacciones_db")
cur.execute("CREATE DATABASE transacciones_db")
print("Base de Datos 'transacciones_db' creada exitosamente")

cur.close()
conn.close()

# Conectar a la nueva BD
conn = psycopg2.connect(
    dbname = "transacciones_db",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

cur = conn.cursor()

# Crear tabla y cuentas
cur.execute("""
CREATE TABLE IF NOT EXISTS cuentas (
            id SERIAL PRIMARY KEY,
            saldo DECIMAL NOT NULL
);
""")

conn.commit()

cur.execute("INSERT INTO cuentas (saldo) VALUES (1000), (2000);")
conn.commit()
print("Tabla 'cuentas' creada e inicializada con datos de ejemplo")

def realizar_transaccion(id_cuenta, monto):
    max_intentos = 3
    intento = 0

    while intento < max_intentos:
        try:
            intento += 1
            cur.execute("BEGIN;")
            # Obtener saldo actual y bloquear la fila para evitar operaciones concurrentes
            cur.execute("SELECT saldo FROM cuentas WHERE ID = %s FOR UPDATE;", (id_cuenta,))
            saldo_actual = cur.fetchone()[0]
            nuevo_saldo = saldo_actual - monto
            if nuevo_saldo < 0:
                raise Exception("Saldo insuficiente.")
            # Si hay suficiente actualizo saldo de la cuenta
            cur.execute("UPDATE cuentas SET saldo = %s WHERE id = %s;", (nuevo_saldo, id_cuenta))
            cur.execute("COMMIT;")
            print(f"Transaccion completada. Tu Nuevo Saldo es: {nuevo_saldo}")
            break
        except Exception as e:
            cur.execute("ROLLBACK;")
            print(f"Error en la transaccion: {e}")
            if intento == max_intentos:
                print(f"Transacción fallida despues de {max_intentos} intentos")
cur.close()
conn.close()

