import time
import streamlit as st
import pandas as pd
import os


CSV_DIR = "data"
ALUNOS_CSV_PATH = os.path.join(CSV_DIR, "alunos.csv")
TURMAS_CSV_PATH = os.path.join(CSV_DIR, "turmas.csv")


def _ensure_csv_files():
    os.makedirs(CSV_DIR, exist_ok=True)
    alunos_header = ["matricula", "nome", "turma"]
    turmas_header = ["turma"]
    
    if not os.path.exists(ALUNOS_CSV_PATH) or os.path.getsize(ALUNOS_CSV_PATH) == 0:
        pd.DataFrame(columns=alunos_header).to_csv(ALUNOS_CSV_PATH, index=False)
    
    if not os.path.exists(TURMAS_CSV_PATH) or os.path.getsize(TURMAS_CSV_PATH) == 0:
        pd.DataFrame(columns=turmas_header).to_csv(TURMAS_CSV_PATH, index=False)


def show_aluno_management():
    _ensure_csv_files()

    alunos_df = pd.read_csv(ALUNOS_CSV_PATH, dtype=str, keep_default_na=False)
    alunos_df = alunos_df.apply(lambda col: col.str.strip())
    turmas_df = pd.read_csv(TURMAS_CSV_PATH, dtype=str, keep_default_na=False)
    turmas_df = turmas_df.apply(lambda col: col.str.strip())

    col1, col2 = st.columns([3,1])
    
    if "ProfessorHome" not in st.session_state:
        st.session_state.current_page = "ProfessorHome"

    with col2:
        if st.button("🔙 Voltar"):
            st.session_state.page = "ProfessorHome"

    st.title("Gerenciar Alunos")
    st.subheader("👥 Lista de Alunos")
    st.dataframe(alunos_df)


    with st.expander("Adicionar Aluno"):
        with st.form(key="add_aluno", clear_on_submit=True):
            matricula = st.number_input("Matrícula do Aluno", min_value=1, step=1)
            nome = st.text_input("Nome Completo")
            turmas = turmas_df["turma"].dropna().unique().tolist()
            turma = st.selectbox("Turma", options=["Selecione..."] + turmas)
            if st.form_submit_button("Adicionar"):
                mat_str = str(int(matricula))
                if not nome.strip() or turma == "Selecione...":
                    st.error("Preencha todos os campos")
                else:
                    if mat_str in alunos_df["matricula"].values:
                        st.error("Matrícula já cadastrada")
                    else:
                        new_row = pd.DataFrame([{
                            "matricula": mat_str,
                            "nome": nome.strip(),
                            "turma": turma
                        }])
                        alunos_df = pd.concat([alunos_df, new_row], ignore_index=True)
                        alunos_df.to_csv(ALUNOS_CSV_PATH, index=False)
                        st.success("Aluno adicionado com sucesso")
                        st.rerun()

    with st.expander("Remover Aluno"):
        with st.form(key="remove_aluno", clear_on_submit=True):
            options = alunos_df["matricula"] + " - " + alunos_df["nome"]
            to_remove = st.selectbox("Selecione o aluno", options)
            confirm_removal = st.selectbox("Tem certeza que deseja remover este aluno?", ["Não", "Sim"])
            if st.form_submit_button("Remover"):
                if confirm_removal == "Sim":
                    mat = to_remove.split(" - ")[0]
                    alunos_df = alunos_df[alunos_df["matricula"] != mat]
                    alunos_df.to_csv(ALUNOS_CSV_PATH, index=False)
                    st.success(f"Aluno {to_remove} removido com sucesso")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.info("Ação de remoção cancelada.")
