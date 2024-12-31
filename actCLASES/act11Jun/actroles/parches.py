import subprocess

def check_postgresql_version():
    result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
    print(f"Versión de PostgreSQL: {result.stdout.strip()}")

# Para checar la actualización en mac
def check_brew_updates():
    result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
    print("Actualizaciones disponibles medianete HomeBrew:")
    print(result.stdout.strip())
    
check_postgresql_version()
check_brew_updates()
