
import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
from funciones import etiquetas


ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "clean"

CSV_FILE = CLEAN / "dataset_merged.csv"

df = pd.read_csv(CSV_FILE)

# 1. Cuantos planetas hay por sistema, frente a 8 en el Sistema Solar

orden = sorted(df["sy_pnum"].unique())

plt.figure(figsize=(10, 7))
sns.countplot(data=df,x="sy_pnum",order=orden,color="steelblue")

plt.title("1.Número de planetas conocidos por sistema")
plt.xlabel("Número de planetas")
plt.ylabel("Número de sistemas")
plt.tight_layout()
etiquetas(plt.gca(), df["sy_pnum"].notna().sum())
plt.show()

# 2. Sistemas con planetas pequenos en la zona interior 3. Ley de Kepler

validos_orbita = ((df["st_mass_y"] > 0) & (df["st_mass_y"] < 100) &(df["pl_orbper_y"] > 0))
df["a_ua"] = float("nan")
df.loc[validos_orbita, "a_ua"] = (df.loc[validos_orbita, "st_mass_y"]
* (df.loc[validos_orbita, "pl_orbper_y"] / 365.25) ** 2) ** (1 / 3)

df["pequeno_interior"] = ((df["pl_rade_y"] >= 0.5) &(df["pl_rade_y"] <= 1.6) &(df["a_ua"] < 1.5))

pla_peq_int = (df.groupby("hostname")["pequeno_interior"].any()
    .map({True: "Con planeta pequeno interior", False: "Sin candidato detectado"})
    .value_counts())

plt.figure(figsize=(10, 7))
sns.barplot( x=pla_peq_int.index ,y=pla_peq_int.values ,hue=pla_peq_int.index,palette=["green","gray"])

plt.title("2.Sistemas con planetas pequeños interiores")
plt.xlabel("")
plt.ylabel("Número de sistemas")
etiquetas(plt.gca(), pla_peq_int.sum())

plt.show()

# 3. Sistemas con y sin gigantes calientes

df["gigante_caliente"] = ((df["pl_rade_y"] >= 8) &(df["pl_orbper_y"] < 10))

gigantes_por_sistema = df.groupby("hostname").agg(
    gigante_caliente=("gigante_caliente", "any"))

sistemas_gigantes_calientes = (gigantes_por_sistema["gigante_caliente"].value_counts()
    .rename(index={True: "Con gigante caliente",False: "Sin gigante caliente detectado"}))

colores=["#E76F51", "#4C78A8"]

plt.figure(figsize=(10, 7))
sns.barplot( x=sistemas_gigantes_calientes.index ,y=sistemas_gigantes_calientes.values ,
            hue=sistemas_gigantes_calientes.index,palette=colores)

plt.title("3.Sistemas con gigantes calientes")
plt.xlabel("")
plt.ylabel("")
etiquetas(plt.gca(), sistemas_gigantes_calientes.sum())
plt.show()

# 4. Sistemas con gigantes exteriores tipo Jupiter/Saturno
df["gigante_exterior"] = ((df["pl_rade_y"] >= 8) &(df["a_ua"] >= 3))

sistemas_gigantes_exteriores = (df.groupby("hostname")["gigante_exterior"].any()
    .map({True: "Con gigante exterior", False: "Sin gigante exterior detectado"}).value_counts())

colores=["#E9C46A", "#B0B0B0"]

plt.figure(figsize=(10, 7))
sns.barplot( x=sistemas_gigantes_calientes.index ,y=sistemas_gigantes_calientes.values ,
            hue=sistemas_gigantes_calientes.index,palette=colores)

plt.title("4. Gigantes exteriores en los sistemas")
plt.xlabel("")
plt.ylabel("")
etiquetas(plt.gca(), sistemas_gigantes_exteriores.sum())
plt.show()


# 5. Sistemas con al menos un planeta en zona habitable estimada

temperatura_sol = 5772

validos_estrella = ((df["st_teff_y"] > 0) & (df["st_rad"] > 0))

df["luminosidad_relativa"] = float("nan")
df.loc[validos_estrella, "luminosidad_relativa"] = (df.loc[validos_estrella, "st_rad"] ** 2
* (df.loc[validos_estrella, "st_teff_y"] / temperatura_sol) ** 4)

df["zh_interior"] = 0.95 * df["luminosidad_relativa"] ** 0.5
df["zh_exterior"] = 1.67 * df["luminosidad_relativa"] ** 0.5

df["en_zh"] = ((df["a_ua"] >= df["zh_interior"]) &(df["a_ua"] <= df["zh_exterior"]))

sistemas_zh = (
    df.groupby("hostname")["en_zh"].any()
    .map({True: "Con planeta en zona habitable", False: "Sin planeta HZ detectado"}).value_counts())

colores=["#2A9D8F", "#B0B0B0"]

plt.figure(figsize=(10, 7))
sns.barplot( x=sistemas_zh .index ,y=sistemas_zh .values ,
            hue=sistemas_zh .index,palette=colores)

plt.title("5. Sistemas con planetas en zona habitable estimada")
plt.xlabel("")
plt.ylabel("")
etiquetas(plt.gca(), sistemas_zh.sum())
plt.show()

# 6. Frecuencia de estrellas parecidas al Sol

df["similar_al_sol"] = (df["st_teff_y"].between(5500, 6050) &df["st_rad"].between(0.85, 1.15) &df["st_mass_y"].between(0.85, 1.15))
conteo_solares = df["similar_al_sol"].map({True: "Similar al Sol", False: "No similar al Sol"}).value_counts()

colores=["#F6D55C", "#B0B0B0"]

plt.figure(figsize=(10, 7))
sns.barplot( x=conteo_solares.index ,y=conteo_solares.values ,
            hue=conteo_solares.index,palette=colores)

