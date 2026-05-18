#!/usr/bin/env python
"""
Buoc 1 — Huan luyen mo hinh (chay truoc khi mo dashboard).

    conda activate fraud-aml-demo
    python train.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from src.config import CHART_FILE, ARTIFACTS_DIR
from src.dataset import load_dataset, summary_stats
from src.modeling import train_all, save_artifacts


def plot_distribution(df, target_col, out_path):
    stats = summary_stats(df, target_col)
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.pie(
        [stats["safe"], stats["risk"]],
        labels=["Binh thuong", "Rui ro / Default"],
        colors=["#1a936f", "#c0392b"],
        autopct="%1.1f%%",
        startangle=90,
        explode=(0, 0.06),
    )
    ax.set_title("Phan bo rui ro tin dung — UCI Dataset")
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)


def main():
    print("=" * 60)
    print("  AML & FRAUD PATTERNS — HUAN LUYEN MO HINH")
    print("=" * 60)

    df, _, target_col = load_dataset()
    stats = summary_stats(df, target_col)
    print(f"\nDu lieu: {stats['total']:,} ho so | Rui ro: {stats['risk']:,} ({stats['risk_rate']}%)")

    print("\nDang huan luyen...")
    out = train_all()
    save_artifacts(out)

    ARTIFACTS_DIR.mkdir(exist_ok=True)
    plot_distribution(out["df"], target_col, CHART_FILE)

    print("\n--- KET QUA ---")
    print(f"{'Mo hinh':<24} {'Acc':>7} {'Prec':>7} {'Rec':>7} {'F1':>7} {'AUC':>7}")
    print("-" * 60)
    for m in out["metrics"]:
        print(
            f"{m.name:<24} {m.accuracy:>7.4f} {m.precision:>7.4f} "
            f"{m.recall:>7.4f} {m.f1:>7.4f} {m.roc_auc:>7.4f}"
        )

    best = max(out["metrics"], key=lambda x: x.roc_auc)
    print(f"\nMo hinh tot nhat (ROC-AUC): {best.name}")
    print(f"Da luu: artifacts/models.joblib")
    print(f"Chay web: streamlit run dashboard/app.py")


if __name__ == "__main__":
    main()
