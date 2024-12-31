import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
import wordcloud

# Cargar los datos
df = pd.read_csv("starbucks_ny_broadway.csv")

# Análisis de exploración
print(df.head())
print(df.info())

# Manejar posibles errores de análisis de fecha
try:
    df["publishedDate"] = pd.to_datetime(df["publishedDate"], format = "%Y-%m-%d")
except pd.errors.ParserError:
    print("Advertencia: No se pudieron analizar algunas fechas.")

# Estadísticas descriptivas para la calificación
estadisticas_calificacion = df["rating"].describe()
print(estadisticas_calificacion)

frecuencia_calificaciones, bins, patches = plt.hist(df["rating"], bins = 5, edgecolor = "black")
plt.xlabel("Calificación")
plt.ylabel("Frecuencia")
plt.title("Distribución de calificaciones")
plt.show()

# Tendencia de Calificaciones a lo largo del tiempo
df["publishedDate_month"] = df["publishedDate"].dt.month
tendencia_calificacion = df.groupby("publishedDate_month")["rating"].mean()
plt.plot(tendencia_calificacion.index, tendencia_calificacion.values)
plt.xlabel("Mes")
plt.ylabel("Calificacion promedio")
plt.title("Tendencia promedio de calificaciones a lo largo del tiempo")

# Calificacion por titulo de la reseña
calificacion_por_titulo = df.groupby("title")["rating"].mean()
calificacion_por_titulo.sort_values(ascending=False).plot(kind="bar")
plt.xlabel("Titulo de la reseña")
plt.ylabel("Calificacion promedio")
plt.title("Calificacion promedio por titulo de la reseña")
plt.xticks(rotation=90, ha="right")
plt.tight_layout()
plt.savefig("fig1.png", bbox_inches="tight")
plt.show()

# Distribucion del sentimiento (grafico pastel)

totales_sentimiento = {"positivo":0, "neutral":0, "negativo":0}
for text in df["text"]:
    try:
        analisis = TextBlob(text)
        polaridad = analisis.sentiment.polarity
        if polaridad > 0:
            totales_sentimiento["positivo"] += 1
        elif polaridad == 0:
            totales_sentimiento["neutral"] += 1
        else:
            totales_sentimiento["negativo"] += 1
    except:
        print("Error al procesar el texto")

etiquetas_sentimiento = totales_sentimiento.keys()
valores_sentimiento = totales_sentimiento.values()
plt.pie(valores_sentimiento, labels=etiquetas_sentimiento, autopct="%1.1f%%")
plt.title("Distribucion del Sentimiento en las Reseñas")
plt.show()

# Nube de palabras para palabras comunes
nube_palabras = wordcloud.WordCloud(background_color="white").generate(" ".join(df["text"]))

plt.imshow(nube_palabras, interpolation="bilinear")
plt.axis("off")
plt.title("Palabras comunes en las reseñas")
plt.show()