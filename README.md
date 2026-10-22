# Matria Care

> **Research and clinical decision-support prototype — not a medical device and not for diagnosis, treatment, or emergency use.**

Matria Care is a portfolio demonstration of a connected maternal-and-fetal care workspace. It combines a fictional care profile, simulated maternal–fetal monitoring, clinician oversight, and CTG-style machine-learning classification: **Normal**, **Suspect**, or **Pathological**. It pairs a React dashboard with a FastAPI service and a scikit-learn MLP classifier.

## Why this project

- Demonstrates an end-to-end ML product: preprocessing, model training, evaluation, inference, a human-facing UI, and a device-ready telemetry boundary.
- Keeps the model's role narrow: it supports review, never replaces a qualified clinician.
- Makes uncertainty visible through confidence, model provenance, and feature-level context.

## MVP architecture

```text
React + Tailwind dashboard  →  FastAPI API  →  scikit-learn pipeline (Scaler + MLP)
                                              ↳ PostgreSQL/SQLite demo records
                                              ↳ synthetic maternal–fetal telemetry
                                              ↳ future wearable / CTG adapter boundary
```

## Quick start

### Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The API starts with a clearly marked synthetic **demo** model so the UI is usable immediately. Replace it with a real, appropriately licensed research dataset before presenting results as real model performance:

```powershell
python ..\ml\train.py --data path\to\fetal_health.csv --output app\artifacts\fetal_mlp.joblib
```

Expected training CSV: the 21 CTG feature columns used in `backend/app/schemas.py`, plus `fetal_health` with values `1` (Normal), `2` (Suspect), and `3` (Pathological).

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open the displayed local URL. The frontend expects the API at `http://localhost:8000`; set `VITE_API_URL` to change it.

## API

- `GET /health` — service and model status
- `GET /api/v1/model-info` — provenance and global feature context
- `POST /api/v1/predictions` — prediction with confidence and safe-use notice
- `GET /api/v1/predictions` — recent local prediction history

## Roadmap

1. **MVP (included):** demo care profile, simulated monitoring, API, MLP pipeline, clinician dashboard, safe messaging, and prediction history.
2. **Data and persistence:** PostgreSQL, SQLAlchemy/Alembic, authenticated clinician roles, audit logs.
3. **ML quality:** held-out evaluation report, experiment tracking, calibration, drift monitoring, SHAP-based explanations.
4. **RAG (optional):** retrieve only from reviewed, versioned reference material and generate an educational explanation; never let an LLM produce the risk class.
5. **Portfolio polish:** demo video/screenshots, GitHub Actions, Docker Compose, deployed demo using synthetic data only.

## Responsible-use notes

- Never enter real patient-identifying information in this demo.
- Do not use this project to make clinical decisions.
- Validate independently with domain experts, governance, privacy controls, and appropriate regulatory review before any real-world use.

## Suggested LinkedIn project description

Built **Matria Care**, a maternal-and-fetal care portfolio demonstration using React, Tailwind CSS, FastAPI, PostgreSQL-ready persistence, and a scikit-learn MLP pipeline. The application includes a fictional care profile, simulated monitoring feed, a clinician dashboard, and CTG-style classification into Normal, Suspect, and Pathological categories. It is explicitly designed as a research prototype—not a diagnostic or clinical-record system.

