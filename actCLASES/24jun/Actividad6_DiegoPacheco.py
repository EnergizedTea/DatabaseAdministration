# Actiidad 6
# Desarrollar una pequeña aplicación en Python que interactúe con MongoDB para gestionar una base de datos de películas.
from pymongo import MongoClient

def mostrar_menu():
    print("-----------------------------------------------")
    print("-------- Menu de Gestion de Peliculas ---------")
    print("-----------------------------------------------")
    print("----------- 1. Agregar una película -----------")
    print("-----------------------------------------------")
    print("----- 2. Consultar películas por director -----")
    print("-----------------------------------------------")
    print("---------- 3. Consultas avanzadas -------------")
    print("-----------------------------------------------")
    print("-- 4. Actualizar Información de una Película --")
    print("-----------------------------------------------")
    print("---------- 5. Eliminar una Película -----------")
    print("-----------------------------------------------")
    print("------------ 6. Salir del Programa ------------")
    print("-----------------------------------------------")

def mostar_submenu():
    print("-----------------------------------------------")
    print("------- SubMenu de Consultas Avanzadas --------")
    print("-----------------------------------------------")
    print("------- 1. Agrupar Películas por Género -------")
    print("-----------------------------------------------")
    print("----- 2. cantidad de películas por género -----")
    print("-----------------------------------------------")
    print("------------ 3. Salir del Submenu -------------")
    print("-----------------------------------------------")

def agregar_pelicula(db):
    coleccion = db.peliculas

    print("-----------------------------------------------")
    pelicula = {
        "titulo": input("Ingrese el titulo de la película:   "),
        "director": input("Ingrese el director de la película:     "),
        "agno_estreno": int(input("Ingrese el año del estreno:     ")),
        "genero": input("Ingrese el genero de la película:   ")
    }
    print("-----------------------------------------------")

    # Insertar el documento a la colección
    coleccion.insert_one(pelicula)
    print("Pelicula Agregado!")

def consultar_pelicula_director(db):
    coleccion = db.peliculas
    director =  input("Ingresar el nombre del director:     ")
    peliculas = coleccion.find({"director": director})

    for pelicula in peliculas:
        print(pelicula)

def actualizar_pelicula(db):
    coleccion = db.peliculas
    titulo = input("Ingrese el titulo de la pelicula:    ")
    filtro = {"titulo": titulo}

    upIt = input("Introduzca el Nuevo Titulo de la Pelicula (o deje en blanco para no cambiar):     ")
    upIt = upIt if upIt != '' else None

    upDir = input("Introduzca el Nuevo Director de la Pelicula (o deje en blanco para no cambiar):      ")
    upDir = upDir if upDir != '' else None

    upAgn = input("Introduzca la Nueva Fecha de Estreno de la Pelicula (o deje en blanco para no cambiar):      ")
    upAgn = int(upAgn) if upAgn != '' else None

    upGen = input("Introduzca el Nuevo Genero de la Pelicula (o deje en blanco para no cambiar):        ")
    upGen = upGen if upGen != '' else None

    dictionary = {'titulo': upIt, 'director': upDir, 'agno_estreno': upAgn, 'genero': upGen}

    
    for key in dictionary:
        if dictionary[key] is not None:
            nuevo_valor = {"$set": {f"{key}": dictionary[key]}}
            coleccion.update_one(filtro, nuevo_valor)
    print("Pelicula actualizado!!")

def eliminar_pelicula(db):
    coleccion = db.peliculas
    titulo = input("Ingrese el titulo de la pelicula a eliminar:    ")
    filtro = {"titulo":titulo}
    coleccion.delete_one(filtro)
    print("Pelicula eliminado!")

def agrupar_pelicula_genero(db):
    coleccion = db.peliculas

    pipeline = [
        {"$group":{"_id": "$genero", "total_peliculas": {"$sum": 1}}}
    ]

    peliculas = coleccion.aggregate(pipeline)
    for pelicula in peliculas:
        print(pelicula)

# Función para contar la cantidad de peliculas con el mismo genero
def contar_peliculas_genero(db):
    coleccion = db.peliculas
    genero = input("Ingresar el genero de la pelicula:      ")

    pipeline = [
        { "$match": { "genero" : genero } },
        {"$group":{"_id": "$genero", "total_peliculas": {"$sum": 1}}}
    ]
    peliculas = coleccion.aggregate(pipeline)
    for pelicula in peliculas:
        print(pelicula)


def main():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.cine
    
    while True:
        mostrar_menu()
        opcion = int(input("Seleccione una opcion:  "))
        
        if opcion ==  1:
            agregar_pelicula(db)

        elif opcion == 2:
            consultar_pelicula_director(db)

        elif opcion == 3:
            while True:
                mostar_submenu()
                opcion = int(input("Seleccione una opcion:  "))

                if opcion == 1:
                    agrupar_pelicula_genero(db)
                elif opcion == 2:
                    contar_peliculas_genero(db)
                elif opcion == 3:
                    print("Regresando a menu principal")
                    break
                else:
                    print("Opcion no valida")
                                        
        elif opcion == 4:
            actualizar_pelicula(db)

        elif opcion == 5:
            eliminar_pelicula(db)

        elif opcion == 6:
                print("Saliendo...")
                break

        else:
            print("Opcion no valida")
    
    client.close()

if __name__ == "__main__":
    main()
    
