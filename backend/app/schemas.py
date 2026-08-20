from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


FEATURES = [
    "baseline_value", "accelerations", "fetal_movement", "uterine_contractions",
    "light_decelerations", "severe_decelerations", "prolongued_decelerations",
    "abnormal_short_term_variability", "mean_value_of_short_term_variability",
    "percentage_of_time_with_abnormal_long_term_variability",
    "mean_value_of_long_term_variability", "histogram_width", "histogram_min",
    "histogram_max", "histogram_number_of_peaks", "histogram_number_of_zeroes",
    "histogram_mode", "histogram_mean", "histogram_median", "histogram_variance",
    "histogram_tendency",
]


class CTGMeasurements(BaseModel):
    """CTG-style inputs. Defaults support a non-clinical product demonstration only."""

    baseline_value: float = Field(130, ge=50, le=250)
    accelerations: float = Field(0.006, ge=0, le=1)
    fetal_movement: float = Field(0.0, ge=0, le=1)
    uterine_contractions: float = Field(0.004, ge=0, le=1)
    light_decelerations: float = Field(0.0, ge=0, le=1)
    severe_decelerations: float = Field(0.0, ge=0, le=1)
    prolongued_decelerations: float = Field(0.0, ge=0, le=1)
    abnormal_short_term_variability: float = Field(25, ge=0, le=100)
    mean_value_of_short_term_variability: float = Field(1.5, ge=0, le=20)
    percentage_of_time_with_abnormal_long_term_variability: float = Field(0, ge=0, le=100)
    mean_value_of_long_term_variability: float = Field(10, ge=0, le=100)
    histogram_width: float = Field(70, ge=0, le=300)
    histogram_min: float = Field(80, ge=0, le=250)
    histogram_max: float = Field(160, ge=0, le=300)
    histogram_number_of_peaks: float = Field(2, ge=0, le=50)
    histogram_number_of_zeroes: float = Field(0, ge=0, le=50)
    histogram_mode: float = Field(130, ge=0, le=250)
    histogram_mean: float = Field(125, ge=0, le=250)
    histogram_median: float = Field(128, ge=0, le=250)
    histogram_variance: float = Field(20, ge=0, le=1000)
    histogram_tendency: float = Field(0, ge=-1, le=1)


class PredictionRequest(BaseModel):
    patient_reference: str | None = Field(default=None, max_length=60, description="Non-identifying local reference only")
    measurements: CTGMeasurements


class PredictionResponse(BaseModel):
    id: str
    category: Literal["Normal", "Suspect", "Pathological"]
    confidence: float
    probabilities: dict[str, float]
    model_version: str
    is_demo_model: bool
    explanation: str
    safety_notice: str


class RegisterRequest(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: str = Field(min_length=5, max_length=255)
    password: str = Field(min_length=8, max_length=72)
    role: Literal["patient", "doctor"]


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: Literal["patient", "doctor"]


class AuthResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class StoredAnalysisResponse(PredictionResponse):
    created_at: datetime
    patient_reference: str
