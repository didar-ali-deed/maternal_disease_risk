from typing import Annotated

from pydantic import BaseModel, Field


class PatientVitals(BaseModel):
    Age: Annotated[
        int, Field(..., description="Patient Age", examples=[80], gt=0, lt=120)
    ]
    SystolicBP: Annotated[
        int,
        Field(
            ...,
            description="Resting systolic blood pressure in mmHg",
            examples=[120],
            gt=30,
            lt=300,
        ),
    ]
    DiastolicBP: Annotated[
        int,
        Field(
            ...,
            description="Resting diastolic blood pressure in mmHg",
            examples=[80],
            gt=20,
            lt=200,
        ),
    ]
    BS: Annotated[
        int,
        Field(
            ...,
            description="Blood glucose concentration in mmol/L",
            examples=[5.5],
            gt=1.0,
            lt=35.0,
        ),
    ]
    BodyTemp: Annotated[
        float,
        Field(
            ...,
            description="Body temperature in degrees Fahrenheit (°F)",
            examples=[98.6],
            gt=85.0,
            lt=110.0,
        ),
    ]
    HeartRate: Annotated[
        int,
        Field(
            ...,
            description="Resting heart rate in beats per minute (bpm)",
            examples=[72],
            gt=25,
            lt=250,
        ),
    ]


class Predictions(BaseModel):
    prediction: str
