import json
import pickle
from pathlib import Path

from load_data import load_data
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

root_path = Path(__file__).resolve().parent.parent
model_dir = root_path / "models"
model_dir.mkdir(parents=True, exist_ok=True)  # Creates 'models' folder if missing

model_path = model_dir / "model.pkl"
metric_path = model_dir / "metrics.json"  # Changed from .csv to .json


def train(df: DataFrame):
    X = df.drop(columns="RiskLevel")
    y = df["RiskLevel"]

    enc = LabelEncoder()
    y = enc.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    print("Shape of Training Data:", X_train.shape)
    print("Shape of Testing Data:", X_test.shape)

    model = RandomForestClassifier(
        n_estimators=400, n_jobs=-1, class_weight="balanced", random_state=42
    )
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Added average="weighted" because RiskLevel has 3 classes (low, mid, high)
    eval_metrics = {
        "Accuracy": accuracy_score(y_test, y_pred),
        "F1_Score": f1_score(y_test, y_pred, average="weighted", zero_division=0),
        "Precision": precision_score(
            y_test, y_pred, average="weighted", zero_division=0
        ),
        "Recall": recall_score(y_test, y_pred, average="weighted", zero_division=0),
    }
    classification = classification_report(y_test, y_pred, target_names=enc.classes_)

    model_dict = {"model": model, "le": enc}

    return eval_metrics, classification, model_dict


if __name__ == "__main__":
    df = load_data()
    eval_metrics, classification, model_dic = train(df)
    print("\nClassification Report:\n", classification)

    with open(metric_path, "w") as file:
        json.dump(eval_metrics, file, indent=4)
    print(f"Metrics saved to {metric_path}")

    with open(model_path, "wb") as file:
        pickle.dump(model_dic, file)
    print(f"Model saved to {model_path}")
