from fastapi import FastAPI, HTTPException

from backend.predictor import predictor
from backend.schemas import PatientVitals, Predictions

app = FastAPI(
    title="🩺 Maternal Health Risk Prediction API",
    description=(
        "A machine learning API powered by a Random Forest Classifier to predict "
        "maternal health risk levels (**Low Risk**, **Mid Risk**, and **High Risk**) "
        "based on vital signs and clinical indicators."
    ),
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "status": "online",
        "title": "Maternal Health Risk Prediction API",
        "message": "Welcome! Visit /docs to explore the interactive API documentation and test predictions.",
        "model_info": {
            "algorithm": "Random Forest Classifier",
            "target_classes": ["low risk", "mid risk", "high risk"],
        },
    }


@app.post("/predict", response_model=Predictions)
def predict_risk(vitals: PatientVitals) -> Predictions:
    try:
        return predictor(vitals)
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {exc}"
        ) from exc
