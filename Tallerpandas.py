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