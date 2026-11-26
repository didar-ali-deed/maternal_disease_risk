import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from backend.predictor import predictor
from backend.schemas import PatientVitals, Predictions

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
INDEX_FILE = FRONTEND_DIR / "index.html"

if not INDEX_FILE.is_file():
    raise RuntimeError(f"Frontend not found: {INDEX_FILE}")

# 0 = never cache (development). Set to 3600 in production and
# bump the ?v= number in index.html whenever you change CSS/JS.
STATIC_CACHE_SECONDS = 0

app = FastAPI(
    title="Maternal Health Risk Prediction API",
    description=(
        "A machine learning API powered by a Random Forest Classifier "
        "to predict maternal health risk levels (Low Risk, Mid Risk, "
        "and High Risk) based on vital signs and clinical indicators."
    ),
    version="1.0.0",
)

app.add_middleware(GZipMiddleware, minimum_size=500)


@app.middleware("http")
async def add_cache_headers(request: Request, call_next):
    response = await call_next(request)
    path = request.url.path
    if path.startswith("/static/") and response.status_code == 200:
        if STATIC_CACHE_SECONDS > 0:
            response.headers["Cache-Control"] = (
                f"public, max-age={STATIC_CACHE_SECONDS}"
            )
        else:
            response.headers["Cache-Control"] = "no-store"
    elif path == "/app":
        response.headers["Cache-Control"] = "no-store"
    return response


app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def home():
    return {
        "status": "online",
        "title": "Maternal Health Risk Prediction API",
        "message": "Welcome! Visit /docs to explore the API or /app for the UI.",
        "model_info": {
            "algorithm": "Random Forest Classifier",
            "target_classes": ["low risk", "mid risk", "high risk"],
        },
    }


@app.get("/health", include_in_schema=False)
def health():
    return {"status": "ok"}


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
    return FileResponse(INDEX_FILE)
