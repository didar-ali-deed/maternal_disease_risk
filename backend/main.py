import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.predictor import predictor
from backend.schemas import PatientVitals, Predictions

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(
    title="Maternal Health Risk Prediction API",
    description=(
        "A machine learning API powered by a Random Forest Classifier "
        "to predict maternal health risk levels (Low Risk, Mid Risk, "
        "and High Risk) based on vital signs and clinical indicators."
    ),
    version="1.0.0",
)
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


@app.get("/")
def home():
    return {
        "status": "online",
        "title": "Maternal Health Risk Prediction API",
        "message": "Welcome! Visit /docs to explore the API.",
        "model_info": {
            "algorithm": "Random Forest Classifier",
            "target_classes": [
                "low risk",
                "mid risk",
                "high risk",
            ],
        },
    }


@app.post("/predict", response_model=Predictions)
def predict_risk(vitals: PatientVitals) -> Predictions:
    
    try:
        return predictor(vitals)

    except Exception as exc:
        logger.exception("Maternal health prediction failed")

        raise HTTPException(
            status_code=500,
            detail="Prediction failed. Check server logs for details.",
        ) from exc


@app.get("/app", include_in_schema=False)
def serve_frontend():
    return FileResponse(FRONTEND_DIR / "index.html")
