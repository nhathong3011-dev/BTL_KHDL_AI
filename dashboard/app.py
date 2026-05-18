"""Web demo AML & Fraud Patterns."""

import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from dashboard.theme import CSS, COLORS, PLOTLY
from src.config import DATA_FILE, FEATURE_LABELS
from src.dataset import load_dataset, summary_stats
from src.modeling import load_artifacts, load_metrics, predict_one, train_all, save_artifacts

st.set_page_config(page_title="FinGuard AML", page_icon="🛡️", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def get_data():
    return load_dataset()


def ensure_models():
    bundle = load_artifacts()
    if bundle is None:
        with st.spinner("Dang huan luyen mo hinh (lan dau, ~1-2 phut)..."):
            save_artifacts(train_all())
        bundle = load_artifacts()
    return bundle


def read_upload(f):
    n = f.name.lower()
    if n.endswith(".csv"):
        return pd.read_csv(f)
    if n.endswith(".xls"):
        return pd.read_excel(f, engine="xlrd", header=1)
    return pd.read_excel(f, header=1)


# ----- Sidebar -----
with st.sidebar:
    st.markdown("## FinGuard AML")
    st.caption("Fraud Patterns & Credit Risk")
    page = st.radio("Menu", ["Tong quan", "Mo hinh AI", "Scoring ho so"])
    st.divider()
    st.caption("Nguon: UCI Credit Card Default")

try:
    df, feature_cols, target_col = get_data()
except Exception as e:
    st.error(f"Loi doc du lieu: {e}")
    st.info(f"Can file: {DATA_FILE}")
    st.stop()

stats = summary_stats(df, target_col)

st.markdown(
    """
    <div class="hero">
        <h1>Phan tich AML & Fraud Patterns</h1>
        <p>Scoring rui ro tin dung — 30.000 ho so, 4 mo hinh ML, dashboard danh cho bao cao BTL KHDL/AI.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ==================== TONG QUAN ====================
if page == "Tong quan":
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Tong ho so", f"{stats['total']:,}")
    m2.metric("Binh thuong", f"{stats['safe']:,}")
    m3.metric("Rui ro / Default", f"{stats['risk']:,}")
    m4.metric("Ty le rui ro", f"{stats['risk_rate']}%")

    left, right = st.columns(2)
    with left:
        fig = px.pie(
            names=["Binh thuong", "Rui ro"],
            values=[stats["safe"], stats["risk"]],
            title="Phan bo nhan muc tieu",
            color_discrete_sequence=[COLORS[2], COLORS[3]],
            hole=0.45,
        )
        fig.update_layout(**PLOTLY)
        st.plotly_chart(fig, use_container_width=True)
    with right:
        fig2 = px.histogram(
            df, x="LIMIT_BAL", color=target_col,
            barmode="overlay", opacity=0.7,
            title="Phan phoi han muc theo nhan",
            color_discrete_map={0: COLORS[2], 1: COLORS[3]},
        )
        fig2.update_layout(**PLOTLY)
        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Thong ke mo ta")
    desc = df[feature_cols].describe().T
    desc.index = [FEATURE_LABELS.get(i, i) for i in desc.index]
    st.dataframe(desc.style.background_gradient(cmap="Blues", axis=0), use_container_width=True)

    st.subheader("Ma tran tuong quan")
    corr = df[feature_cols].corr()
    fig_c = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="RdBu_r")
    fig_c.update_layout(**PLOTLY, height=500)
    st.plotly_chart(fig_c, use_container_width=True)

# ==================== MO HINH AI ====================
elif page == "Mo hinh AI":
    metrics = load_metrics()
    if metrics is None:
        if st.button("Huan luyen mo hinh ngay"):
            with st.spinner("Dang huan luyen..."):
                save_artifacts(train_all())
            st.rerun()
        st.warning("Chua co mo hinh. Bam nut tren hoac chay: `python train.py`")
        st.stop()

    bundle = ensure_models()
    df_m = pd.DataFrame(metrics).set_index("name")
    st.dataframe(df_m[["accuracy", "precision", "recall", "f1", "roc_auc"]], use_container_width=True)

    best = df_m["roc_auc"].idxmax()
    st.success(f"Mo hinh tot nhat (ROC-AUC): **{best}** — {df_m.loc[best, 'roc_auc']:.4f}")

    melted = df_m.reset_index()[["name", "accuracy", "precision", "recall", "f1", "roc_auc"]].melt(
        id_vars="name", var_name="Chi so", value_name="Gia tri"
    )
    fig_b = px.bar(melted, x="name", y="Gia tri", color="Chi so", barmode="group", title="So sanh mo hinh")
    fig_b.update_layout(**PLOTLY)
    st.plotly_chart(fig_b, use_container_width=True)

    st.subheader("Duong cong ROC")
    fig_roc = go.Figure()
    for row in metrics:
        fig_roc.add_trace(go.Scatter(
            x=row["roc_fpr"], y=row["roc_tpr"], mode="lines",
            name=f"{row['name']} (AUC={row['roc_auc']:.3f})",
        ))
    fig_roc.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Ngau nhien", line=dict(dash="dash")))
    fig_roc.update_layout(xaxis_title="FPR", yaxis_title="TPR", title="ROC Curve", **PLOTLY)
    st.plotly_chart(fig_roc, use_container_width=True)

    st.subheader("Confusion matrix")
    ncols = min(len(metrics), 4)
    cols = st.columns(ncols)
    for col, row in zip(cols, metrics):
        with col:
            cm = row["confusion_matrix"]
            fig_cm = px.imshow(cm, text_auto=True, color_continuous_scale="Reds", title=row["name"])
            fig_cm.update_layout(**PLOTLY, height=300)
            st.plotly_chart(fig_cm, use_container_width=True)

    st.subheader("Feature importance (Top 10)")
    imp_rows = []
    for row in metrics:
        for feat, val in list(row["feature_importance"].items())[:10]:
            imp_rows.append({"Mo hinh": row["name"], "Dac trung": FEATURE_LABELS.get(feat, feat), "Quan trong": val})
    imp_df = pd.DataFrame(imp_rows)
    fig_i = px.bar(imp_df, x="Quan trong", y="Dac trung", color="Mo hinh", orientation="h", height=500)
    fig_i.update_layout(**PLOTLY)
    st.plotly_chart(fig_i, use_container_width=True)

    if st.button("Huan luyen lai mo hinh"):
        with st.spinner("Dang cap nhat..."):
            save_artifacts(train_all())
        st.cache_data.clear()
        st.rerun()

# ==================== SCORING ====================
else:
    bundle = ensure_models()
    metrics = load_metrics() or []
    model_names = list(bundle["pipelines"].keys())
    default_model = max(metrics, key=lambda x: x["roc_auc"])["name"] if metrics else model_names[0]

    tab1, tab2 = st.tabs(["Nhap thu cong", "Phan tich hang loat"])

    with tab1:
        with st.form("score_form"):
            inputs = {}
            cols = st.columns(3)
            for i, col in enumerate(feature_cols):
                lbl = FEATURE_LABELS.get(col, col)
                with cols[i % 3]:
                    inputs[col] = st.number_input(lbl, value=float(bundle["medians"][col]), step=1.0)
            model_name = st.selectbox("Mo hinh", model_names, index=model_names.index(default_model))
            go_btn = st.form_submit_button("Phan tich rui ro")

        if go_btn:
            label, p_risk, p_safe = predict_one(bundle, model_name, inputs)
            if label == 0:
                st.markdown(
                    f'<div class="alert-ok"><h3>Ho so binh thuong</h3>'
                    f'<p>Xac suat rui ro: {p_risk*100:.1f}%</p></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="alert-risk"><h3>Canh bao rui ro cao</h3>'
                    f'<p>Xac suat vo no / gian lan: {p_risk*100:.1f}% — de xuat ra soat AML.</p></div>',
                    unsafe_allow_html=True,
                )

            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=p_risk * 100,
                title={"text": "Diem rui ro (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#c0392b" if label else "#1a936f"},
                    "steps": [
                        {"range": [0, 30], "color": "rgba(26,147,111,0.25)"},
                        {"range": [30, 70], "color": "rgba(201,162,39,0.25)"},
                        {"range": [70, 100], "color": "rgba(192,57,43,0.25)"},
                    ],
                },
            ))
            gauge.update_layout(**PLOTLY, height=280)
            st.plotly_chart(gauge, use_container_width=True)

    with tab2:
        up = st.file_uploader("File CSV / XLS / XLSX", type=["csv", "xls", "xlsx"])
        mname = st.selectbox("Mo hinh quet", model_names, key="batch_m")
        if st.button("Quet hang loat"):
            if up is None:
                st.warning("Hay upload file.")
            else:
                batch = read_upload(up)
                miss = [c for c in feature_cols if c not in batch.columns]
                if miss:
                    st.error(f"Thieu cot: {miss}")
                else:
                    pipe = bundle["pipelines"][mname]
                    Xb = batch[feature_cols]
                    pred = pipe.predict(Xb)
                    prob = pipe.predict_proba(Xb)[:, 1]
                    batch["Ket_luan"] = ["Binh thuong" if p == 0 else "Rui ro cao" for p in pred]
                    batch["Xac_suat_rui_ro_%"] = (prob * 100).round(2)
                    st.metric("Rui ro cao", int((pred == 1).sum()))
                    st.dataframe(batch.head(20), use_container_width=True)
                    buf = io.BytesIO()
                    batch.to_excel(buf, index=False, engine="openpyxl")
                    buf.seek(0)
                    st.download_button("Tai ket qua Excel", buf, "ket_qua_scoring.xlsx")
