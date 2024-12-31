import psycopg2

conn = psycopg2.connect(
    database = "prueba",
    user = "postgres",
    password = "1234"
    port = "5432"
)