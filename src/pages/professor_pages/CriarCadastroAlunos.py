from pathlib import Path
import time

import pandas as pd
import streamlit as st


DATA_DIR = Path("data")
USERS_CSV = DATA_DIR / "users.csv"
ALUNOS_CSV = DATA_DIR / "alunos.csv"

USERS_HEADER = ["id","username","password","user_type","name"]
ALUNOS_HEADER = ["user_id","matricula","nome","turma"]


def ensure_csv(path: Path, header: list):
    DATA_DIR.mkdir(exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        pd.DataFrame(columns=header).to_csv(path, index=False)
    else:
        cols = pd.read_csv(path, nrows=0).columns.tolist()
        if set(cols) != set(header):
            pd.DataFrame(columns=header).to_csv(path, index=False)


def load_df(path: Path, header: list) -> pd.DataFrame:
    ensure_csv(path, header)
    return pd.read_csv(path, dtype=str, keep_default_na=False).map(lambda x: x.strip())


def save_df(df: pd.DataFrame, path: Path):
    df.to_csv(path, index=False)


def show_criar_cadastro_alunos():
    alunos_df = load_df(ALUNOS_CSV, ALUNOS_HEADER)
    usuarios_df = load_df(USERS_CSV, USERS_HEADER)

    st.title("Criar Cadastro de Aluno")
    if alunos_df.empty:
        st.warning("Nenhum aluno cadastrado. Cadastre alunos em 'Gerenciar Alunos'.")
        return

    options = alunos_df.apply(lambda r: f"{r.matricula} – {r.nome}", axis=1).tolist()
    selecionado = st.selectbox("Selecione o aluno", ["Selecione..."] + options)
    if selecionado == "Selecione...":
        return

    user_id, nome_aluno = selecionado.split(" – ")

    if user_id in usuarios_df["id"].tolist():
        st.info("Este aluno já possui cadastro no sistema.")
        return

    with st.form("form_cadastro_aluno", clear_on_submit=True):
        username = st.text_input("Username", placeholder="Ex.: joaosalva")
        password = st.text_input("Senha", type="password")
        if st.form_submit_button("Criar cadastro"):
            username = username.strip()
            password = password.strip()
            if not username or not password:
                st.error("Preencha username e senha.")
                return
            if username in usuarios_df["username"].tolist():
                st.error("Este username já está em uso.")
                return

            new_row = pd.DataFrame([{  
                "id": user_id,
                "username": username,
                "password": password,
                "user_type": "aluno",
                "name": nome_aluno
            }])
            updated = pd.concat([usuarios_df, new_row], ignore_index=True)
            save_df(updated, USERS_CSV)
            st.success(f"Cadastro criado para aluno {nome_aluno} (ID: {user_id})!")
            time.sleep(1.5)
            st.rerun()