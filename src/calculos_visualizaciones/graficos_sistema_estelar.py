

import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "clean"
CSV_FILES = ["estrellas.csv","planetas.csv"]


df = pd.read_csv(CLEAN / "dataset_merged.csv")

'''
st_spectype      Tipo espectral de la estrella.
st_teff_y        Temperatura efectiva estelar [K]; procedente del segundo DataFrame.
st_rad           Radio estelar [radios solares].
st_mass_y        Masa estelar [masas solares]; procedente del segundo DataFrame.
st_met           Metalicidad estelar [dex].
st_metratio      Escala de la metalicidad, por ejemplo [Fe/H] o [M/H].
st_logg          Gravedad superficial estelar [log10(cm/s²)].'''

print(df.head())

print(df["st_rad"].info)
print(df["st_rad"].min())
total_sistemas = df["hostname"].nunique()

print(f"Numero total de sistemas estelares: {total_sistemas}")


# RADIO de estrellas respecto al sol

df = pd.read_csv(CLEAN / "estrellas.csv")
radios = df["st_rad"].dropna()

categorias = pd.cut(
    radios,
    bins=[0, 0.5, 0.9, 1.1, 2, float("inf")],
    labels=[
        "Muy pequeñas\n(< 0,5 R☉)",
        "Pequeñas\n(0,5–0,9 R☉)",
        "Similares al Sol\n(0,9–1,1 R☉)",
        "Grandes\n(1,1–2 R☉)",
        "Muy grandes\n(> 2 R☉)"
    ],
    include_lowest=True
)

conteo = categorias.value_counts().reindex(categorias.cat.categories)

colores = ["#2E86AB", "#70B7D1", "#F2C14E", "#F28E5B", "#C94C4C"]

plt.figure(figsize=(11, 6))
barras = plt.bar(
    conteo.index,
    conteo.values,
    color=colores,
    edgecolor="white",
    width=0.7
)

plt.title("Radio de las estrellas anfitrionas respecto al Sol")
plt.ylabel("Número de estrellas")
plt.grid(axis="y", alpha=0.25)

for barra, valor in zip(barras, conteo.values):
    porcentaje = valor / conteo.sum() * 100
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        valor + 20,
        f"{valor}\n({porcentaje:.1f}%)",
        ha="center",
        va="bottom"
    )

plt.ylim(0, conteo.max() * 1.15)
plt.tight_layout()
plt.show()

#-------------------------------

# Gráfico: clasificación estelar según temperatura efectiva

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(CLEAN / "estrellas.csv")
temperaturas = df["st_teff"].dropna()

# Etiquetas cortas para clasificar
clases = pd.cut(
    temperaturas,
    bins=[0, 2400, 3700, 5200, 6000, 7500, 10000, 30000, float("inf")],
    labels=["Ultrafrias", "M", "K", "G", "F", "A", "B", "O"],
    include_lowest=True,
    right=False
)

conteo = clases.value_counts().reindex(
    ["Ultrafrias", "M", "K", "G", "F", "A", "B", "O"],
    fill_value=0
)
etiquetas_x = [
    "Ultrafrias\n< 2400 K",
    "M\n2400 - 3700 K",
    "K\n3700 - 5200 K",
    "G\n5200 - 6000 K",
    "F\n6000 - 7500 K",
    "A\n7500 - 10000 K",
    "B\n10000 - 30000 K",
    "O\n>= 30000 K"
]

colores = [
    "#6A4C93", "#D1495B", "#E9A23B", "#F6D55C",
    "#F97B72", "#A9D6E5", "#6D9DC5", "#4056A1"
]

plt.figure(figsize=(12, 6))

posiciones = range(len(conteo))

barras = plt.bar(
    posiciones,
    conteo.values,
    color=colores,
    edgecolor="white",
    width=0.75
)

# Fuerza las etiquetas de dos lineas bajo cada barra
plt.xticks(posiciones, etiquetas_x)

