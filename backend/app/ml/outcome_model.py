from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import pandas as pd

from app.ml.features import make_prediction_frame
from app.schemas.clinical import ClinicalProfile


MODEL_DIR = Path(__file__).resolve().parent / "artifacts"
DEFAULT_MODEL_PATH = MODEL_DIR / "best_outcome_model.joblib"


@dataclass
class OutcomePredictionModel:
    pipeline: object
    model_name: str
    metrics: dict[str, float | str]

    @classmethod
    def load(cls, path: Path = DEFAULT_MODEL_PATH) -> "OutcomePredictionModel | None":
        if not path.exists():
            return None
        payload = joblib.load(path)
        return cls(
            pipeline=payload["pipeline"],
            model_name=payload["model_name"],
            metrics=payload.get("metrics", {}),
        )

    def predict_success_probability(self, profile: ClinicalProfile, medicine: pd.Series) -> float:
        frame = make_prediction_frame(profile, medicine)
        if hasattr(self.pipeline, "predict_proba"):
            probability = self.pipeline.predict_proba(frame)[0][1]
        else:
            probability = self.pipeline.predict(frame)[0]
        return float(max(0.0, min(1.0, probability)))

