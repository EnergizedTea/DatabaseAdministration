from pymongo import MongoClient

client = MongoClient("mongodb+srv://mongo1:mongo@pruebapostgres.1bdtrwm.mongodb.net/?retryWrites=true&w=majority&appName=PruebaPostgres")

db = client.pruebas

coleccion = db.peliculas

documento = {
    "titulo" : "El Menu",
    "agno" : "2022",
    "genero" : "Suspenso",
    "sala" : "B4"
}

coleccion.insert_one(documento)

'''filtro = {"titulo": "La Dama y El Vagabundo"}
nuevo_valor = {"$set": {"agno":1989}}
coleccion.update_one(filtro,nuevo_valor)'''

client.close()