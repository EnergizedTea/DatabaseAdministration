import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Cargar los datos
df = pd.read_csv("The_Cancer_data_1500_V2.csv")

# Exploracion de datos
print(df.head())
print(df.info())

#Estadisiticas descriptivas para verificar la calidad de los
print(df.describe())

### Analisis 1: Distribuión de Diagnosticos

# Distribucion del diagnostido de cancer
diagnostico_counts = df['Diagnosis'].value_counts()

plt.figure(figsize=(6,4))
diagnostico_counts.plot(kind='bar', color=['skyblue', 'salmon'])
plt.xlabel("Diagnostico")
plt.ylabel("Frecuencia")
plt.title("Distribucion del Diagnostico de Cancer")
plt.xticks(ticks=[0,1], labels=["No Cancer", "Cancer"], rotation=0)
plt.show()

## Analisis 2: Distribucion de Edad por Diagnostico

plt.figure(figsize=(10,6))
sns.histplot(data=df, x='Age', hue='Diagnosis', multiple='stack', bins=15, palette=['skyblue', 'salmon'])
plt.xlabel("Edad")
plt.ylabel("Frecuencia")
plt.title("Distribución de la Edad por Diaganostico")
plt.show()

### Analisis 3: Distribucion de BMI vs Diagnostico
plt.figure(figsize=(10,6))
sns.boxplot(data=df, x='Diagnosis', y = 'BMI', palette=['skyblue', 'salmon'])
plt.xlabel("Diagnostico")
plt.ylabel("Indice de Masa Corporal (BMI)")
plt.title("Distribucion de BMI por Diagnostico")
plt.xticks(ticks=[0,1], labels=["No Cancer", "Cancer"])
plt.show()

# Analisis 4: Correlacion entra las variables
# Mapa de calor

plt.figure(figsize=(10,8))
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Mapa de Calor de la Correlacion entre Variables")
plt.show()

# Analisis 5: Distribución de la actividad fisica por diagnostico

plt.figure(figsize=(10, 6))
sns.histplot(data=df, x="PhysicalActivity", hue="Diagnosis", multiple="stack", bins=10, palette=['skyblue', 'salmon'])
plt.xlabel("Horas de Actividad Fisica por Semana")
plt.ylabel("Frecuencia")
plt.title("Distribucion de la Actividad Fisica por Diagnostico")
plt.show()

# Analisis 6: Distribucion del consumo de Alcohol
plt.figure(figsize=(10,6))
sns.histplot(data=df, x="AlcoholIntake", hue="Diagnosis", multiple="stack", bins=5, palette=['skyblue', 'salmon'])
plt.xlabel("Consumo de Alcohol por Semana (Unidades)")
plt.ylabel("Frecuencia")
plt.title("Distribucion del consumo de Alcohol por Diagnostico")
plt.show()

# Analisis 7: Riesgo Genetico por Diagnostico

plt.figure(figsize=(8,6))
sns.countplot(data=df, x="GeneticRisk", hue="Diagnosis", palette=['skyblue', 'salmon'])
plt.xlabel("Riesgo Genetico")
plt.ylabel("Frecuencia")
plt.title("Distribución del Riesgo Genetico por Diagnostico")
plt.xticks(ticks=[0,1,2], labels=['bajo','medio','alto'])
plt.show()

# Analisis 8: Distribucion de Generos por diagnosticos

plt.figure(figsize=(8,6))
sns.countplot(data = df, x='Gender', hue='Diagnosis', palette=['skyblue', 'salmon'])
plt.xlabel("Genero")
plt.ylabel("Frecuencia")
plt.title("Distribución de Genero por Diagnostico")
plt.xticks(ticks=[0,1], labels=['Hombre', 'Mujer'])
plt.show()

# Analisis 9:  Historia de Cancer

plt.figure(figsize=(8, 6))
sns.countplot(data=df, x="CancerHistory", hue="Diagnosis", palette=["skyblue", "salmon"])
plt.xlabel("Historia de Cancer")
plt.ylabel("Frecuencia")
plt.title("Distribucion de historia de cancer por Diagnostico")
plt.xticks(ticks=[0,1], labels=['No', 'Si'])
plt.show()
