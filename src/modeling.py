"""Huan luyen, danh gia va luu mo hinh AML / Fraud."""

import json
from dataclasses import dataclass, asdict

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
)

from src.config import RANDOM_STATE, TEST_SIZE, MODEL_NAMES, MODELS_FILE, METRICS_FILE, ARTIFACTS_DIR
from src.dataset import load_dataset

try:
    from xgboost import XGBClassifier
    HAS_XGB = True
except ImportError:
    HAS_XGB = False


@dataclass
class ModelResult:
    name: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    roc_auc: float
    confusion_matrix: list
    roc_fpr: list
    roc_tpr: list
    feature_importance: dict


def _make_estimators() -> dict:
    """Khoi tao cac mo hinh trong pipeline co chuan hoa."""
    est = {
        "Logistic Regression": LogisticRegression(
            max_iter=1000, class_weight="balanced", solver="liblinear", random_state=RANDOM_STATE
        ),
        "Random Forest": RandomForestClassifier(
            n_estimators=150, max_depth=14, class_weight="balanced",
            random_state=RANDOM_STATE, n_jobs=-1,
        ),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=120, max_depth=5, learning_rate=0.08, random_state=RANDOM_STATE
        ),
    }
    if HAS_XGB:
        est["XGBoost"] = XGBClassifier(
            n_estimators=150, max_depth=6, learning_rate=0.08,
            eval_metric="logloss", random_state=RANDOM_STATE, n_jobs=-1,
        )
    return {k: est[k] for k in MODEL_NAMES if k in est}


def _importance(pipeline, feature_cols: list[str]) -> dict:
    model = pipeline.named_steps["clf"]
    if hasattr(model, "feature_importances_"):
        vals = model.feature_importances_
    elif hasattr(model, "coef_"):
        vals = np.abs(model.coef_).ravel()
    else:
        vals = np.zeros(len(feature_cols))
    pairs = sorted(zip(feature_cols, vals), key=lambda x: x[1], reverse=True)
    return {k: float(v) for k, v in pairs[:15]}


def train_all(test_size: float = TEST_SIZE) -> dict:
    """Huan luyen tat ca mo hinh, tra ve bundle luu file."""
    df, feature_cols, target_col = load_dataset()
    X = df[feature_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=RANDOM_STATE, stratify=y
    )

    pipelines = {}
    metrics = []

    for name, clf in _make_estimators().items():
        pipe = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", clf),
        ])
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)
        y_prob = pipe.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_prob)

        pipelines[name] = pipe
        metrics.append(ModelResult(
            name=name,
            accuracy=round(accuracy_score(y_test, y_pred), 4),
            precision=round(precision_score(y_test, y_pred, zero_division=0), 4),
            recall=round(recall_score(y_test, y_pred, zero_division=0), 4),
            f1=round(f1_score(y_test, y_pred, zero_division=0), 4),
            roc_auc=round(roc_auc_score(y_test, y_prob), 4),
            confusion_matrix=confusion_matrix(y_test, y_pred).tolist(),
            roc_fpr=fpr.tolist(),
            roc_tpr=tpr.tolist(),
            feature_importance=_importance(pipe, feature_cols),
        ))

    bundle = {
        "pipelines": pipelines,
        "feature_cols": feature_cols,
        "target_col": target_col,
        "medians": X.median().to_dict(),
        "test_size": test_size,
    }
    return {"bundle": bundle, "metrics": metrics, "df": df}


def save_artifacts(train_output: dict) -> None:
    """Luu mo hinh va bang metrics ra artifacts/."""
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(train_output["bundle"], MODELS_FILE)

    rows = [asdict(m) for m in train_output["metrics"]]
    METRICS_FILE.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")


def load_artifacts() -> dict | None:
    if not MODELS_FILE.exists():
        return None
    return joblib.load(MODELS_FILE)


def load_metrics() -> list[dict] | None:
    if not METRICS_FILE.exists():
        return None
    return json.loads(METRICS_FILE.read_text(encoding="utf-8"))


def predict_one(bundle: dict, model_name: str, features: dict) -> tuple[int, float, float]:
    """Du doan 1 ho so: (nhan, xac suat rui ro, xac suat an toan)."""
    pipe = bundle["pipelines"][model_name]
    cols = bundle["feature_cols"]
    row = pd.DataFrame([{c: features[c] for c in cols}])
    proba = pipe.predict_proba(row)[0]
    label = int(pipe.predict(row)[0])
    return label, float(proba[1]), float(proba[0])
