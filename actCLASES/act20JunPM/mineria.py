import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import KMeans
from mlxtend.frequent_patterns import apriori, association_rules
import matplotlib.pyplot as plt

# Cargar los datos
df = pd.read_csv("The_Cancer_data_1500_V2.csv")

# Exploración y Análiis descriptivo
print(df.head())
print(df.describe())
print(df.info())

df.fillna(df.mean(), inplace = True) # Rellena colores faltantes con la media de los datos

label_encoder = LabelEncoder()
df['Gender'] = label_encoder.fit_transform(df['Gender'])

# Estandarizar las caracteristicas numericas
numerical_features = ["Age", "BMI", "Smoking", "GeneticRisk", "PhysicalActivity", "AlcoholIntake"]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[numerical_features])
df_prepocessed = pd.DataFrame(data = scaled_features, columns = numerical_features)
df_prepocessed = df.drop(numerical_features, axis=1).join(df_prepocessed) # Reemplazar caracteristicas originales con las estandarizadas

# Definir la variable objetivo
target_variable = 'Diagnosis'

# Dividir los datos
X = df_prepocessed.drop(target_variable, axis=1)
y = df_prepocessed[target_variable]
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

# Entrenar y Evaluar modelos de aprendizaje automatico
modelo_lr = LogisticRegression()
modelo_lr.fit(X_train, y_train)
y_pred_lr = modelo_lr.predict(X_test)
print("Regresion Logistica")
print("Exactitud (Accuracy) (le da al tablero): ", accuracy_score(y_test, y_pred_lr))
print("Precision (Precision) (le da donde quieres): ", precision_score(y_test, y_pred_lr))
print("Sensibilidad (Recall) (que tanto puedes cambiar los valores sin cambiar el resultado): ", recall_score(y_test, y_pred_lr))

# Arbol de decisiones
model_dt = DecisionTreeClassifier()
model_dt.fit(X_train, y_train)
y_pred_dt = model_dt.predict(X_test)
print("Clasificador de Arbol de Decision")
print("Exactitud:", accuracy_score(y_test, y_pred_dt))
print("Precision:", precision_score(y_test, y_pred_dt))
print("Sensibiliad (Recall):", recall_score(y_test, y_pred_dt))

# KNEIGHBOURS
model_knn = KNeighborsClassifier()
model_knn.fit(X_train, y_train)
y_pred_knn = model_knn.predict(X_test)
print("Clasificador K vecinos cercanos de Decision")
print("Exactitud:", accuracy_score(y_test, y_pred_knn))
print("Precision:", precision_score(y_test, y_pred_knn))
print("Sensibiliad (Recall):", recall_score(y_test, y_pred_knn))