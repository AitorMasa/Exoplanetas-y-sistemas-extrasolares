
import pandas as pd
from pathlib import Path


ROOT = Path(__file__).resolve().parent

CLEAN = ROOT / "CLEAN" 
RAW = ROOT / "RAW"
ISSUES = ROOT / "Issues"
DATASET_EDA = ROOT / "DATASETS_EDA"

for folder in [CLEAN,RAW,ISSUES,DATASET_EDA]:
    folder.mkdir(parents=True, exist_ok=True)

CSV_FILES = ["descubrimientos.csv","estrellas.csv","mediciones.csv","planetas.csv","sistemas.csv"]

d = pd.read_csv(DATASET_EDA / "descubrimientos.csv")
e = pd.read_csv(DATASET_EDA / "estrellas.csv")
m = pd.read_csv(DATASET_EDA / "mediciones.csv")
p = pd.read_csv(DATASET_EDA / "planetas.csv")
s = pd.read_csv(DATASET_EDA / "sistemas.csv")

print(d.head())
print(d.shape)
print(e.head())
print(e.shape)
print(m.head())
m = m.drop(columns=["pl_refname","pl_bmasse", "rowupdate"])
print(m)
print(p.head())
p = p.drop(columns=["pl_orbsmax","pl_bmassprov", "pl_bmassj"])
print(p)
print(s.head())
s = s.drop(columns=["sy_vmag","sy_kmag", "sy_gaiamag"])
print(s)

print(d.shape)
print(e.shape)
print(m.shape)
print(p.shape)
print(s.shape)

print(d.duplicated().sum())
print(e.duplicated().sum())
print(m.duplicated().sum())
print(p.duplicated().sum())
print(s.duplicated().sum())

dup = d.duplicated(keep=False)
print(d.loc[dup].sort_values("pl_name"))
d = d.drop_duplicates()
print(d.duplicated().sum())

dup = e.duplicated(keep=False)
print(e.loc[dup].sort_values("hostname"))
e = e.drop_duplicates()
print(d.duplicated().sum())

dup = m.duplicated(keep=False)
print(m.loc[dup].sort_values("measurement_id"))
m = m.drop_duplicates()
print(d.duplicated().sum())

dup = p.duplicated(keep=False)
print(p.loc[dup].sort_values("pl_name"))
p = p.drop_duplicates()
print(d.duplicated().sum())

dup = s.duplicated(keep=False)
print(s.loc[dup].sort_values("hostname"))
s = s.drop_duplicates()
print(d.duplicated().sum())

print(d.shape)
print(e.shape)
print(m.shape)
print(p.shape)
print(s.shape)

d.to_csv("CLEAN/descubrimientos.csv", index=False)
e.to_csv("CLEAN/estrellas.csv", index=False)
m.to_csv("CLEAN/mediciones.csv", index=False)
p.to_csv("CLEAN/planetas.csv", index=False)
s.to_csv("CLEAN/sistemas.csv", index=False)