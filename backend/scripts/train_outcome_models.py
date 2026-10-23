from __future__ import annotations

import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.ml.features import CATEGORICAL_FEATURES, NUMERIC_FEATURES, make_training_frame

DATA_DIR = ROOT / "data"
ARTIFACT_DIR = ROOT / "app" / "ml" / "artifacts"


def build_preprocessor() -> ColumnTransformer:
    return ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("numeric", StandardScaler(), NUMERIC_FEATURES),
        ]
    )


def candidate_models() -> dict[str, object]:
    models: dict[str, object] = {
        "random_forest": RandomForestClassifier(
            n_estimators=250,
            max_depth=10,
            min_samples_leaf=4,
            class_weight="balanced",
            random_state=42,
        ),
        "gradient_boosting_xgboost_style": GradientBoostingClassifier(
            n_estimators=180,
            learning_rate=0.045,
            max_depth=3,
            random_state=42,
        ),
    }

    try:
        from xgboost import XGBClassifier

        models["xgboost"] = XGBClassifier(
            n_estimators=220,
            max_depth=3,
            learning_rate=0.045,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="logloss",
            random_state=42,
        )
    except ImportError:
        pass

    return models


def evaluate_model(name: str, pipeline: Pipeline, x_test: pd.DataFrame, y_test: pd.Series) -> dict[str, float | str]:
    predictions = pipeline.predict(x_test)
    probabilities = pipeline.predict_proba(x_test)[:, 1]
    return {
        "model_name": name,
        "accuracy": round(float(accuracy_score(y_test, predictions)), 4),
        "f1": round(float(f1_score(y_test, predictions)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probabilities)), 4),
    }


def main() -> None:
    medicines = pd.read_csv(DATA_DIR / "medicines.csv")
    cases = pd.read_csv(DATA_DIR / "treatment_cases.csv")
    features, target = make_training_frame(cases, medicines)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.25,
        stratify=target,
        random_state=42,
    )

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, float | str]] = []
    trained_payloads: dict[str, dict[str, object]] = {}

    for name, estimator in candidate_models().items():
        pipeline = Pipeline(
            steps=[
                ("preprocessor", build_preprocessor()),
                ("model", estimator),
            ]
        )
        pipeline.fit(x_train, y_train)
        metrics = evaluate_model(name, pipeline, x_test, y_test)
        results.append(metrics)
        trained_payloads[name] = {
            "pipeline": pipeline,
            "model_name": name,
            "metrics": metrics,
            "features": {
                "categorical": CATEGORICAL_FEATURES,
                "numeric": NUMERIC_FEATURES,
            },
        }
        joblib.dump(trained_payloads[name], ARTIFACT_DIR / f"{name}.joblib")

    best_metrics = max(results, key=lambda item: (float(item["roc_auc"]), float(item["f1"])))
    best_name = str(best_metrics["model_name"])
    joblib.dump(trained_payloads[best_name], ARTIFACT_DIR / "best_outcome_model.joblib")

    with (ARTIFACT_DIR / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump({"best_model": best_name, "results": results}, file, indent=2)

    print(json.dumps({"best_model": best_name, "results": results}, indent=2))


if __name__ == "__main__":
    main()

