"""Xac thuc API key truoc khi vao dashboard."""

import hmac
import os
import tomllib
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
SECRETS_PATHS = [
    ROOT / ".streamlit" / "secrets.toml",
    Path(__file__).resolve().parent / ".streamlit" / "secrets.toml",
]

SESSION_AUTH = "aml_authenticated"


def _parse_toml_file(path: Path) -> list[str]:
    keys: list[str] = []
    with path.open("rb") as f:
        data = tomllib.load(f)
    if "key" in data:
        keys.append(str(data["key"]))
    if "api_key" in data:
        keys.append(str(data["api_key"]))
    auth = data.get("auth", {})
    if isinstance(auth, dict):
        for item in auth.get("api_keys", []):
            keys.append(str(item))
    return keys


def _load_valid_keys() -> list[str]:
    keys: list[str] = []

    for path in SECRETS_PATHS:
        if path.exists():
            keys.extend(_parse_toml_file(path))

    try:
        if "key" in st.secrets:
            keys.append(str(st.secrets["key"]))
        if "api_key" in st.secrets:
            keys.append(str(st.secrets["api_key"]))
        auth = st.secrets.get("auth", {})
        if isinstance(auth, dict):
            for item in auth.get("api_keys", []):
                keys.append(str(item))
    except Exception:
        pass

    env_key = os.environ.get("AML_API_KEY", "").strip()
    if env_key:
        keys.append(env_key)

    seen: set[str] = set()
    unique: list[str] = []
    for k in keys:
        k = k.strip()
        if k and k not in seen:
            seen.add(k)
            unique.append(k)
    return unique


def keys_configured() -> bool:
    return len(_load_valid_keys()) > 0


def verify_api_key(user_key: str) -> bool:
    user_key = (user_key or "").strip()
    if not user_key:
        return False
    for valid in _load_valid_keys():
        if hmac.compare_digest(user_key, valid):
            return True
    return False


def is_authenticated() -> bool:
    return bool(st.session_state.get(SESSION_AUTH))


def authenticate(user_key: str) -> bool:
    if verify_api_key(user_key):
        st.session_state[SESSION_AUTH] = True
        return True
    return False


def logout() -> None:
    st.session_state.pop(SESSION_AUTH, None)


def render_login_gate() -> None:
    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(
            """
            <div class="login-panel">
                <h2>FinGuard AML</h2>
                <p class="login-sub">He thong phan tich AML & Fraud Patterns</p>
                <p class="login-hint">Nhap key de tiep tuc</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not keys_configured():
            st.error(
                "Chua cau hinh key. Tao file:\n\n"
                f"`{ROOT / '.streamlit' / 'secrets.toml'}`"
            )
            st.stop()

        with st.form("login_form", clear_on_submit=False):
            user_key = st.text_input("Key", type="password", placeholder="Nhap key")
            submitted = st.form_submit_button("Dang nhap", use_container_width=True)

        if submitted:
            if authenticate(user_key):
                st.success("Dang nhap thanh cong.")
                st.rerun()
            else:
                st.error("Key khong hop le. Kiem tra hoa/thuong va khoang trang.")

        st.info("**Key mac dinh (local):** `FinGuard2026` — doi trong `.streamlit/secrets.toml`")
