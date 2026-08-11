from pathlib import Path
from typing import Any

import joblib


def predict_churn(features: dict[str, Any], model_path: Path) -> float:
    artifact = joblib.load(model_path)
    values = [[float(features[name]) for name in artifact["features"]]]
    return float(artifact["model"].predict_proba(values)[0][1])
