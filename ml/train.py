"""Train FetalAI from a licensed research CSV; never train on identifiable patient data."""
from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import sys
sys.path.insert(0, str(Path(__file__).parents[1] / "backend"))
from app.schemas import FEATURES  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True, help="CSV with the documented CTG features and fetal_health label")
    parser.add_argument("--output", default="../backend/app/artifacts/fetal_mlp.joblib")
    args = parser.parse_args()

    frame = pd.read_csv(args.data)
    required = set(FEATURES + ["fetal_health"])
    missing = required.difference(frame.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")
    X, y = frame[FEATURES], frame["fetal_health"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
    pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", MLPClassifier(hidden_layer_sizes=(64, 32), early_stopping=True, max_iter=1000, random_state=42))])
    pipeline.fit(X_train, y_train)
    importance = permutation_importance(pipeline, X_test, y_test, n_repeats=10, random_state=42)
    ordered = sorted(zip(FEATURES, importance.importances_mean), key=lambda item: item[1], reverse=True)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"pipeline": pipeline, "feature_importance": ordered, "version": "trained-mlp-v1"}, output)
    print(f"Saved model to {output}. Hold-out accuracy: {pipeline.score(X_test, y_test):.3f}")


if __name__ == "__main__":
    main()
