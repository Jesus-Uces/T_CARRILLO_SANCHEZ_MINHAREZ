import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
df = pd.read_csv("biometria_pacientes(in).csv", encoding='latin1', delimiter=";")
print(df.head(10))

duplicados = df.duplicated().sum()
print(f"Cantidad de filas duplicadas:{duplicados}")

nulos_por_columna = df.isnull().sum()
print("Valores nulos por columna:")
print(nulos_por_columna)

print("Opciones ingresadas en la columna 'Fuma':")
print(df["Fuma"].value_counts(dropna=False))

df_sin_dupli = df.drop_duplicates()
print(df_sin_dupli)
print("no hay duplicados")

df_sin_nulos = df.dropna(subset=["Peso", "Talla", "Glucosa", "Colesterol"])
print(df_sin_nulos)
print ("no hay nulos")

df['Fuma'] = df['Fuma'].str.lower().replace({
    'sí': True, 'si': True, '1': True, 'fuma': True, 'yes': True, 'y': True,
    'no': False, '0': False, 'desconocido': False, 'no fuma': False, 'na': False
})
df['Fuma'] = df['Fuma'].astype(bool)
print(df[['Fuma']].head(10))

df['Fecha de tamizaje'] = pd.to_datetime(df['Fecha de tamizaje'], dayfirst=True, errors='coerce')
df['Mes'] = df['Fecha de tamizaje'].dt.month
print(df[['Fecha de tamizaje', 'Mes']].head(10))

df['imc'] = df['Peso'] / (df['Talla'] / 100) ** 2
print(df[['Peso', 'Talla', 'imc']].head(10))
def calcular_imc(fila):
    if fila['Talla'] > 0:
        return fila['Peso'] / (fila['Talla'] / 100) ** 2
    else:
        return np.nan  
df['imc'] = df.apply(calcular_imc, axis=1)
print(df[['Peso', 'Talla', 'imc']].head(10))

def clasificar_imc(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 24.9:
        return "Normal"
    elif imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidad"
df["clasificacion"] = df["imc"].apply(clasificar_imc)
print(df)

df['Sedentario'] = df['Actividad física (min/sem)'] < 60
print(df[['Actividad física (min/sem)', 'Sedentario']].head(10))

df['Hipertenso'] = (df['PAS'] >= 140) | (df['PAD'] >= 90)
print(df[['PAS', 'PAD', 'Hipertenso']].head(10))

df['Metabolicamente alterado'] = (
    ((df['Glucosa'] > 126).astype(int) +
     (df['Colesterol'] > 240).astype(int) +
     (df['imc'] > 30).astype(int) +
     (df['Sedentario'] == True).astype(int)) >= 2
)
print(df[['Glucosa', 'Colesterol', 'imc', 'Sedentario', 'Metabolicamente alterado']].head(10))

df_region = df.groupby('Región')['Metabolicamente alterado'].agg('sum').reset_index()
region_max_riesgo = df_region.loc[df_region['Metabolicamente alterado'].idxmax()]
print(f"La región con mayor carga de riesgo metabólico es: {region_max_riesgo['Región']}")
df_mes = df.groupby('Mes')['Sedentario'].agg('sum').reset_index()
mes_max_sedentario = df_mes.loc[df_mes['Sedentario'].idxmax()]
print(f"El mes con más sedentarismo es: {mes_max_sedentario['Mes']}")

region_riesgo = df[df['Metabolicamente alterado'] == True].groupby('Región').size()
plt.figure(figsize=(10, 6))
region_riesgo.plot(kind='bar', color='red')
plt.title('Carga de riesgo metabólico por región')
plt.xlabel('Región')
plt.ylabel('Número de casos con riesgo metabólico')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

sedentarismo_mes = df[df['Sedentario'] == True].groupby('Mes').size()
plt.figure(figsize=(10, 6))
sedentarismo_mes.plot(kind='bar', color='salmon')
plt.title('Sedentarismo por mes')
plt.xlabel('Mes')
plt.ylabel('Número de personas sedentarias')
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()