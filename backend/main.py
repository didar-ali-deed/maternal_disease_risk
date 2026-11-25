from fastapi import FastAPI

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
