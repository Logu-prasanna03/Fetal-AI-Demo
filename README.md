# FetalAI

> **Research and clinical decision-support prototype — not a medical device and not for diagnosis, treatment, or emergency use.**

FetalAI is a portfolio project that turns fetal cardiotocography-style measurements into an interpretable machine-learning risk classification: **Normal**, **Suspect**, or **Pathological**. It pairs a React clinician dashboard with a FastAPI prediction service and a scikit-learn MLP classifier.

## Why this project

- Demonstrates an end-to-end ML product: preprocessing, model training, evaluation, inference, and a human-facing UI.
- Keeps the model's role narrow: it supports review, never replaces a qualified clinician.
- Makes uncertainty visible through confidence, model provenance, and feature-level context.

## MVP architecture

```text
React + Tailwind dashboard  →  FastAPI API  →  scikit-learn pipeline (Scaler + MLP)
                                              ↳ prediction history (in-memory for MVP)
                                              ↳ global feature importance
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

1. **MVP (included):** API, MLP pipeline, clinician dashboard, safe messaging, prediction history.
2. **Data and persistence:** PostgreSQL, SQLAlchemy/Alembic, authenticated clinician roles, audit logs.
3. **ML quality:** held-out evaluation report, experiment tracking, calibration, drift monitoring, SHAP-based explanations.
4. **RAG (optional):** retrieve only from reviewed, versioned reference material and generate an educational explanation; never let an LLM produce the risk class.
5. **Portfolio polish:** demo video/screenshots, GitHub Actions, Docker Compose, deployed demo using synthetic data only.

## Responsible-use notes

- Never enter real patient-identifying information in this demo.
- Do not use this project to make clinical decisions.
- Validate independently with domain experts, governance, privacy controls, and appropriate regulatory review before any real-world use.

## Suggested LinkedIn project description

Built **FetalAI**, an end-to-end fetal-health clinical decision-support prototype using React, Tailwind CSS, FastAPI, and a scikit-learn MLP pipeline. The application classifies CTG-style measurements into Normal, Suspect, and Pathological categories, exposes prediction confidence and feature context, and is explicitly designed as a research prototype—not a diagnostic tool.

