import argparse
from pathlib import Path

import joblib
import pandas as pd

from ml.training.churn_model import build_model

FEATURES = ["transaction_count", "total_spend", "average_order_value", "campaign_engagements", "support_case_count"]


def train(dataset: Path, output: Path) -> float:
    frame = pd.read_csv(dataset)
    missing = set(FEATURES + ["churned"]) - set(frame.columns)
    if missing:
        raise ValueError(f"dataset missing columns: {sorted(missing)}")
    model = build_model()
    model.fit(frame[FEATURES], frame["churned"])
    output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump({"model": model, "features": FEATURES}, output)
    return float(model.score(frame[FEATURES], frame["churned"]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--output", type=Path, default=Path("ml/models/churn_model.joblib"))
    args = parser.parse_args()
    print(f"training accuracy={train(args.dataset, args.output):.3f}")
