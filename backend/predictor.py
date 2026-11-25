import pandas as pd

from backend.load_model import load
from backend.schemas import PatientVitals, Predictions

MODEL_VERSION = "v1.0.0"


def predictor(patient_vitals: PatientVitals) -> Predictions:
    model, le = load()

    input_df = pd.DataFrame([patient_vitals.model_dump()])

    raw_pred = model.predict(input_df)
    raw_item = raw_pred[0]

    try:
        pred_code: int | None = int(raw_item)
    except (ValueError, TypeError):
        pred_code = None

    risk_level = (
        str(le.inverse_transform(raw_pred)[0]) if le is not None else str(raw_item)
    )

    probabilities: dict[str, float] | None = None
    confidence: float | None = None

    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)[0]
        class_labels = (
            [str(c) for c in le.classes_]
            if le is not None
            else [str(c) for c in model.classes_]
        )
        probabilities = {
            cls: round(float(prob), 4) for cls, prob in zip(class_labels, probs)
        }
        confidence = round(float(max(probs)), 4)

    return Predictions(
        risk_level=risk_level,
        confidence=confidence,
        probabilities=probabilities,
        risk_code=pred_code,
        model_version=MODEL_VERSION,
    )
