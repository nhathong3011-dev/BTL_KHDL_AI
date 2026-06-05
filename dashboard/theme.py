"""Giao dien dashboard tai chinh."""

COLORS = ["#0d3b66", "#c9a227", "#1a936f", "#c0392b", "#3d5a80", "#ee6c4d"]

PLOTLY = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,15,28,0.85)",
    font=dict(family="Segoe UI, sans-serif", color="#e8ecf1", size=12),
    margin=dict(l=48, r=32, t=56, b=48),
    colorway=COLORS,
)

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'IBM Plex Sans', sans-serif; }
.stApp {
    background: linear-gradient(160deg, #060a12 0%, #0c1424 50%, #101c32 100%);
}
[data-testid="stSidebar"] {
    background: #0a1220;
    border-right: 1px solid rgba(201,162,39,0.2);
}
.brand {
    padding: 1rem 0 1.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1rem;
}
.brand h2 { color: #d4af37; font-size: 1.1rem; margin: 0; font-weight: 700; }
.brand p { color: #6b7c93; font-size: 0.75rem; margin: 0.25rem 0 0; }
.hero {
    background: linear-gradient(120deg, rgba(13,59,102,0.95), rgba(16,28,50,0.98));
    border: 1px solid rgba(201,162,39,0.3);
    border-radius: 14px;
    padding: 1.75rem 2rem;
    margin-bottom: 1.5rem;
}
.hero h1 { color: #f5f7fa; font-size: 1.65rem; margin: 0 0 0.5rem; }
.hero p { color: #94a3b8; margin: 0; line-height: 1.55; font-size: 0.95rem; }
.kpi {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.1rem;
    text-align: center;
}
.kpi .val { font-size: 1.75rem; font-weight: 700; color: #d4af37; }
.kpi .lbl { font-size: 0.7rem; color: #8899ad; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi.risk .val { color: #e74c3c; }
.kpi.safe .val { color: #1a936f; }
.alert-ok {
    background: rgba(26,147,111,0.12);
    border: 1px solid rgba(26,147,111,0.45);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    color: #a8e6cf;
}
.alert-risk {
    background: rgba(192,57,43,0.12);
    border: 1px solid rgba(192,57,43,0.5);
    border-radius: 12px;
    padding: 1.25rem 1.5rem;
    color: #f5b7b1;
}
.stButton > button {
    background: linear-gradient(90deg, #0d3b66, #1a5080) !important;
    border: 1px solid rgba(201,162,39,0.45) !important;
    color: #fff !important;
    font-weight: 600 !important;
}
.login-panel {
    background: linear-gradient(145deg, rgba(13,59,102,0.5), rgba(10,18,32,0.95));
    border: 1px solid rgba(201,162,39,0.35);
    border-radius: 16px;
    padding: 2rem 1.75rem 1rem;
    margin-bottom: 1.25rem;
    text-align: center;
}
.login-panel h2 { color: #d4af37; margin: 0; font-size: 1.5rem; }
.login-panel .login-sub { color: #94a3b8; margin: 0.35rem 0 0; font-size: 0.9rem; }
.login-panel .login-hint { color: #6b7c93; font-size: 0.8rem; margin-top: 0.75rem; }
</style>
"""
