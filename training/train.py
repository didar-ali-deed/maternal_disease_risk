
import json
import pickle
from pathlib import Path

from .load_data import load_data
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import (
    StratifiedKFold,
    cross_validate,
    train_test_split,
)
from sklearn.preprocessing import LabelEncoder

root_path = Path(__file__).resolve().parent.parent
model_dir = root_path / "models"
model_dir.mkdir(parents=True, exist_ok=True)

model_path = model_dir / "model.pkl"
metric_path = model_dir / "metrics.json"


def train(df: DataFrame):
    X = df.drop(columns="RiskLevel")
    y = df["RiskLevel"]

    enc = LabelEncoder()
    y = enc.fit_transform(y)

    class_labels = list(range(len(enc.classes_)))
    class_names = enc.classes_.tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    print("Training shape:", X_train.shape)
    print("Testing shape:", X_test.shape)

    model = RandomForestClassifier(
        n_estimators=600,
        max_depth=20,
        n_jobs=-1,
        class_weight="balanced",
        random_state=42,
    )

    # Cross-validation on training data only
    cv = StratifiedKFold(
        n_splits=5,
        shuffle=True,
        random_state=42,
    )

    scoring = {
        "accuracy": "accuracy",
        "precision_macro": "precision_macro",
        "recall_macro": "recall_macro",
        "f1_macro": "f1_macro",
    }

    cv_results = cross_validate(
        model,
        X_train,
        y_train,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
    )

    cv_metrics = {}

    for metric in scoring:
        scores = cv_results[f"test_{metric}"]

        cv_metrics[metric] = {
            "mean": float(scores.mean()),
            "std": float(scores.std()),
        }

    # Fit final model on complete training partition
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    # Aggregate holdout metrics
    holdout_metrics = {
        "Accuracy": float(accuracy_score(y_test, y_pred)),
        "Precision_Weighted": float(
            precision_score(y_test, y_pred, average="weighted", zero_division=0)
        ),
        "Recall_Weighted": float(
            recall_score(y_test, y_pred, average="weighted", zero_division=0)
        ),
        "F1_Weighted": float(
            f1_score(y_test, y_pred, average="weighted", zero_division=0)
        ),
        "F1_Macro": float(
            f1_score(y_test, y_pred, average="macro", zero_division=0)
        ),
        "Recall_Macro": float(
            recall_score(y_test, y_pred, average="macro", zero_division=0)
        ),
    }

    # Class-wise metrics
    class_report = classification_report(
        y_test,
        y_pred,
        labels=class_labels,
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    # Raw confusion matrix
    matrix = confusion_matrix(
        y_test,
        y_pred,
        labels=class_labels,
    )

    # Normalized confusion matrix: each row sums to 1
    normalized_matrix = confusion_matrix(
        y_test,
        y_pred,
        labels=class_labels,
        normalize="true",
    )

    metrics = {
        "dataset": {
            "total_samples": int(len(df)),
            "training_samples": int(len(X_train)),
            "testing_samples": int(len(X_test)),
            "features": X.columns.tolist(),
            "classes": class_names,
        },
        "cross_validation": {
            "folds": 5,
            "scoring": cv_metrics,
        },
        "holdout_test": holdout_metrics,
        "classification_report": class_report,
        "confusion_matrix": {
            "labels": class_names,
            "counts": matrix.tolist(),
            "normalized": normalized_matrix.tolist(),
        },
    }

    model_dict = {
        "model": model,
        "LabelEnc": enc,
    }

    return metrics, model_dict


if __name__ == "__main__":
    df = load_data()

    metrics, model_dict = train(df)

    with open(metric_path, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=4)

    with open(model_path, "wb") as file:
        pickle.dump(model_dict, file)

    print("\nCross-validation results:")
    print(json.dumps(metrics["cross_validation"], indent=4))

    print("\nHoldout test results:")
    print(json.dumps(metrics["holdout_test"], indent=4))

    print("\nClassification report:")
    for class_name, values in metrics["classification_report"].items():
        if isinstance(values, dict) and "precision" in values:
            print(
                f"{class_name}: "
                f"Precision={values['precision']:.3f}, "
                f"Recall={values['recall']:.3f}, "
                f"F1={values['f1-score']:.3f}"
            )

    print("\nConfusion matrix:")
    print(metrics["confusion_matrix"]["counts"])

    print(f"\nMetrics saved: {metric_path}")
    print(f"Model saved: {model_path}")
