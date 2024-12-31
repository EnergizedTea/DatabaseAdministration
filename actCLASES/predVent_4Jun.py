# Esta actividad fue realizada 4 de Junio durante clase
import pandas as pd
from sklearn.linear_model import LinearRegression
import sqlalchemy as sa
import psycopg2

def insertar_nuevo_producto(producto, precio, publicidad, ventas):
    conn = psycopg2.connect(
        dbname = "predVen",
        user = "postgres",
        password = "1234",
        host = "localhost"
    )

    cursor = conn.cursor()

    # Consulta insertar dato
    sql_insert = """
    INSERT INTO SALES (producto, precio, publicidad, ventas) VALUES(%s, %s, %s, %s)
    """
    
    cursor.execute(sql_insert, (producto, precio, publicidad, ventas))

    conn.commit()

    cursor.close()
    conn.close()

'''insertar_nuevo_producto("Coca Cola", 18, 100, 1000)
insertar_nuevo_producto("Pepsi", 14, 80, 5)
insertar_nuevo_producto("Audifonos Beats",3000, 100, 80)'''

engine = sa.create_engine(
    "postgresql://postgres:1234@localhost:5432/predVen"
)

# lectura de datos de la tabla "Sales" en un Dataframe de pandas.
df = pd.read_sql_table("sales", engine)

# Seleccion de las columnas "precio" y "publicidad" como caracteristicas
X = df[["precio", "publicidad"]]

# Seleccion de la columna "ventas" como variable objetivo
# la dependiente son las ventas
y = df["ventas"]

# Creación y Entrenamiento del Modelo de regresión linbeal

model = LinearRegression() #instancia de la clase linearRegression
model.fit(X, y)

# Realizar predicción
nuevo_precio = 20
nueva_publicidad = 100 # presupuesto de publicidad del nuevo producto

prediction = model.predict([[nuevo_precio, nueva_publicidad]])

# Impresión de la Predicción de venta para el nuevo producto
print("Ventas predichas para el nuevo producto:     ", prediction)