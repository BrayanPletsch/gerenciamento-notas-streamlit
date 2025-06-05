import streamlit as st
import pandas as pd
import os


CSV_PATH = os.path.join("data", "users.csv")


def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "user_type" not in st.session_state:
        st.session_state.user_type = None
    if "current_user" not in st.session_state:
        st.session_state.current_user = None


def check_auth() -> bool:
    return st.session_state.logged_in


def _ensure_csv_header(csv_path: str):
    header = ["username", "password", "user_type"]
    if not os.path.exists(csv_path) or os.path.getsize(csv_path) == 0:
        pd.DataFrame(columns=header).to_csv(csv_path, index=False)
        return
    try:
        df0 = pd.read_csv(csv_path, nrows=0)
        if set(header) != set(df0.columns):
            raise ValueError
    except Exception:
        pd.DataFrame(columns=header).to_csv(csv_path, index=False)


def login_user_from_csv(username: str, password: str, csv_path: str = CSV_PATH) -> bool:
    _ensure_csv_header(csv_path)
    try:
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    except Exception as e:
        st.error(f"Erro ao ler users.csv: {e}")
        return False
    df = df.astype(str).apply(lambda col: col.str.strip())
    user_in, pass_in = username.strip(), password.strip()
    match = df.query("username == @user_in and password == @pass_in")
    if not match.empty:
        st.session_state.logged_in = True
        st.session_state.current_user = user_in
        st.session_state.user_type = match.iloc[0]["user_type"]
        return True
    return False


def register_professor(username: str, password: str, csv_path: str = CSV_PATH) -> bool:
    _ensure_csv_header(csv_path)
    try:
        df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    except Exception as e:
        st.error(f"Erro ao ler users.csv: {e}")
        return False
    df["username"] = df["username"].str.strip()
    user_in = username.strip()
    if user_in in df["username"].values:
        st.error("Já existe um usuário com esse nome. Tente outro.")
        return False
    new_row = pd.DataFrame([{
        "username": user_in,
        "password": password.strip(),
        "user_type": "professor"
    }])
    pd.concat([df, new_row], ignore_index=True).to_csv(csv_path, index=False)
    return True


def logout():
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.current_user = None
    if hasattr(st, "rerun"):
        st.rerun()
    else:
        st.stop()