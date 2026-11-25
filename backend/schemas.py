from typing import Annotated

from pydantic import BaseModel, Field, model_validator


class PatientVitals(BaseModel):
    Age: Annotated[
        int,
        Field(..., description="Patient age in years", examples=[28], gt=0, lt=120),
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
        float,
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

    @model_validator(mode="after")
    def validate_bp_order(self) -> "PatientVitals":
        if self.SystolicBP <= self.DiastolicBP:
            raise ValueError("SystolicBP must be greater than DiastolicBP")
        return self


class Predictions(BaseModel):
    risk_level: str = Field(
        ..., description="Predicted patient risk category", examples=["high risk"]
    )
    confidence: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Probability of the predicted class",
        examples=[0.87],
    )
    probabilities: dict[str, float] | None = Field(
        default=None,
        description="Class probability distribution across all risk levels",
        examples=[{"low risk": 0.03, "mid risk": 0.10, "high risk": 0.87}],
    )
    risk_code: int | None = Field(
        default=None,
        description="Encoded integer class label if applicable",
        examples=[2],
    )
    model_version: str | None = Field(
        default=None,
        description="Identifier or version of the model artifact used",
        examples=["v1.0.0"],
    )
