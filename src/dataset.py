"""Doc va tien xu ly bo du lieu UCI Credit Card Default."""

import pandas as pd
import numpy as np

from src.config import DATA_FILE, TARGET_COL, ID_COL


def load_raw(path=None) -> pd.DataFrame:
    """Doc file Excel UCI (header o dong 2)."""
    path = path or DATA_FILE
    if not path.exists():
        raise FileNotFoundError(f"Khong tim thay du lieu: {path}")

    df = pd.read_excel(path, engine="xlrd", header=1)
    if TARGET_COL not in df.columns:
        raise ValueError(f"Thieu cot muc tieu '{TARGET_COL}'")
    return df


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Lay cot so lam dac trung, bo ID va nhan."""
    numeric = df.select_dtypes(include=[np.number]).columns.tolist()
    features = [c for c in numeric if c not in (TARGET_COL, ID_COL)]
    clean = df[[TARGET_COL] + features].dropna().copy()
    clean[TARGET_COL] = clean[TARGET_COL].astype(int)
    return clean, features


def load_dataset(path=None) -> tuple[pd.DataFrame, list[str], str]:
    """Ham chinh: tra ve DataFrame, danh sach feature, ten cot target."""
    raw = load_raw(path)
    return *prepare_features(raw), TARGET_COL


def summary_stats(df: pd.DataFrame, target_col: str) -> dict:
    """Thong ke tong quan cho dashboard."""
    counts = df[target_col].value_counts().sort_index()
    total = len(df)
    risk = int(counts.get(1, 0))
    safe = int(counts.get(0, 0))
    return {
        "total": total,
        "safe": safe,
        "risk": risk,
        "risk_rate": round(risk / total * 100, 2) if total else 0,
        "features": len([c for c in df.columns if c != target_col]),
    }
