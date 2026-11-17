import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "clean"
df = pd.read_csv(CLEAN / "dataset_merged.csv")

# Preparacion comun
for columna in [
    "sy_pnum", "st_teff_y", "st_rad", "st_mass_y", "pl_orbper_y",
    "pl_rade_y", "pl_bmasse", "pl_orbeccen_y"
]:
    df[columna] = pd.to_numeric(df[columna], errors="coerce")

# Una fila por planeta y una fila por sistema.
planetas = df.drop_duplicates(subset=["hostname", "pl_name"]).copy()
sistemas = planetas.drop_duplicates(subset="hostname").copy()

# Distancia orbital estimada con la tercera ley de Kepler.
validos_orbita = (
    (planetas["st_mass_y"] > 0) & (planetas["st_mass_y"] < 100) &
    (planetas["pl_orbper_y"] > 0)
)
planetas["a_ua"] = float("nan")
planetas.loc[validos_orbita, "a_ua"] = (
    planetas.loc[validos_orbita, "st_mass_y"]
    * (planetas.loc[validos_orbita, "pl_orbper_y"] / 365.25) ** 2
) ** (1 / 3)

# Luminosidad y zona habitable aproximadas.
temperatura_sol = 5772
validos_estrella = (
    (planetas["st_teff_y"] > 0) & (planetas["st_rad"] > 0)
)
planetas["luminosidad_relativa"] = float("nan")
planetas.loc[validos_estrella, "luminosidad_relativa"] = (
    planetas.loc[validos_estrella, "st_rad"] ** 2
    * (planetas.loc[validos_estrella, "st_teff_y"] / temperatura_sol) ** 4
)
planetas["zh_interior"] = 0.95 * planetas["luminosidad_relativa"] ** 0.5
planetas["zh_exterior"] = 1.67 * planetas["luminosidad_relativa"] ** 0.5

planetas["en_zh"] = (
    (planetas["a_ua"] >= planetas["zh_interior"]) &
    (planetas["a_ua"] <= planetas["zh_exterior"])
)

# Definiciones de trabajo. No son clasificaciones universales.
planetas["pequeno_interior"] = (
    (planetas["pl_rade_y"] >= 0.5) &
    (planetas["pl_rade_y"] <= 1.6) &
    (planetas["a_ua"] < 1.5)
)
planetas["gigante_caliente"] = (
    (planetas["pl_rade_y"] >= 8) &
    (planetas["pl_orbper_y"] < 10)
)
planetas["gigante_exterior"] = (
    (planetas["pl_rade_y"] >= 8) &
    (planetas["a_ua"] >= 3)
)


def barras(conteo, titulo, xlabel="", ylabel="Numero de sistemas",
           colores=None, figsize=(10, 6)):
    """Grafico de barras con cantidad y porcentaje."""
    conteo = conteo[conteo.index.notna()]
    if conteo.empty:
        print(f"No hay datos para: {titulo}")
        return

    if colores is None:
        colores = "#4C78A8"

    plt.figure(figsize=figsize)
    posiciones = range(len(conteo))
    valores = conteo.values
    grafico = plt.bar(posiciones, valores, color=colores, edgecolor="white")
    plt.xticks(posiciones, conteo.index)
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.25)

    for barra, valor in zip(grafico, valores):
        porcentaje = valor / valores.sum() * 100
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            valor + max(valores) * 0.015,
            f"{valor}\n({porcentaje:.1f}%)",
            ha="center",
            va="bottom"
        )

    plt.ylim(0, max(valores) * 1.16)
    plt.tight_layout()
    plt.show()


# 1. Cuantos planetas hay por sistema, frente a 8 en el Sistema Solar
conteo_planetas = sistemas["sy_pnum"].dropna().value_counts().sort_index()
barras(
    conteo_planetas,
    "1. Numero de planetas conocidos por sistema",
    "Planetas conocidos en el sistema",
    colores="#4C78A8"
)


# 2. Sistemas con planetas pequenos en la zona interior
sistemas_pequenos = (
    planetas.groupby("hostname")["pequeno_interior"].any()
    .map({True: "Con planeta pequeno interior", False: "Sin candidato detectado"})
    .value_counts()
)
barras(
    sistemas_pequenos,
    "2. Sistemas con planetas pequenos en la zona interior",
    colores=["#2A9D8F", "#B0B0B0"]
)


# 3. Sistemas con y sin gigantes calientes
sistemas_gigantes_calientes = (
    planetas.groupby("hostname")["gigante_caliente"].any()
    .map({True: "Con gigante caliente", False: "Sin gigante caliente detectado"})
    .value_counts()
)
barras(
    sistemas_gigantes_calientes,
    "3. Gigantes calientes en los sistemas",
    colores=["#E76F51", "#4C78A8"]
)


# 4. Sistemas con gigantes exteriores tipo Jupiter/Saturno
sistemas_gigantes_exteriores = (
    planetas.groupby("hostname")["gigante_exterior"].any()
    .map({True: "Con gigante exterior", False: "Sin gigante exterior detectado"})
    .value_counts()
)
barras(
    sistemas_gigantes_exteriores,
    "4. Gigantes exteriores en los sistemas",
    colores=["#E9C46A", "#B0B0B0"]
)


# 5. Sistemas con al menos un planeta en zona habitable estimada
sistemas_zh = (
    planetas.groupby("hostname")["en_zh"].any()
    .map({True: "Con planeta en zona habitable", False: "Sin planeta HZ detectado"})
    .value_counts()
)
barras(
    sistemas_zh,
    "5. Sistemas con planetas en zona habitable estimada",
    colores=["#2A9D8F", "#B0B0B0"]
)


