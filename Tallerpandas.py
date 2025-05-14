import pandas as pd
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
#2.7
df['imc'] = df['Peso'] / (df['Talla'] / 100) ** 2
print(df[['Peso', 'Talla', 'imc']].head(10))
def calcular_imc(fila):
    if fila['Talla'] > 0:
        return fila['Peso'] / (fila['Talla'] / 100) ** 2
    else:
        return "Nan" 
df['imc'] = df.apply(calcular_imc, axis=1)
print(df[['Peso', 'Talla', 'imc']].head(10))

#2.8

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

#2.9

df['Sedentario'] = df['Actividad física (min/sem)'] < 60
print(df[['Actividad física (min/sem)', 'Sedentario']].head(10))