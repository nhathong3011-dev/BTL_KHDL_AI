# AML & Fraud Patterns — BTL KHDL/AI

Phan tich rui ro tin dung va phat hien patterns gian lan tren bo du lieu
[UCI — Default of Credit Card Clients](https://archive.ics.uci.edu/ml/datasets/default+of+credit+card+clients).

## Cau truc du an (thiet ke moi)

```
BTL_KHDL_AI/
├── data.xls              # Du lieu UCI (30.000 mau)
├── train.py              # Buoc 1: huan luyen & luu mo hinh
├── run.bat               # Buoc 2: mo web demo (Windows)
├── environment.yml       # Moi truong Anaconda
├── src/
│   ├── config.py         # Cau hinh duong dan, nhan feature
│   ├── dataset.py        # Doc & tien xu ly Excel
│   └── modeling.py       # Pipeline ML + luu artifacts
├── dashboard/
│   ├── app.py            # Web demo Streamlit
│   └── theme.py          # Giao dien tai chinh
└── artifacts/            # Tao sau khi chay train.py
    ├── models.joblib
    ├── metrics.json
    └── risk_distribution.png
```

## Cai dat (Anaconda)

```bash
cd BTL_KHDL_AI
conda env create -f environment.yml
conda activate fraud-aml-demo
```

## Chay du an

**Buoc 1 — Huan luyen:**

```bash
python train.py
```

**Buoc 2 — Web demo:**

```bash
streamlit run dashboard/app.py
```

Hoac double-click `run.bat` (tu dong train neu chua co mo hinh).

## Mo hinh

| Mo hinh | Mo ta |
|---------|--------|
| Logistic Regression | Baseline, giai thich duoc |
| Random Forest | Ensemble cay |
| Gradient Boosting | Boosting sklearn |
| XGBoost | Gradient boosting toi uu |

Moi mo hinh dung `StandardScaler` + classifier, danh gia Accuracy, Precision, Recall, F1, ROC-AUC.

## Dashboard

1. **Tong quan** — KPI, bieu do, tuong quan
2. **Mo hinh AI** — bang metrics, ROC, confusion matrix, feature importance
3. **Scoring ho so** — nhap tay / upload hang loat, xuat Excel