plt.title("Clasificacion de estrellas anfitrionas por temperatura")
plt.xlabel("Clase espectral y rango de temperatura")
plt.ylabel("Numero de estrellas")
plt.grid(axis="y", alpha=0.25)

for barra, cantidad in zip(barras, conteo.values):
    porcentaje = cantidad / conteo.sum() * 100

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        cantidad + conteo.max() * 0.015,
        f"{cantidad}\n({porcentaje:.1f}%)",
        ha="center",
        va="bottom"
    )

plt.ylim(0, conteo.max() * 1.16)
plt.tight_layout()
plt.show()

#--------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv(CLEAN / "estrellas.csv")

# Necesitamos radio y temperatura para estimar la luminosidad
estrellas = df.dropna(subset=["st_rad", "st_teff"]).copy()

# Luminosidad relativa al Sol:
# L / L_sol = (R / R_sol)^2 * (T / T_sol)^4
temperatura_sol = 5772

estrellas["luminosidad_relativa"] = (
    estrellas["st_rad"] ** 2
    * (estrellas["st_teff"] / temperatura_sol) ** 4
)

luminosidades = estrellas["luminosidad_relativa"]

# Clasificar respecto a la luminosidad solar
rangos_luminosidad = pd.cut(
    luminosidades,
    bins=[0, 0.01, 0.1, 0.5, 0.85, 1.15, 2, 10, float("inf")],
    labels=[
        "Muy baja\n< 0.01 L_sol",
        "Baja\n0.01 - 0.1 L_sol",
        "Menor que el Sol\n0.1 - 0.5 L_sol",
        "Un poco menor\n0.5 - 0.85 L_sol",
        "Similar al Sol\n0.85 - 1.15 L_sol",
        "Un poco mayor\n1.15 - 2 L_sol",
        "Alta\n2 - 10 L_sol",
        "Muy alta\n> 10 L_sol"
    ],
    include_lowest=True,
    right=False
)

conteo = rangos_luminosidad.value_counts().reindex(
    rangos_luminosidad.cat.categories,
    fill_value=0
)

colores = [
    "#352F6E",
    "#5271A5",
    "#79B8D1",
    "#F6D55C",
    "#F28E5B",
    "#C94C4C"
]

plt.figure(figsize=(13, 6))

posiciones = range(len(conteo))

barras = plt.bar(
    posiciones,
    conteo.values,
    color=colores,
    edgecolor="white",
    width=0.75
)

plt.xticks(posiciones, conteo.index)

plt.title("Luminosidad estimada de estrellas anfitrionas respecto al Sol")
plt.xlabel("Rango de luminosidad")
plt.ylabel("Numero de estrellas")
plt.grid(axis="y", alpha=0.25)

for barra, cantidad in zip(barras, conteo.values):
    porcentaje = cantidad / conteo.sum() * 100

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        cantidad + conteo.max() * 0.015,
        f"{cantidad}\n({porcentaje:.1f}%)",
        ha="center",
        va="bottom"
    )

plt.ylim(0, conteo.max() * 1.16)
plt.tight_layout()
plt.show()


#------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------------------------
# 1. Cargar el dataset
# ----------------------------------------------------
df = pd.read_csv(CLEAN / "dataset_merged.csv")

# Convertir columnas a numeros
columnas_numericas = [
    "st_teff_y",
    "st_rad",
    "st_mass_y",
    "pl_orbper_y",
    "pl_rade_y"
]

for columna in columnas_numericas:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

# Conservar solo filas con datos necesarios
datos = df.dropna(
    subset=["hostname", "st_teff_y", "st_rad", "st_mass_y", "pl_orbper_y"]
).copy()

# Eliminar datos fisicamente imposibles
datos = datos[
    (datos["st_teff_y"] > 0) &
    (datos["st_rad"] > 0) &
    (datos["st_mass_y"] > 0) &
    (datos["st_mass_y"] < 100) &
    (datos["pl_orbper_y"] > 0)
].copy()

