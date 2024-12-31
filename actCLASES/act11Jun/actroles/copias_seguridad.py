import subprocess
def backup_database():
    try:
        subprocess.run([
            "pg_dump", 
            "-U", "postgres",
            "-F", "c",
            "-b",
            "-v",
            "-f", "copia.backup",
            "integridad"
        ], check = True)
        print("Copia de Seguridad Realizada correctamente")
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar la copia de seguridad: {e}")

def restore_database():
    try:
        subprocess.run([
            "pg_restore",
            "-U", "postgres",
            "-d", "restauro",
            "-v", "copia.backup"
        ], check = True)
        print("Restauracion realizada con exito")
    except subprocess.CalledProcessError as e:
        print(f"Error al realizar la restauración: {e}")

backup_database()
restore_database()