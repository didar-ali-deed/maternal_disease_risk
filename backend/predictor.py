import pandas as pd

from backend.load_model import load
from backend.schemas import PatientVitals, Predictions

MODEL_VERSION = "v1.0.0"


def predictor(patient_vitals: PatientVitals) -> Predictions:

    # Load trained model and label encoder
    model, le = load()

    # Convert validated input into DataFrame
    input_df = pd.DataFrame([patient_vitals.model_dump()])

    # Generate prediction
    raw_prediction = model.predict(input_df)

    # Convert encoded prediction into original label
    risk_level = le.inverse_transform(raw_prediction)[0]

    # Return validated response
    return Predictions(risk_level=str(risk_level))
