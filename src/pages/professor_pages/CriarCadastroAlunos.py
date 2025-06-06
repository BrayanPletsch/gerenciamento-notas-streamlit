import streamlit as st
import pandas as pd
import os

USERS_CSV  = os.path.join("data", "users.csv")
ALUNOS_CSV = os.path.join("data", "alunos.csv")

def _ensure_users_csv():
    header = ["username", "password", "user_type"]
    os.makedirs(os.path.dirname(USERS_CSV), exist_ok=True)
    if (not os.path.exists(USERS_CSV)) or (os.path.getsize(USERS_CSV) == 0):
        pd.DataFrame(columns=header).to_csv(USERS_CSV, index=False)
        return
    try:
        df0 = pd.read_csv(USERS_CSV, nrows=0)
        if set(df0.columns) != set(header):
            raise ValueError
    except Exception:
        pd.DataFrame(columns=header).to_csv(USERS_CSV, index=False)

def _ensure_alunos_csv():
    os.makedirs(os.path.dirname(ALUNOS_CSV), exist_ok=True)
    header = ["matricula", "nome", "turma"]
    if (not os.path.exists(ALUNOS_CSV)) or (os.path.getsize(ALUNOS_CSV) == 0):
        pd.DataFrame(columns=header).to_csv(ALUNOS_CSV, index=False)

def show_criar_cadastro_alunos():
    _ensure_users_csv()
    _ensure_alunos_csv()

    alunos_df = pd.read_csv(ALUNOS_CSV, dtype=str, keep_default_na=False)
    alunos_df = alunos_df.astype(str).apply(lambda col: col.str.strip())

    usuarios_df = pd.read_csv(USERS_CSV, dtype=str, keep_default_na=False)
    usuarios_df = usuarios_df.astype(str).apply(lambda col: col.str.strip())

    st.title("Criar Cadastro de Alunos")
    st.subheader("Selecione o registro de aluno existente")

    # Se não houver nenhum aluno cadastrado, exibir mensagem e sair
    if alunos_df.empty:
        st.warning("Nenhum aluno registrado. Cadastre alunos em 'Gerenciar Alunos' primeiro.")
        return

    options = alunos_df["matricula"] + " - " + alunos_df["nome"]
    selecionado = st.selectbox("Alunos existentes", options)

    # Caso a seleção retorne None, mostre aviso e pare
    if not selecionado:
        st.warning("Selecione um aluno para continuar.")
        return

    # Proteção extra com try/except ao fazer split, caso algo inesperado ocorra
    try:
        matricula = selecionado.split(" - ")[0]
    except Exception:
        st.error("Formato do registro de aluno inválido.")
        return

    st.write("### Informe o username e a senha para este aluno")
    with st.form(key="cadastro_aluno_form", clear_on_submit=True):
        username_input = st.text_input("Username para o aluno", placeholder="Ex.: joao123")
        password_input = st.text_input("Senha para o aluno", type="password")
        submit = st.form_submit_button("Criar cadastro")

    if submit:
        if not username_input.strip() or not password_input.strip():
            st.error("Preencha username e senha.")
            return

        usuarios_df = pd.read_csv(USERS_CSV, dtype=str, keep_default_na=False)
        usuarios_df = usuarios_df.astype(str).apply(lambda col: col.str.strip())

        if username_input.strip() in usuarios_df["username"].values:
            st.error("Este username já está em uso. Escolha outro.")
            return

        if matricula in usuarios_df["username"].values:
            st.info("Este aluno já possui cadastro.")
            return

        new_user = pd.DataFrame([{
            "username": username_input.strip(),
            "password": password_input.strip(),
            "user_type": "aluno"
        }])
        updated = pd.concat([usuarios_df, new_user], ignore_index=True)
        updated.to_csv(USERS_CSV, index=False)

        st.success(f"Cadastro de aluno '{username_input.strip()}' criado com sucesso!")
        if hasattr(st, "rerun"):
            st.rerun()
        else:
            st.rerun()
