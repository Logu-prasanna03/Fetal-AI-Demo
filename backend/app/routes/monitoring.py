from datetime import UTC, datetime
from math import sin

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models import MonitoringReading, User
from app.schemas import MonitoringReadingRequest, MonitoringReadingResponse

router = APIRouter(prefix="/api/v1/monitoring", tags=["Monitoring"])


def serialize(reading: MonitoringReading) -> dict:
    return {
        "id": str(reading.id), "source": reading.source, "observed_at": reading.observed_at.replace(tzinfo=UTC),
        "maternal_heart_rate": reading.maternal_heart_rate, "systolic_bp": reading.systolic_bp,
        "diastolic_bp": reading.diastolic_bp, "oxygen_saturation": reading.oxygen_saturation,
        "fetal_heart_rate": reading.fetal_heart_rate, "uterine_activity": reading.uterine_activity,
        "data_quality": reading.data_quality, "is_simulated": reading.is_simulated, "raw_payload": reading.raw_payload,
    }


@router.get("/demo-live")
def demo_live(patient: User = Depends(require_role("patient"))) -> dict:
    """A visibly synthetic stream for UI development; it must never drive clinical action."""
    now = datetime.now(UTC)
    wave = sin(now.timestamp() / 8)
    return {
        "is_simulated": True,
        "generated_at": now,
        "status": "demo_stream_active",
        "message": "Simulated measurements only. This feed has no clinical meaning.",
        "reading": {
            "maternal_heart_rate": round(74 + wave * 4, 0),
            "systolic_bp": round(112 + wave * 3, 0),
            "diastolic_bp": round(72 + wave * 2, 0),
            "oxygen_saturation": round(98 + wave * 0.4, 0),
            "fetal_heart_rate": round(142 + wave * 7, 0),
            "uterine_activity": round(14 + max(wave, 0) * 9, 0),
            "data_quality": "good",
        },
    }


@router.post("/readings", response_model=MonitoringReadingResponse)
def ingest_reading(payload: MonitoringReadingRequest, db: Session = Depends(get_db), patient: User = Depends(require_role("patient"))) -> dict:
    """Future adapter entry point. Authentication and vendor validation must be added per device vendor."""
    reading = MonitoringReading(patient_id=patient.id, observed_at=payload.observed_at or datetime.utcnow(), is_simulated=payload.source == "simulator", **payload.model_dump(exclude={"observed_at"}))
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return serialize(reading)


@router.get("/me", response_model=list[MonitoringReadingResponse])
def my_readings(db: Session = Depends(get_db), patient: User = Depends(require_role("patient"))) -> list[dict]:
    records = db.scalars(select(MonitoringReading).where(MonitoringReading.patient_id == patient.id).order_by(MonitoringReading.observed_at.desc()).limit(100)).all()
    return [serialize(record) for record in records]
