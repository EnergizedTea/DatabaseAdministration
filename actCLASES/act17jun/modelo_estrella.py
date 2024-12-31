#Actividad del lunes 17 de Junio del 2024
import psycopg2

conn = psycopg2.connect(
        dbname = "me",
        user = "postgres",
        password = "1234",
        host = "localhost"
)

cur = conn.cursor()

# Crear las tablas
cur.execute("""
    CREATE TABLE productos(
        id_producto SERIAL PRIMARY KEY,
        nombre_producto VARCHAR(100),
        categoria VARCHAR(100)
    );
            
    CREATE TABLE clientes(
        id_cliente SERIAL PRIMARY KEY,
        nombre_cliente VARCHAR(100),
        region VARCHAR(100)
    );
    
    CREATE TABLE tiempo(
        id_tiempo SERIAL PRIMARY KEY,
        fecha DATE UNIQUE,
        dia INT,
        mes INT,
        agno INT
    );
            
    CREATE TABLE ventas (
        id_venta SERIAL PRIMARY KEY,
        fecha DATE REFERENCES tiempo(fecha),
        id_producto INT REFERENCES productos(id_producto), 
        id_cliente INT REFERENCES clientes(id_cliente),
        cantidad INT,
        total DECIMAL
    )
""")

conn.commit()

# Insertar datos

cur.execute("""
    INSERT INTO productos (nombre_producto, categoria) VALUES
    ('Producto A', 'Categoria 1'),
    ('Producto B', 'Categoria 2');
            
    INSERT INTO clientes (nombre_cliente, region) VALUES
    ('Cliente 1', 'Region 1'),
    ('Cliente 2', 'Region 2');
            
    INSERT INTO tiempo (fecha, dia, mes, agno) VALUES
    ('2023-06-01', '1', '6', '2023'),
    ('2023-06-02', '2', '6', '2023');
            
    INSERT INTO ventas (fecha, id_producto, id_cliente, cantidad, total) VALUES
    ('2023-06-01', 1, 1, 10, 100.00),
    ('2023-06-02', 2, 2, 20, 250.00);
""")

conn.commit()

# Consultar datos
cur.execute("SELECT * FROM ventas;")
print(cur.fetchall())

cur.close()
conn.close()
