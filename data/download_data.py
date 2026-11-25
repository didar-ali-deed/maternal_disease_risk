from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo

root_path = Path(__file__).parent.parent
data_path = root_path / "data" / "maternal_risk.csv"

# fetch dataset
maternal_health_risk = fetch_ucirepo(id=863)

# data (as pandas dataframes)
X = maternal_health_risk.data.features
y = maternal_health_risk.data.targets

df = pd.concat([X, y], axis=1)
df.to_csv(data_path, index=False)
print(f"Data Saved to {data_path}")
