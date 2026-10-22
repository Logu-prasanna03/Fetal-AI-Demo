from datetime import UTC

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models import CareProfile, User
from app.schemas import CareProfileRequest, CareProfileResponse

router = APIRouter(prefix="/api/v1/care-profile", tags=["Care profile"])


def serialize(profile: CareProfile) -> dict:
    return {
        "id": str(profile.id),
        "pregnancy_week": profile.pregnancy_week,
        "care_stage": profile.care_stage,
        "preferred_contact": profile.preferred_contact,
        "updated_at": profile.updated_at.replace(tzinfo=UTC),
    }


@router.get("/me", response_model=CareProfileResponse | None)
def my_profile(db: Session = Depends(get_db), patient: User = Depends(require_role("patient"))) -> dict | None:
    profile = db.scalar(select(CareProfile).where(CareProfile.patient_id == patient.id))
    return serialize(profile) if profile else None


@router.put("/me", response_model=CareProfileResponse)
def save_profile(payload: CareProfileRequest, db: Session = Depends(get_db), patient: User = Depends(require_role("patient"))) -> dict:
    profile = db.scalar(select(CareProfile).where(CareProfile.patient_id == patient.id))
    if not profile:
        profile = CareProfile(patient_id=patient.id, **payload.model_dump())
        db.add(profile)
    else:
        for key, value in payload.model_dump().items():
            setattr(profile, key, value)
    db.commit()
    db.refresh(profile)
    return serialize(profile)
