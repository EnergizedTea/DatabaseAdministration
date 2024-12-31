# Actividad del lunes 24 de Junio sobre bases NoSQL

from pymongo import MongoClient

# funcion para mostrar el menu
def mostrar_menu():
    print("--------Menu de Gestion de Libros-------")
    print("1. Insertar un libro")
    print("2. Consultar un libro por autor")
    print("3. Consultas avanzadas")
    print("4. Actualizar un libro")
    print("5. Eliminar un libro")
    print("6. Salir")
    print("----------------------------------------")

def agregar_libro(db):
    coleccion = db.libros

    libro = {
        "titulo": input("Ingrese el titulo del libro:   "),
        "autor": input("Ingrese el autor del libro:     "),
        "agno_publicacion": int(input("Ingrese el año de la publicacón:     ")),
        "genero": input("Ingrese el genero del libro:   ")
    }

    # Insertar el documento a la colección
    coleccion.insert_one(libro)
    print("libro Agregado!")

def consultar_libros_autor(db):
    coleccion = db.libros
    autor =  input("Ingresar el nombre del autor:     ")
    libros = coleccion.find({"autor": autor})

    for libro in libros:
        print(libro)

def actualizar_libro(db):
    coleccion = db.libros
    titulo = input("Ingrese el titulo del libro:    ")
    filtro = {"Titulo": titulo}

    nuevos_valores = {"$set": {
            "agno_publicacion": int(input("Ingrese el nuevo año de publicación:     ")),
            "genero": input("Ingrese el nuevo genero del libro:     ")
    }}
    coleccion.update_one(filtro, nuevos_valores)
    print("Libro actualizado!!")

def eliminar_libro(db):
    coleccion = db.libros
    titulo = input("Ingrese el titulo del libro a eliminar:    ")
    filtro = {"Titulo":titulo}
    coleccion.delete_one(filtro)
    print("Libro eliminado!")

def consulta_avanzada(db):
    coleccion = db.libros

    pipeline = [
        {"$group":{"_id": "$genero", "total_libros": {"$sum": 1}}}
    ]

    libros = coleccion.aggregate(pipeline)
    for libro in libros:
        print(libro)

def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.biblioteca

    while True:
        mostrar_menu()
        opcion = int(input("Seleccione una opcion:  "))

        if opcion == 1:
            agregar_libro(db)

        elif opcion == 2:
            consultar_libros_autor(db)

        elif opcion == 3:
            consulta_avanzada(db)

        elif opcion == 6:
            print("Saliendo...")
            break

        else:
            print("Opcion no valida")
    
    client.close()

if __name__ == "__main__":
    main()