# Actividad 5 asignada el lunes 17 de Junio del 2024
# Diego Pacheco Valdez
import psycopg2

conn = psycopg2.connect(
        dbname = "mcn",
        user = "postgres",
        password = "1234",
        host = "localhost"
)

cur = conn.cursor()

# Crear las tablas
cur.execute("""
    CREATE TABLE categorias(
        id_categoria SERIAL PRIMARY KEY,
        categoria VARCHAR(100)
    );
        
    CREATE TABLE productos(
        id_producto SERIAL PRIMARY KEY,
        nombre_producto VARCHAR(100),
        id_categoria INT REFERENCES categorias(id_categoria)
    );
            
    CREATE TABLE regiones(
        id_region SERIAL PRIMARY KEY,
        region VARCHAR(100)
    );
            
    CREATE TABLE clientes(
        id_cliente SERIAL PRIMARY KEY,
        nombre_cliente VARCHAR(100),
        id_region INT REFERENCES regiones(id_region)
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
    INSERT INTO categorias (categoria) VALUES
    ('Categoria 1'),
    ('Categoria 2');
    
    INSERT INTO productos (nombre_producto, id_categoria) VALUES
    ('Producto A', 1),
    ('Producto B', 1),
    ('Producto C', 2);
            
    INSERT INTO regiones (region) VALUES
    ('Region 1'),
    ('Region 2');
            
    INSERT INTO clientes (nombre_cliente, id_region) VALUES
    ('Cliente 1', 1),
    ('Cliente 2', 2),
    ('Cliente 3', 1);
            
    INSERT INTO tiempo (fecha, dia, mes, agno) VALUES
    ('2023-06-01', '1', '6', '2023'),
    ('2023-06-02', '2', '6', '2023'),
    ('2023-06-03', '3', '6', '2023'),
    ('2023-06-04', '4', '6', '2023');
            
    INSERT INTO ventas (fecha, id_producto, id_cliente, cantidad, total) VALUES
    ('2023-06-01', 1, 1, 10, 100.00),
    ('2023-06-02', 2, 2, 20, 250.00),
    ('2023-06-03', 1, 3, 15, 150.00),
    ('2023-06-04', 3, 2, 10, 125.00);
""")

conn.commit()

# Consultar datos
cur.execute("SELECT * FROM ventas;")
print(cur.fetchall())

cur.close()
conn.close()
