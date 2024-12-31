import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración a la conexión

engine = create_engine('postgresql://postgres:1234@localhost:5432/olap_example')

# Función para realizar consultas y mostrar resultados

def ejecutar_consulta(query):
    with engine.connect() as connection:
        result = pd.read_sql(query, connection)
    return result

# Consultas OLAP

# Slice : Analizar las ventas del producto A en todas las regiones

query_slice = """
    SELECT fecha, region, ventas
    FROM ventas
    WHERE producto = 'Producto A';
"""

resultado_slice = ejecutar_consulta(query_slice)
print("Slice - ventas del producto A:")
print(resultado_slice)

# Dice: Crear un subcubo con ventas de los productos A y B en las regiones Norte y SUr

query_dice = """
    SELECT fecha, region, producto, ventas
    FROM ventas
    WHERE producto IN ('Producto A', 'Producto B') AND region IN ('Norte', 'Sur');
"""

resultado_dice = ejecutar_consulta(query_dice)
print("\nDice - Ventas de Productos A y B en las regiones Norte y Sur:")
print(resultado_dice)

# Drill-Down: Detallar las ventas mensuales a nivel diario
query_drill_down = """
    SELECT fecha, SUM(ventas) as total_ventas
    FROM ventas
    GROUP BY fecha;
"""

resultado_drill_down = ejecutar_consulta(query_drill_down)
print("\nDrill Down - Ventas Diarias:")
print(resultado_drill_down)
# Roll up: Agrupar las ventas diarias a nivel

query_roll_up = """
    SELECT DATE_TRUNC('month', fecha) as mes, SUM(ventas) as total_ventas
    FROM ventas
    GROUP BY mes;
"""

resultado_roll_up = ejecutar_consulta(query_roll_up)
print("\nRoll up - Ventas Mensuales:")
print(resultado_roll_up)

# Pivot: Rotar los datos para ver las ventas de cada producto por region
query_pivot = """
    SELECT region,
        SUM(CASE WHEN producto = 'Producto A' THEN VENTAS ELSE 0 END) as ventas_producto_a,
        SUM(CASE WHEN producto = 'Producto B' THEN VENTAS ELSE 0 END) as ventas_producto_b,
        SUM(CASE WHEN producto = 'Producto C' THEN VENTAS ELSE 0 END) as ventas_producto_c,
        SUM(CASE WHEN producto = 'Producto D' THEN VENTAS ELSE 0 END) as ventas_producto_d
    FROM ventas
    GROUP BY region;
"""

resultado_pivot = ejecutar_consulta(query_pivot)
print("\nPivot - Ventas por Producto y Región:")
print(resultado_pivot)

# Visualización de los resultados

# Grafico de Barras - Ventas por Region (Pivot):
resultado_pivot.set_index('region').plot(kind='bar', stacked = 'True')
plt.title("Ventas por Producto y Region:")
plt.xlabel("Region")
plt.ylabel('Ventas')
plt.legend(title="Producto")
plt.show()


# Grafico de Lineas - Ventas Mensuales (Roll Up)
resultado_roll_up.set_index("mes").plot(kind='line', marker='o')
plt.xlabel