import pickle
from pathlib import Path

root_path = Path(__file__).resolve().parent.parent
model_dir = root_path / "models"

model_path = model_dir / "model.pkl"


def load():
    with open(model_path, "rb") as file:
        model_dic = pickle.load(file)

    model = model_dic["model"]
    LabelEnc = model_dic["LabelEnc"]

    return model, LabelEnc
