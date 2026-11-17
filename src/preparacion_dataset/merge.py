
import pandas as pd
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CLEAN = ROOT / "clean"

CLEAN.mkdir(parents=True, exist_ok=True)

CSV_FILES = ["descubrimientos.csv","estrellas.csv","mediciones.csv","planetas.csv","sistemas.csv"]

d = pd.read_csv(CLEAN / "descubrimientos.csv")
e = pd.read_csv(CLEAN / "estrellas.csv")
m = pd.read_csv(CLEAN / "mediciones.csv")
p = pd.read_csv(CLEAN / "planetas.csv")
s = pd.read_csv(CLEAN / "sistemas.csv")


print(d.shape)
print(e.shape)
print(m.shape)
print(p.shape)
print(s.shape)

print(d["disc_year"].sort_values(ascending=False))

mask_year = (d["disc_year"] == 3025) | (d["disc_year"] == 1700)
d.loc[mask_year, "disc_year"] = pd.NA
print(d.head())
print(d["disc_year"].sort_values(ascending=False))


print(m.head())
mask_flag = m["default_flag"] == 1
m2 = m.loc[mask_flag]
print(m2.head)
print(m2.shape)

m2.to_csv(CLEAN / "mediciones2.csv", index=False)

print(d.duplicated().sum())
print(e.duplicated().sum())
print(m2.duplicated().sum())
print(p.duplicated().sum())
print(s.duplicated().sum())

dataset = m2.merge(
    p,
    on="pl_name",
    how="left"
).sort_values(by="pl_name", ascending=False)
print(dataset.shape)

dataset = dataset.merge(
    d,
    on="pl_name",
    how="left"
).sort_values(by="pl_name", ascending=False)
print(dataset.shape)

dataset = dataset.merge(
    e,
    on="hostname",
    how="left"
).sort_values(by="hostname", ascending=False)
print(dataset.shape)

dataset = dataset.merge(
    s,
    on="hostname",
    how="left"
).sort_values(by="hostname", ascending=False)
print(dataset.shape)

dataset.to_csv(CLEAN / "dataset_merged.csv", index=False)
