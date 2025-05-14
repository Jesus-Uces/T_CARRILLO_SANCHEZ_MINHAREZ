import pandas as pd
df_pacientes_1 =pd.read_csv("pacientes_1.csv")
df_pacientes_2 =pd.read_csv("pacientes_2.csv")
print("archivos CSV cargados correctamente")


df_pacientes_1_nuevo =df_pacientes_1.rename(columns={"altura_m":"altura","peso_kg":"peso"})
df_pacientes_2_nuevo =df_pacientes_2.rename(columns={"nombre_completo":"nombre","estatura":"altura","peso corporal":"peso"})
print(df_pacientes_1_nuevo)
print( "pacientes_1 renombrados")

df_pacientes_1_no_dupli=df_pacientes_1_nuevo.drop_duplicates(subset=["nombre","peso","altura"])
df_pacientes_2_no_dupli=df_pacientes_2_nuevo.drop_duplicates(subset=["nombre","peso","altura"])
print(df_pacientes_1_no_dupli)
print ("listo sin duplicacion")

df_pacientes_1_0=df_pacientes_1_no_dupli.fillna(0)
df_pacientes_2_0=df_pacientes_2_no_dupli.fillna(0)
print(df_pacientes_1_0)
print("reemplazado")

df_pacientes=pd.concat([df_pacientes_1_0,df_pacientes_2_0],ignore_index=True)
print(df_pacientes)
print("se unifico")

def clasifico_imc(fila):
   if fila["altura"] > 0:
        return fila["peso"] / (fila["altura"] ** 2)
   else:
        return 
df_pacientes["imc"] = df_pacientes.apply(clasifico_imc, axis=1)
print(df_pacientes)

def clasificar_imc(imc):
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 24.9:
        return "Normal"
    elif imc < 29.9:
        return "Sobrepeso"
    else:
        return "Obesidad"
df_pacientes["clasificacion"] = df_pacientes["imc"].apply(clasificar_imc)
print(df_pacientes)

df_pacientes_ordenado = df_pacientes.sort_values(by='nombre')
print(df_pacientes_ordenado)
print("orden alfabeticamente")

df_pacientes_filtrado = df_pacientes_ordenado[df_pacientes_ordenado["imc"] > 25]
print(df_pacientes_filtrado)
df_pacientes_filtrado.to_csv("pacientes_sobrepeso.csv", index=False)
print("Archivo 'pacientes_sobrepeso.csv' guardado correctamente.")

df_pacientes_ordenado.to_csv("pacientes_final.csv", index=False)
print("Archivo 'pacientes_final.csv' guardado correctamente.")

def nota_personalizada(fila):
    imc = fila["imc"]
    if imc < 18.5:
        return "Cuida tu alimentación, estás bajo peso."
    elif 18.5 <= imc < 25:
        return "¡Muy bien! Tienes un IMC normal."
    elif 25 <= imc < 30:
        return "Atento, podrías mejorar tu dieta."
    else:
        return "Cuidado, hay riesgo por obesidad."
df_pacientes["nota"] = df_pacientes.apply(nota_personalizada, axis=1)
print(df_pacientes[["nombre", "imc", "clasificacion", "nota"]].head(10))