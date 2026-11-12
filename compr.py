import pandas as pd
import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLEAN = ROOT / "CLEAN"

df = pd.read_csv(CLEAN / "dataset_merged.csv")


# con pl_rade, pl_orbeccen, pl_eqt, st_teff y
print(df.shape)
distintos = ~np.isclose(
    df["pl_rade_x"],
    df["pl_rade_y"],
    equal_nan=True
)

print(
    df.loc[distintos, [
        "pl_name",
        "pl_orbper_x",
        "pl_orbper_y",
        "default_flag",
        "pl_pubdate_x",
        "pl_pubdate_y"
    ]]
    .sort_values("pl_name")
    )


print("\nCantidad de períodos orbitales distintos:", distintos.sum())