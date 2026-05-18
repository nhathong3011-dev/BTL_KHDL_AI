"""Cau hinh du an — duong dan, cot du lieu, nhan hien thi."""

from pathlib import Path

# Thu muc goc du an (BTL_KHDL_AI)
ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = ROOT / "data.xls"
ARTIFACTS_DIR = ROOT / "artifacts"
MODELS_FILE = ARTIFACTS_DIR / "models.joblib"
METRICS_FILE = ARTIFACTS_DIR / "metrics.json"
CHART_FILE = ARTIFACTS_DIR / "risk_distribution.png"

TARGET_COL = "default payment next month"
ID_COL = "ID"
RANDOM_STATE = 42
TEST_SIZE = 0.2

# Ten mo hinh hien thi tren dashboard
MODEL_NAMES = [
    "Logistic Regression",
    "Random Forest",
    "Gradient Boosting",
    "XGBoost",
]

FEATURE_LABELS = {
    "LIMIT_BAL": "Han muc tin dung",
    "SEX": "Gioi tinh",
    "EDUCATION": "Trinh do hoc van",
    "MARRIAGE": "Tinh trang hon nhan",
    "AGE": "Tuoi",
    "PAY_0": "Trang thai tra no (thang hien tai)",
    "PAY_2": "Trang thai tra no (T-2)",
    "PAY_3": "Trang thai tra no (T-3)",
    "PAY_4": "Trang thai tra no (T-4)",
    "PAY_5": "Trang thai tra no (T-5)",
    "PAY_6": "Trang thai tra no (T-6)",
    "BILL_AMT1": "Du no hoa don (T)",
    "BILL_AMT2": "Du no hoa don (T-2)",
    "BILL_AMT3": "Du no hoa don (T-3)",
    "BILL_AMT4": "Du no hoa don (T-4)",
    "BILL_AMT5": "Du no hoa don (T-5)",
    "BILL_AMT6": "Du no hoa don (T-6)",
    "PAY_AMT1": "So tien tra (T)",
    "PAY_AMT2": "So tien tra (T-2)",
    "PAY_AMT3": "So tien tra (T-3)",
    "PAY_AMT4": "So tien tra (T-4)",
    "PAY_AMT5": "So tien tra (T-5)",
    "PAY_AMT6": "So tien tra (T-6)",
}