# 6. Frecuencia de estrellas parecidas al Sol
sistemas["similar_al_sol"] = (
    sistemas["st_teff_y"].between(5500, 6050) &
    sistemas["st_rad"].between(0.85, 1.15) &
    sistemas["st_mass_y"].between(0.85, 1.15)
)
conteo_solares = sistemas["similar_al_sol"].map(
    {True: "Similar al Sol", False: "No similar al Sol"}
).value_counts()
barras(
    conteo_solares,
    "6. Estrellas similares al Sol",
    colores=["#F6D55C", "#B0B0B0"]
)


# 7. Analogos terrestres alrededor de estrellas similares al Sol
# Criterio: estrella similar al Sol, planeta 0.8 - 1.25 R_tierra y en HZ.
planetas["estrella_similar_al_sol"] = (
    planetas["st_teff_y"].between(5500, 6050) &
    planetas["st_rad"].between(0.85, 1.15) &
    planetas["st_mass_y"].between(0.85, 1.15)
)
planetas["analogo_tierra"] = (
    planetas["estrella_similar_al_sol"] &
    planetas["pl_rade_y"].between(0.8, 1.25) &
    planetas["en_zh"]
)
sistemas_solares = planetas[planetas["estrella_similar_al_sol"]].groupby("hostname")
analogos_por_sistema = sistemas_solares["analogo_tierra"].any()
conteo_analogos = analogos_por_sistema.map(
    {True: "Con analogo terrestre", False: "Sin analogo terrestre detectado"}
).value_counts()
barras(
    conteo_analogos,
    "7. Analogos terrestres en estrellas similares al Sol",
    colores=["#2A9D8F", "#B0B0B0"]
)


# 8. Arquitectura: pequenos interiores y gigantes exteriores
arquitectura = planetas.groupby("hostname").agg(
    pequenos_interiores=("pequeno_interior", "any"),
    gigantes_exteriores=("gigante_exterior", "any")
)
arquitectura["tipo"] = "Ninguno de los dos"
arquitectura.loc[
    arquitectura["pequenos_interiores"] & ~arquitectura["gigantes_exteriores"],
    "tipo"
] = "Solo pequenos interiores"
arquitectura.loc[
    ~arquitectura["pequenos_interiores"] & arquitectura["gigantes_exteriores"],
    "tipo"
] = "Solo gigante exterior"
arquitectura.loc[
    arquitectura["pequenos_interiores"] & arquitectura["gigantes_exteriores"],
    "tipo"
] = "Arquitectura tipo Solar"
conteo_arquitectura = arquitectura["tipo"].value_counts().reindex([
    "Ninguno de los dos",
    "Solo pequenos interiores",
    "Solo gigante exterior",
    "Arquitectura tipo Solar"
], fill_value=0)
barras(
    conteo_arquitectura,
    "8. Arquitectura planetaria por sistema",
    colores=["#B0B0B0", "#4C78A8", "#E9C46A", "#2A9D8F"],
    figsize=(12, 6)
)


# 9. Excentricidad de las orbitas
excentricidades = planetas["pl_orbeccen_y"].dropna()
excentricidades = excentricidades[(excentricidades >= 0) & (excentricidades < 1)]
rangos_excentricidad = pd.cut(
    excentricidades,
    bins=[-0.001, 0.05, 0.15, 0.30, 0.60, 1],
    labels=[
        "Casi circular\n0 - 0.05",
        "Baja\n0.05 - 0.15",
        "Moderada\n0.15 - 0.30",
        "Alta\n0.30 - 0.60",
        "Muy alta\n0.60 - 1"
    ],
    include_lowest=True
)
conteo_excentricidad = rangos_excentricidad.value_counts().reindex(
    rangos_excentricidad.cat.categories, fill_value=0
)
barras(
    conteo_excentricidad,
    "9. Excentricidad de las orbitas de exoplanetas",
    "Rango de excentricidad orbital",
    ylabel="Numero de planetas",
    colores=["#2A9D8F", "#8AB17D", "#E9C46A", "#F4A261", "#E76F51"],
    figsize=(11, 6)
)


# 10. Extension orbital: a_max / a_min en sistemas con 2 o mas planetas
distancias = planetas.dropna(subset=["a_ua"]).groupby("hostname")["a_ua"].agg(
    planetas_con_distancia="count",
    a_min="min",
    a_max="max"
)
distancias = distancias[distancias["planetas_con_distancia"] >= 2].copy()
distancias["extension_orbital"] = distancias["a_max"] / distancias["a_min"]

rangos_extension = pd.cut(
    distancias["extension_orbital"],
    bins=[1, 3, 10, 100, float("inf")],
    labels=[
        "Compacto\n< 3 veces",
        "Intermedio\n3 - 10 veces",
        "Extendido\n10 - 100 veces",
        "Muy extendido\n> 100 veces"
    ],
    include_lowest=True,
    right=False
)
conteo_extension = rangos_extension.value_counts().reindex(
    rangos_extension.cat.categories, fill_value=0
)
barras(
    conteo_extension,
    "10. Extension orbital de sistemas multiplaneta",
    "Relacion entre la orbita mas externa e interna",
    colores=["#6D9DC5", "#4C78A8", "#E9C46A", "#E76F51"]
)


print("\nRESUMEN")
print(f"Sistemas unicos: {sistemas['hostname'].nunique()}")
print(f"Planetas unicos: {planetas['pl_name'].nunique()}")
print(f"Planetas en zona habitable estimada: {planetas['en_zh'].sum()}")
print(f"Sistemas con planeta en zona habitable: {(planetas.groupby('hostname')['en_zh'].any()).sum()}")
print(f"Excentricidad mediana: {excentricidades.median():.3f}")