plt.title("6. Estrellas similares al Sol",)
plt.xlabel("")
etiquetas(plt.gca(), conteo_solares.sum())
plt.show()

# 7. Analogos terrestres alrededor de estrellas similares al Sol
# Criterio: estrella similar al Sol, planeta 0.8 - 1.25 R_tierra y en HZ.
df["estrella_similar_al_sol"] = (
    df["st_teff_y"].between(5500, 6050) &
    df["st_rad"].between(0.85, 1.15) &
    df["st_mass_y"].between(0.85, 1.15)
)
df["analogo_tierra"] = (
    df["estrella_similar_al_sol"] &
    df["pl_rade_y"].between(0.8, 1.25) &
    df["en_zh"]
)
sistemas_solares = df[df["estrella_similar_al_sol"]].groupby("hostname")
analogos_por_sistema = sistemas_solares["analogo_tierra"].any()
conteo_analogos = analogos_por_sistema.map(
    {True: "Con analogo terrestre", False: "Sin analogo terrestre detectado"}
).value_counts()

colores=["#2A9D8F", "#B0B0B0"]

plt.figure(figsize=(10, 7))
sns.barplot( x=conteo_analogos.index ,y=conteo_analogos.values ,
            hue=conteo_analogos.index,palette=colores)

plt.title("7. Analogos terrestres en estrellas similares al Sol")
plt.xlabel("")
plt.ylabel("")
etiquetas(plt.gca(), conteo_analogos.sum())
plt.show()

# 8. Arquitectura: pequenos interiores y gigantes exteriores
arquitectura = df.groupby("hostname").agg(
    pequenos_interiores=("pequeno_interior", "any"),
    gigantes_exteriores=("gigante_exterior", "any")
)
arquitectura["tipo"] = "Ninguno de los dos"
arquitectura.loc[arquitectura["pequenos_interiores"] & ~arquitectura["gigantes_exteriores"],"tipo"] = "Solo pequenos interiores"
arquitectura.loc[ ~arquitectura["pequenos_interiores"] & arquitectura["gigantes_exteriores"],"tipo"] = "Solo gigante exterior"
arquitectura.loc[arquitectura["pequenos_interiores"] & arquitectura["gigantes_exteriores"],"tipo"] = "Arquitectura tipo Solar"

conteo_arquitectura = arquitectura["tipo"].value_counts().reindex([
    "Ninguno de los dos",
    "Solo pequenos interiores",
    "Solo gigante exterior",
    "Arquitectura tipo Solar"
], fill_value=0)
colores=["#B0B0B0", "#4C78A8", "#E9C46A", "#2A9D8F"]

plt.figure(figsize=(10, 5))
sns.barplot( x=conteo_arquitectura.index ,y=conteo_arquitectura.values ,
            hue=conteo_arquitectura.index,palette=colores)

plt.title("8. Arquitectura planetaria por sistema")
plt.xlabel("Número de sistemas")
plt.ylabel("")
etiquetas(plt.gca(), conteo_arquitectura.sum())
plt.show()

# 9. Excentricidad de las orbitas

excentricidades = df["pl_orbeccen_y"].dropna()
excentricidades = excentricidades[(excentricidades >= 0) & (excentricidades < 1)]
rangos_excentricidad = pd.cut(excentricidades,bins=[-0.001, 0.05, 0.15, 0.30, 0.60, 1],
    labels=["Casi circular\n0 - 0.05","Baja\n0.05 - 0.15","Moderada\n0.15 - 0.30","Alta\n0.30 - 0.60","Muy alta\n0.60 - 1"],
    include_lowest=True)
conteo_excentricidad = rangos_excentricidad.value_counts().reindex(
    rangos_excentricidad.cat.categories, fill_value=0)

colores=["#2A9D8F", "#8AB17D", "#E9C46A", "#F4A261", "#E76F51"]

plt.figure(figsize=(10, 7))
sns.barplot(x=conteo_excentricidad .index , y=conteo_excentricidad.values,
            hue=conteo_excentricidad .index,palette=colores)

plt.title("9. Excentricidad de las orbitas de exoplanetas")
plt.xlabel("Rango de excentricidad orbital")
plt.ylabel("")
etiquetas(plt.gca(), conteo_excentricidad.sum())
plt.show()


# 10. Extension orbital: a_max / a_min en sistemas con 2 o mas planetas
distancias = df.dropna(subset=["a_ua"]).groupby("hostname")["a_ua"].agg(
    planetas_con_distancia="count",
    a_min="min",
    a_max="max")
distancias = distancias[distancias["planetas_con_distancia"] >= 2].copy()
distancias["extension_orbital"] = distancias["a_max"] / distancias["a_min"]

rangos_extension = pd.cut(distancias["extension_orbital"],bins=[1, 3, 10, 100, float("inf")],
    labels=["Compacto\n< 3 veces","Intermedio\n3 - 10 veces","Extendido\n10 - 100 veces","Muy extendido\n> 100 veces"],
    include_lowest=True,
    right=False)
conteo_extension = rangos_extension.value_counts().reindex(
    rangos_extension.cat.categories, fill_value=0)

colores=["#6D9DC5", "#4C78A8", "#E9C46A", "#E76F51"]

plt.figure(figsize=(10, 7))
sns.barplot(x=conteo_extension.index , y=conteo_extension.values,
            hue=conteo_extension.index,palette=colores)

plt.title("10. Extension orbital de sistemas multiplaneta")
plt.xlabel("Relacion entre la orbita mas externa e interna")
plt.ylabel("Numero de planetas")
etiquetas(plt.gca(), conteo_extension.sum())
plt.show()









