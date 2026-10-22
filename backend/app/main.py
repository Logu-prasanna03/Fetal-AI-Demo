from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import CORS_ORIGINS
from app.core.database import Base, engine
from app.routes import analyses, auth, monitoring, profiles
from app.routes.analyses import service

app = FastAPI(title="Matria Care API", version="0.3.1", description="Maternal and fetal care portfolio demo; not for diagnosis or emergency use.")
app.add_middleware(CORSMiddleware, allow_origins=CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
Base.metadata.create_all(bind=engine)


@app.on_event("startup")
def create_database_tables() -> None:
    Base.metadata.create_all(bind=engine)


app.include_router(auth.router)
app.include_router(analyses.router)
app.include_router(monitoring.router)
app.include_router(profiles.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_version": service.model.version, "is_demo_model": service.model.is_demo}


@app.get("/")
def root() -> dict:
    return {"service": "Matria Care API", "docs": "/docs", "health": "/health"}
