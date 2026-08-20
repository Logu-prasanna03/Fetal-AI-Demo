from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user, require_role
from app.models import Analysis, User
from app.schemas import PredictionRequest, StoredAnalysisResponse
from app.services.model_service import ModelService

router = APIRouter(prefix="/api/v1", tags=["Analyses"])
service = ModelService()
SAFETY_NOTICE = "Research/clinical decision-support prototype only. Not for diagnosis, treatment, or emergency use; a qualified clinician must independently review all information."


def serialize(analysis: Analysis) -> dict:
    return {
        "id": str(analysis.id),
        "patient_reference": analysis.patient_reference,
        "category": analysis.category,
        "confidence": analysis.confidence,
        "probabilities": analysis.probabilities,
        "model_version": analysis.model_version,
        "is_demo_model": analysis.is_demo_model,
        "explanation": "Model context is available in the model information endpoint. This is not a patient-specific clinical explanation.",
        "safety_notice": SAFETY_NOTICE,
        "created_at": analysis.created_at.replace(tzinfo=UTC),
    }


@router.get("/model-info")
def model_info() -> dict:
    return service.info()


@router.post("/analyses", response_model=StoredAnalysisResponse)
def create_analysis(payload: PredictionRequest, db: Session = Depends(get_db), user: User = Depends(require_role("patient"))) -> dict:
    result = service.predict(payload.measurements.model_dump())
    analysis = Analysis(
        patient_id=user.id,
        patient_reference=payload.patient_reference or f"Patient-{user.id}",
        category=result["category"], confidence=result["confidence"], probabilities=result["probabilities"],
        measurements=payload.measurements.model_dump(), model_version=result["model_version"], is_demo_model=result["is_demo_model"],
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)
    response = serialize(analysis)
    response["explanation"] = result["explanation"]
    return response


@router.get("/analyses/me", response_model=list[StoredAnalysisResponse])
def my_analyses(db: Session = Depends(get_db), user: User = Depends(require_role("patient"))) -> list[dict]:
    records = db.scalars(select(Analysis).where(Analysis.patient_id == user.id).order_by(Analysis.created_at.desc())).all()
    return [serialize(record) for record in records]


@router.get("/doctor/dashboard")
def doctor_dashboard(db: Session = Depends(get_db), user: User = Depends(require_role("doctor"))) -> dict:
    rows = db.execute(select(Analysis, User.full_name, User.email).join(User, User.id == Analysis.patient_id).order_by(Analysis.created_at.desc()).limit(100)).all()
    summaries = [{**serialize(analysis), "patient_name": name, "patient_email": email} for analysis, name, email in rows]
    return {
        "summary": {
            "total_patients": db.scalar(select(func.count()).select_from(User).where(User.role == "patient")) or 0,
            "total_analyses": db.scalar(select(func.count()).select_from(Analysis)) or 0,
            "pathological_reviews": db.scalar(select(func.count()).select_from(Analysis).where(Analysis.category == "Pathological")) or 0,
        },
        "analyses": summaries,
    }