# ----------------------------------------------------
# 2. Calcular luminosidad respecto al Sol
#
# L / L_sol = R^2 * (T / T_sol)^4
# ----------------------------------------------------
temperatura_sol = 5772

datos["luminosidad_relativa"] = (
    datos["st_rad"] ** 2
    * (datos["st_teff_y"] / temperatura_sol) ** 4
)

# ----------------------------------------------------
# 3. Calcular limites aproximados de zona habitable
# ----------------------------------------------------
datos["zh_interior_ua"] = (
    0.95 * datos["luminosidad_relativa"] ** 0.5
)

datos["zh_exterior_ua"] = (
    1.67 * datos["luminosidad_relativa"] ** 0.5
)

# ----------------------------------------------------
# 4. Calcular distancia orbital aproximada con Kepler
#
# P se convierte de dias a anos.
# a queda expresada en UA.
# ----------------------------------------------------
datos["periodo_anos"] = datos["pl_orbper_y"] / 365.25

datos["distancia_orbital_ua"] = (
    datos["st_mass_y"] * datos["periodo_anos"] ** 2
) ** (1 / 3)

# ----------------------------------------------------
# 5. Seleccionar planetas en zona habitable
#
# Se limita el radio a planetas aproximadamente rocosos:
# entre 0.5 y 1.6 radios terrestres.
# ----------------------------------------------------
candidatos = datos[
    (datos["distancia_orbital_ua"] >= datos["zh_interior_ua"]) &
    (datos["distancia_orbital_ua"] <= datos["zh_exterior_ua"]) &
    (datos["pl_rade_y"] >= 0.5) &
    (datos["pl_rade_y"] <= 1.6)
].copy()

# ----------------------------------------------------
# 6. Contar candidatos por sistema estelar
# ----------------------------------------------------
conteo_sistemas = (
    candidatos
    .groupby("hostname")["pl_name"]
    .count()
    .sort_values(ascending=False)
)

# Numero de sistemas con uno o mas planetas candidatos
numero_sistemas_habitables = conteo_sistemas.index.nunique()

# Total de sistemas para los que se pudieron hacer calculos
total_sistemas_analizados = datos["hostname"].nunique()

# Porcentaje de sistemas con al menos un candidato
porcentaje_sistemas = (
    numero_sistemas_habitables / total_sistemas_analizados * 100
)

# ----------------------------------------------------
# 7. Mostrar resultados en consola
# ----------------------------------------------------
print(f"Planetas candidatos encontrados: {len(candidatos)}")
print(f"Total de sistemas analizados: {total_sistemas_analizados}")

print(
    f"Sistemas con uno o mas planetas potencialmente habitables: "
    f"{numero_sistemas_habitables} "
    f"({porcentaje_sistemas:.1f}%)"
)

print("\nCandidatos por sistema:")
print(conteo_sistemas)

# ----------------------------------------------------
# 8. Grafico: sistemas con mas candidatos
# ----------------------------------------------------
top_sistemas = conteo_sistemas.head(25).sort_values()

plt.figure(figsize=(11, 8))

barras = plt.barh(
    top_sistemas.index,
    top_sistemas.values,
    color="#4C78A8",
    edgecolor="white"
)

plt.title("Sistemas con mas planetas candidatos en zona habitable")
plt.xlabel("Numero de planetas potencialmente habitables")
plt.ylabel("Sistema estelar")
plt.grid(axis="x", alpha=0.25)

for barra, cantidad in zip(barras, top_sistemas.values):
    plt.text(
        cantidad + 0.03,
        barra.get_y() + barra.get_height() / 2,
        str(cantidad),
        va="center"
    )

plt.xlim(0, top_sistemas.max() + 1)
plt.tight_layout()
plt.show()

#---------------------------------------

# ----------------------------------------------------
# GRAFICO 5: Resultado de la busqueda de candidatos
# ----------------------------------------------------

# Total de planetas unicos del dataset
total_planetas = df["pl_name"].nunique()

# Planetas que tenian datos suficientes y radio compatible
planetas_analizados = len(datos)

