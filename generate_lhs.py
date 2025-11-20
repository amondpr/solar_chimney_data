import numpy as np
import pandas as pd
from pyDOE2 import lhs

N = 69

# Parameter ranges (from your manuscript)
bounds = {
    "chimney_height": (125, 290),
    "collector_diameter": (165, 320),
    "chimney_inlet_diameter": (10.5, 55.5),
    "collector_inlet_height": (0.1, 1.5)
}

lhs_unit = lhs(len(bounds), samples=N)

data = {}
for i, (key, (low, high)) in enumerate(bounds.items()):
    data[key] = low + (high - low) * lhs_unit[:, i]

df = pd.DataFrame(data)
df["solar_irradiation"] = np.random.uniform(670, 1020, N)
df["ambient_temperature"] = np.random.uniform(290, 312, N)

df.to_csv("lhs_parameters.csv", index=False)
