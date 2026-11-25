import pickle
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
model_dir = root_path / "models"
model_dir.mkdir(parents=True, exist_ok=True)  # Creates 'models' folder if missing

model_path = model_dir / "model.pkl"
metric_path = model_dir / "metrics.json"  # Changed from .csv to .json


def load():
    with open(model_path, "rb") as file:
        model_dic = pickle.load(file)
    model = model_dic["model"]
    le = model_dic["enc"]

    return model, le