# Planetas que cumplen zona habitable y radio rocoso
numero_candidatos = len(candidatos)

# Planetas analizados que no cumplen la zona habitable
fuera_zona_habitable = planetas_analizados - numero_candidatos

# Planetas sin datos suficientes o descartados por su radio
sin_datos_o_no_rocosos = total_planetas - planetas_analizados

categorias = [
    "Candidatos en\\nzona habitable",
    "Analizados, pero\\nfuera de zona habitable",
    "Sin datos suficientes\\no no rocosos"
]

valores = [
    numero_candidatos,
    fuera_zona_habitable,
    sin_datos_o_no_rocosos
]

colores = [
    "#2A9D8F",  # verde: candidatos
    "#E9C46A",  # amarillo: evaluados pero fuera
    "#B0B0B0"   # gris: no evaluables
]

plt.figure(figsize=(10, 6))

barras = plt.bar(
    categorias,
    valores,
    color=colores,
    edgecolor="white",
    width=0.65
)

plt.title("Planetas candidatos a estar en zona habitable")
plt.ylabel("Numero de planetas")
plt.grid(axis="y", alpha=0.25)

for barra, valor in zip(barras, valores):
    porcentaje = valor / total_planetas * 100

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        valor + total_planetas * 0.01,
        f"{valor}\\n({porcentaje:.2f}%)",
        ha="center",
        va="bottom"
    )

plt.ylim(0, max(valores) * 1.15)
plt.tight_layout()
plt.show()

#---------------------------------

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# ----------------------------------------------------
# 1. Cargar dataset unido
# ----------------------------------------------------
df = pd.read_csv(CLEAN / "dataset_merged.csv")

# Convertir columnas necesarias a numeros
columnas_numericas = [
    "st_teff_y",
    "st_rad",
    "st_mass_y",
    "pl_orbper_y"
]

for columna in columnas_numericas:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

# Una fila por planeta
planetas = df.drop_duplicates(subset=["hostname", "pl_name"]).copy()

# Total real de sistemas y planetas del dataset
total_sistemas = planetas["hostname"].nunique()
total_planetas = planetas["pl_name"].nunique()

print(f"Total de sistemas estelares: {total_sistemas}")
print(f"Total de planetas: {total_planetas}")

# ----------------------------------------------------
# 2. Conservar planetas con datos suficientes
#
# No filtramos por radio planetario:
# buscamos todos los planetas ubicados en zona habitable.
# ----------------------------------------------------
datos = planetas.dropna(
    subset=[
        "hostname",
        "st_teff_y",
        "st_rad",
        "st_mass_y",
        "pl_orbper_y"
    ]
).copy()

# Eliminar datos fisicamente imposibles
datos = datos[
    (datos["st_teff_y"] > 0) &
    (datos["st_rad"] > 0) &
    (datos["st_mass_y"] > 0) &
    (datos["st_mass_y"] < 100) &
    (datos["pl_orbper_y"] > 0)
].copy()

# ----------------------------------------------------
# 3. Calcular luminosidad de cada estrella
#
# L / L_sol = R^2 * (T / T_sol)^4
# ----------------------------------------------------
temperatura_sol = 5772

datos["luminosidad_relativa"] = (
    datos["st_rad"] ** 2
    * (datos["st_teff_y"] / temperatura_sol) ** 4
)

# ----------------------------------------------------
# 4. Estimar los limites de la zona habitable
#
# Distancias expresadas en UA.
# ----------------------------------------------------
datos["zh_interior_ua"] = (
    0.95 * datos["luminosidad_relativa"] ** 0.5
)

datos["zh_exterior_ua"] = (
    1.67 * datos["luminosidad_relativa"] ** 0.5
)

# ----------------------------------------------------
# 5. Calcular distancia orbital aproximada
#
# Tercera ley de Kepler:
# a^3 = M * P^2
#
# P: periodo orbital en anos
# M: masa estelar en masas solares
# a: distancia orbital en UA
# ----------------------------------------------------
datos["periodo_anos"] = datos["pl_orbper_y"] / 365.25

