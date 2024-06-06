# Actividad realizada el 5 de Junio del 2024

import psycopg2
import subprocess

# Rutas para pg_dump y pg_restore
pg_dump_path = r'"/opt/homebrew/Cellar/postgresql@16/16.3/bin/pg_dump"'
pg_restore_path = r'"/opt/homebrew/Cellar/postgresql@16/16.3/bin/pg_restore"'

conn = psycopg2.connect(
    dbname = "escuela",
    user = "postgres",
    password = "1234",
    host = "localhost"
)

cur = conn.cursor()

def backup_database():
    # comando para hacer una cpia de seguridad de una BD
    # forma posible
    # backup_command = f'{pg_dump_path} -h localhost -U postgres -F c -b -v -f "respaldo.backup" escuela'
    backup_command = f'{pg_dump_path} -U postgres -F c -b -v -f "respaldo.backup" escuela'

    try:
        subprocess.run(backup_command, check = True, shell=True)
        print("Copia de seguridad realizada con exito")
    
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar la copia de seguridad: {e}")

def restore_database():
    # Comando para restaurar una copia de seguridad
    restore_command = f'{pg_restore_path} -U postgres -d 05test -v "respaldo.backup"'
    try:
        subprocess.run(restore_command, check=True, shell=True)
        print("Restauracion realizada con exito")
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar la restauracion: {e}")


backup_database()
restore_database()


cur.close()
conn.close()