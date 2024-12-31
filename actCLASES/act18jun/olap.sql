-- Conectar a PostgreSQL y crear la base de datos
CREATE DATABASE olap_example;

-- Conectar a la base de datos olap_example y crear la tabla de ventas
\c olap_example;

CREATE TABLE ventas (
    id SERIAL PRIMARY KEY,
    fecha DATE,
    region VARCHAR(50),
    producto VARCHAR(50),
    ventas INT
);

-- Insertar datos de ejemplo en la tabla
INSERT INTO ventas (fecha, region, producto, ventas) VALUES
('2024-01-01', 'Norte', 'Producto A', 100),
('2024-01-01', 'Sur', 'Producto B', 150),
('2024-01-02', 'Este', 'Producto A', 200),
('2024-01-02', 'Oeste', 'Producto C', 120),
('2024-01-03', 'Norte', 'Producto D', 410),
('2024-01-04', 'Sur', 'Producto C', 150),
('2024-01-05', 'Este', 'Producto B', 350),
('2024-01-06', 'Oeste', 'Producto A', 100),
('2024-01-07', 'Noreste', 'Producto B', 340),
('2024-01-07', 'Oeste', 'Producto D', 100),
('2024-01-07', 'Norte', 'Producto C', 220);