datos["distancia_orbital_ua"] = (
    datos["st_mass_y"] * datos["periodo_anos"] ** 2
) ** (1 / 3)

# ----------------------------------------------------
# 6. Seleccionar planetas dentro de la zona habitable
# ----------------------------------------------------
planetas_zona_habitable = datos[
    (datos["distancia_orbital_ua"] >= datos["zh_interior_ua"]) &
    (datos["distancia_orbital_ua"] <= datos["zh_exterior_ua"])
].copy()

# ----------------------------------------------------
# 7. Calcular resultados
# ----------------------------------------------------
numero_planetas_zh = len(planetas_zona_habitable)

conteo_sistemas = (
    planetas_zona_habitable
    .groupby("hostname")["pl_name"]
    .count()
    .sort_values(ascending=False)
)

numero_sistemas_zh = conteo_sistemas.index.nunique()

porcentaje_planetas = numero_planetas_zh / total_planetas * 100
porcentaje_sistemas = numero_sistemas_zh / total_sistemas * 100

print("\nRESULTADOS")
print(f"Planetas con datos suficientes: {len(datos)}")
print(f"Planetas en zona habitable: {numero_planetas_zh}")
print(f"Porcentaje sobre todos los planetas: {porcentaje_planetas:.2f}%")

print(
    f"Sistemas con uno o mas planetas en zona habitable: "
    f"{numero_sistemas_zh}"
)
print(
    f"Porcentaje sobre todos los sistemas: "
    f"{porcentaje_sistemas:.2f}%"
)

print("\nPlanetas en zona habitable por sistema:")
print(conteo_sistemas)

# ----------------------------------------------------
# 8. Grafico: planetas en zona habitable frente al resto
# ----------------------------------------------------
fuera_zona_habitable = len(datos) - numero_planetas_zh
sin_datos_suficientes = total_planetas - len(datos)

categorias = [
    "En zona\\nhabitable",
    "Analizados, fuera\\nde zona habitable",
    "Sin datos\\nsuficientes"
]

valores = [
    numero_planetas_zh,
    fuera_zona_habitable,
    sin_datos_suficientes
]

colores = [
    "#2A9D8F",
    "#E9C46A",
    "#B0B0B0"
]

plt.figure(figsize=(10, 6))

barras = plt.bar(
    categorias,
    valores,
    color=colores,
    edgecolor="white",
    width=0.65
)

plt.title("Planetas situados en la zona habitable estimada")
plt.ylabel("Numero de planetas")
plt.grid(axis="y", alpha=0.25)

for barra, valor in zip(barras, valores):
    porcentaje = valor / total_planetas * 100

    plt.text(
        barra.get_x() + barra.get_width() / 2,
        valor + total_planetas * 0.01,
        f"{valor}\n({porcentaje:.2f}%)",
        ha="center",
        va="bottom"
    )

plt.ylim(0, max(valores) * 1.15)
plt.tight_layout()
plt.show()

# ----------------------------------------------------
# 9. Grafico: sistemas con mas planetas en zona habitable
# ----------------------------------------------------
top_sistemas = conteo_sistemas.head(25).sort_values()

if not top_sistemas.empty:
    plt.figure(figsize=(11, 8))

    barras = plt.barh(
        top_sistemas.index,
        top_sistemas.values,
        color="#4C78A8",
        edgecolor="white"
    )

    plt.title("Sistemas con planetas en zona habitable estimada")
    plt.xlabel("Numero de planetas en zona habitable")
    plt.ylabel("Sistema estelar")
    plt.grid(axis="x", alpha=0.25)

    for barra, cantidad in zip(barras, top_sistemas.values):
        plt.text(
            cantidad + 0.03,
            barra.get_y() + barra.get_height() / 2,
            str(cantidad),
            va="center"
        )

    plt.xlim(0, top_sistemas.max() + 1)
    plt.tight_layout()
    plt.show()
