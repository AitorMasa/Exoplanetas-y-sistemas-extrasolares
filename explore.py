

import pandas as pd
from pathlib import Path


ROOT = Path(__file__).resolve().parent

RAW = ROOT / "RAW"
CLEAN = ROOT / "CLEAN"

RAW.mkdir(parents=True, exist_ok=True)
CLEAN.mkdir(parents=True, exist_ok=True)
  
df = pd.read_csv(CLEAN / "dataset_merged.csv", comment="#")

print(df.columns)    #1 parsec ≈ 3,26 años luz
print(df.shape)
print(df["discoverymethod"].value_counts())
print(df["discoverymethod"].value_counts().sum()) #40387 +36k transit 3k radial velocity
print(df["default_flag"].value_counts())#0    33923   1     6464
print(df["pl_orbeccen_x"].value_counts().sort_values(ascending=True))
print(df["pl_orbeccen_x"].sort_values(ascending=False))
print(df["pl_orbeccen_x"].isna().sum())#21167

print(df["pl_name"].value_counts())
print(df["pl_name"].unique())
print(df["pl_name"].nunique()) #6464
print(df["hostname"])
print(df["sy_snum"].value_counts()) #N estrelas  gravitacionalemnte engaged 
print(df["sy_pnum"].value_counts()) #N planetas confirmados
print(df["disc_year"].value_counts())
print(df["disc_year"].value_counts().nunique()) # 32 años diferentes disc_facility
print(df["disc_facility"].value_counts())
print(df["disc_facility"].value_counts().nunique()) # 47  obs. diferntes +28.5 kepleler 2.5 k + Tess +2k K2 1 k SuperWASP   
print(df["disc_facility"].count()) # 40387 planets pl_orbper
print(df["pl_orbper_x"].describe())
print(df["pl_orbper_x"].value_counts()) #max 7 iguales 
print(df["pl_orbper_x"].count()) #Name: count, Length: 23984, dtype: int64 36954

print(df["disc_year"].value_counts())
print(df["disc_year"].nunique()) # 32 años diferentes disc_facility
mask_year = (df["disc_year"] == 1700) | (df["disc_year"] == 3025)
df = df.loc[~mask_year]
print(df["disc_year"].value_counts())
print(df["disc_year"].nunique()) 

print(df["disc_facility"].value_counts())
print(df["disc_facility"].nunique()) # 47  obs. diferntes +28.5 kepleler 2.5 k + Tess +2k K2 1 k SuperWASP   
print(df["disc_facility"].count()) # 40387 planets pl_orbper

print(df["soltype"])
print(df["soltype"].value_counts())
print(df["pl_controv_flag"].value_counts())
print(df["pl_rade_x"].value_counts())
print(df["pl_rade_x"].describe())
print(df["pl_bmasse"].describe())