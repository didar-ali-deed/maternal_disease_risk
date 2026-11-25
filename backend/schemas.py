from typing import Annotated, Literal

from pydantic import BaseModel, Field, model_validator


class PatientVitals(BaseModel):
    Age: Annotated[
        int,
        Field(
            description="Patient age in years",
            examples=[28],
            gt=0,
            lt=120,
        ),
    ]

    SystolicBP: Annotated[
        int,
        Field(
            description="Resting systolic blood pressure in mmHg",
            examples=[120],
            gt=30,
            lt=300,
        ),
    ]

    DiastolicBP: Annotated[
        int,
        Field(
            description="Resting diastolic blood pressure in mmHg",
            examples=[80],
            gt=20,
            lt=200,
        ),
    ]

    BS: Annotated[
        float,
        Field(
            description="Blood glucose concentration in mmol/L",
            examples=[5.5],
            gt=1.0,
            lt=35.0,
        ),
    ]

    BodyTemp: Annotated[
        float,
        Field(
            description="Body temperature in Fahrenheit",
            examples=[98.6],
            gt=85.0,
            lt=110.0,
        ),
    ]

    HeartRate: Annotated[
        int,
        Field(
            description="Resting heart rate in bpm",
            examples=[72],
            gt=25,
            lt=250,
        ),
    ]

    @model_validator(mode="after")
    def validate_bp_order(self):
        if self.SystolicBP <= self.DiastolicBP:
            raise ValueError("SystolicBP must be greater than DiastolicBP")

        return self


class Predictions(BaseModel):
    risk_level: Literal[
        "low risk",
        "mid risk",
        "high risk",
    ] = Field(
        ...,
        description="Predicted patient risk category",
        examples=["high risk"],
    )
