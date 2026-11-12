import pandas as pd
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent

CLEAN = ROOT / "CLEAN" 

CSV_FILES = ["dataset_merged.csv"]

df = pd.read_csv("Clean/dataset_merged.csv")

print(df.head)
print(df.columns)
print(df.shape)
print(df.info())


print(df["default_flag"].value_counts()) # 1 
print(df["pl_orbper_x"].sort_values(ascending=False).head(25))
print(df["pl_orbper_x"].head(25))
print(df["pl_orbper_x"].value_counts())
print(df["pl_orbper_x"].max())
print(round(df["pl_orbper_x"].describe(),2))
mask_orbit = df["pl_orbper_x"] > 37
print(df[mask_orbit])
print(df["pl_controv_flag"].value_counts())

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
