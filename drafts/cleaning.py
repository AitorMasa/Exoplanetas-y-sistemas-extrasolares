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
df= df.drop(columns=["hostname_y","pl_orbper_y","pl_orbeccen_y","pl_eqt_y","pl_pubdate_y",
    "releasedate_y","st_teff_y","st_mass_y"])

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

df.to_csv("Clean/dataset_merged.csv")