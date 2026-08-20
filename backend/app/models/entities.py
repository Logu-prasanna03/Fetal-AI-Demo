from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, JSON, String
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
