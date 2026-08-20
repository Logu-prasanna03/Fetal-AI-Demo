from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from app.schemas import FEATURES

LABELS = {1: "Normal", 2: "Suspect", 3: "Pathological"}
ARTIFACT_PATH = Path(__file__).parents[1] / "artifacts" / "fetal_mlp.joblib"


@dataclass
class LoadedModel:
    pipeline: Pipeline
    feature_importance: list[tuple[str, float]]
    version: str
    is_demo: bool


def _demo_model() -> LoadedModel:
    """Create a reproducible synthetic-only model so the portfolio UI can run locally."""
    rng = np.random.default_rng(42)
    n_rows = 720
    frame = pd.DataFrame({feature: rng.normal(0, 1, n_rows) for feature in FEATURES})
    # Deliberately synthetic labels: they do not encode clinical rules or real-world evidence.
    score = 1.2 * frame["abnormal_short_term_variability"] - 0.9 * frame["accelerations"] + rng.normal(0, 0.9, n_rows)
    labels = np.where(score < -0.45, 1, np.where(score < 0.65, 2, 3))
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", MLPClassifier(hidden_layer_sizes=(24, 12), max_iter=500, random_state=42)),
    ])
    pipeline.fit(frame, labels)
    importance = permutation_importance(pipeline, frame, labels, n_repeats=5, random_state=42)
    ordered = sorted(zip(FEATURES, importance.importances_mean), key=lambda item: item[1], reverse=True)
    return LoadedModel(pipeline, ordered, "demo-synthetic-v1", True)


def load_model() -> LoadedModel:
    if ARTIFACT_PATH.exists():
        saved = joblib.load(ARTIFACT_PATH)
        return LoadedModel(saved["pipeline"], saved["feature_importance"], saved.get("version", "trained-v1"), False)
    return _demo_model()


class ModelService:
    def __init__(self) -> None:
        self.model = load_model()

    def predict(self, values: dict[str, float]) -> dict:
        frame = pd.DataFrame([{feature: values[feature] for feature in FEATURES}])
        probabilities = self.model.pipeline.predict_proba(frame)[0]
        classes = self.model.pipeline.named_steps["classifier"].classes_
        mapped = {LABELS[int(label)]: round(float(probability), 4) for label, probability in zip(classes, probabilities)}
        label = LABELS[int(classes[int(np.argmax(probabilities))])]
        top_features = ", ".join(feature.replace("_", " ") for feature, _ in self.model.feature_importance[:3])
        return {
            "category": label,
            "confidence": round(float(np.max(probabilities)), 4),
            "probabilities": mapped,
            "model_version": self.model.version,
            "is_demo_model": self.model.is_demo,
            "explanation": f"Model context: the most influential global features in this model are {top_features}. This is not a patient-specific clinical explanation.",
        }

    def info(self) -> dict:
        return {
            "model_version": self.model.version,
            "is_demo_model": self.model.is_demo,
            "features": FEATURES,
            "global_feature_context": [
                {"feature": name, "importance": round(float(value), 4)}
                for name, value in self.model.feature_importance[:8]
            ],
        }

