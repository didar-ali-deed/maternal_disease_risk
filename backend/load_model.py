import pickle
from functools import lru_cache
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT_PATH / "models" / "model.pkl"


@lru_cache(maxsize=1)
def load():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")

    with MODEL_PATH.open("rb") as file:
        model_dic = pickle.load(file)

    model = model_dic["model"]
    label_encoder = model_dic["LabelEnc"]

    return model, label_encoder
