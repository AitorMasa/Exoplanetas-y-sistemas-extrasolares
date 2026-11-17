import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLEAN = ROOT / "CLEAN"

df = pd.read_csv(CLEAN / "dataset_merged.csv")

# Localiza todas las parejas columna_x / columna_y
pares = []

for columna_x in df.columns:
    if columna_x.endswith("_x"):
        base = columna_x[:-2]
        columna_y = f"{base}_y"

        if columna_y in df.columns:
            pares.append((base, columna_x, columna_y))

resultados = []

for base, columna_x, columna_y in pares:
    x = df[columna_x]
    y = df[columna_y]

    ambos_nulos = x.isna() & y.isna()
    solo_x = x.notna() & y.isna()
    solo_y = x.isna() & y.notna()
    ambos_con_dato = x.notna() & y.notna()

    # Comparación aproximada para números y exacta para textos/fechas
    if (
        pd.api.types.is_numeric_dtype(x)
        and pd.api.types.is_numeric_dtype(y)
    ):
        iguales_con_dato = pd.Series(
            np.isclose(
                x,
                y,
                rtol=1e-5,
                atol=1e-8,
                equal_nan=False,
            ),
            index=df.index,
        ) & ambos_con_dato
    else:
        iguales_con_dato = x.eq(y) & ambos_con_dato

    distintos = ambos_con_dato & ~iguales_con_dato
    iguales = ambos_nulos | iguales_con_dato

    resultados.append({
        "variable": base,
        "iguales": int(iguales.sum()),
        "distintos": int(distintos.sum()),
        "solo_x_tiene_dato": int(solo_x.sum()),
        "solo_y_tiene_dato": int(solo_y.sum()),
        "ambos_nulos": int(ambos_nulos.sum()),
    })

    # Muestra algunos ejemplos cuando existen diferencias
    if distintos.any():
        columnas_mostrar = [
            columna
            for columna in [
                "pl_name",
                columna_x,
                columna_y,
                "default_flag",
                "pl_pubdate_x",
                "pl_pubdate_y",
            ]
            if columna in df.columns
        ]

        print(f"\nDiferencias encontradas en {base}:")
        print(df.loc[distintos, columnas_mostrar].head(10))

resumen = pd.DataFrame(resultados)

print("\nRESUMEN DE COLUMNAS _x / _y")
print(resumen.to_string(index=False))

distintos = ~np.isclose(
    dataset["pl_orbper_x"],
    dataset["pl_orbper_y"],
    equal_nan=True
)

print(dataset.loc[distintos, [
    "pl_name",
    "pl_orbper_x",
    "pl_orbper_y",
    "default_flag"
]])