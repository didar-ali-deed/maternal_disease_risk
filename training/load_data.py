from pathlib import Path

import pandas as pd

root_path = Path(__file__).parent.parent
data_path = root_path / "data" / "maternal_risk.csv"


def load_data():
    print(data_path)
    if not data_path.exists():
        raise FileExistsError("File Not Found")
    df = pd.read_csv(data_path)
    return df
