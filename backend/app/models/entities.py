from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Analysis(Base):
    __tablename__ = "analyses"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    patient_reference: Mapped[str] = mapped_column(String(60), default="")
    category: Mapped[str] = mapped_column(String(30), index=True)
    confidence: Mapped[float]
    probabilities: Mapped[dict] = mapped_column(JSON)
    measurements: Mapped[dict] = mapped_column(JSON)
    model_version: Mapped[str] = mapped_column(String(100))
    is_demo_model: Mapped[bool]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class CareProfile(Base):
    """Non-identifying demo care summary. Do not store real patient records in this project."""

    __tablename__ = "care_profiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    pregnancy_week: Mapped[int | None] = mapped_column(nullable=True)
    care_stage: Mapped[str] = mapped_column(String(80), default="Demo care plan")
    preferred_contact: Mapped[str] = mapped_column(String(80), default="In-app demo only")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class MonitoringReading(Base):
    """Vendor-neutral telemetry record for the future device-adapter layer."""

    __tablename__ = "monitoring_readings"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    source: Mapped[str] = mapped_column(String(30), index=True)
    observed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    maternal_heart_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    systolic_bp: Mapped[float | None] = mapped_column(Float, nullable=True)
    diastolic_bp: Mapped[float | None] = mapped_column(Float, nullable=True)
    oxygen_saturation: Mapped[float | None] = mapped_column(Float, nullable=True)
    fetal_heart_rate: Mapped[float | None] = mapped_column(Float, nullable=True)
    uterine_activity: Mapped[float | None] = mapped_column(Float, nullable=True)
    data_quality: Mapped[str] = mapped_column(String(20), default="unknown")
    is_simulated: Mapped[bool] = mapped_column(Boolean, default=True)
    raw_payload: Mapped[dict] = mapped_column(JSON, default=dict)
