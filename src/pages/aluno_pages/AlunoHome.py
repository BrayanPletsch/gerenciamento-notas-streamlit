import streamlit as st
import pandas as pd
import os

from src.pages.InfoPage import show_info
from src.utils.Auth import logout

ALUNOS_CSV = os.path.join("data", "alunos.csv")
NOTAS_CSV = os.path.join("data", "notas.csv")
DISCIPLINAS_CSV = os.path.join("data", "disciplinas.csv")

def show_aluno_home():
    if "current_page" not in st.session_state:
        st.session_state.current_page = "AlunoHome"

    st.set_page_config(page_title="Área do Aluno", page_icon="🎓", layout="wide")

    st.sidebar.title(f"Bem-vindo, {st.session_state.current_user}!")
    st.sidebar.divider()
    
    if st.sidebar.button("Home", use_container_width=True):
        st.session_state.current_page = "AlunoHome"
    if st.sidebar.button("Informações do Projeto", use_container_width=True):
        st.session_state.current_page = "InfoPage"
    st.sidebar.divider()
    if st.sidebar.button("Sair", use_container_width=True):
        logout()

    page = st.session_state.current_page

    if page == "AlunoHome":
        current_user = st.session_state.get("current_user", "")
        st.title("Área do Aluno")
        st.write(f"Olá, **{current_user}**!")

        df_alunos = pd.read_csv(ALUNOS_CSV, dtype=str, keep_default_na=False)
        df_alunos = df_alunos.astype(str).apply(lambda c: c.str.strip())
        aluno_row = df_alunos[df_alunos["matricula"] == current_user]
        if not aluno_row.empty:
            nome  = aluno_row.iloc[0]["nome"]
            turma = aluno_row.iloc[0]["turma"]
            st.subheader(f"Nome: {nome}")
            st.subheader(f"Turma: {turma}")
        else:
            st.info("Dados do aluno não encontrados.")

        st.write("---")
        st.subheader("Minhas Disciplinas e Notas")

        df_notas = pd.read_csv(NOTAS_CSV, dtype=str, keep_default_na=False)
        df_notas = df_notas.astype(str).apply(lambda c: c.str.strip())
        df_meu  = df_notas[df_notas["matricula"] == current_user]

        if not df_meu.empty:
            df_meu = df_meu.merge(
                pd.read_csv(DISCIPLINAS_CSV, dtype=str, keep_default_na=False)
                .astype(str).apply(lambda c: c.str.strip()),
                on="disciplina", how="left"
            )
            st.dataframe(df_meu[["disciplina", "nota"]].rename(columns={
                "disciplina": "Disciplina",
                "nota": "Nota"
            }))
        else:
            st.info("Nenhuma nota registrada.")
        st.write("---")
        st.caption("Sistema de Gerenciamento de Notas Escolares  •  Versão Acadêmica")

    elif page == "InfoPage":
        show_info()
