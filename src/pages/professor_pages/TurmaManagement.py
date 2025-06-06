import time
import streamlit as st
import pandas as pd
import os


CSV_DIR   = "data"
CSV_PATH  = os.path.join(CSV_DIR, "turmas.csv")


def _ensure_turmas_csv():
    os.makedirs(CSV_DIR, exist_ok=True)
    header = ["turma", "descricao"]
    if (not os.path.exists(CSV_PATH)) or (os.path.getsize(CSV_PATH) == 0):
        pd.DataFrame(columns=header).to_csv(CSV_PATH, index=False)
        return
    try:
        df0 = pd.read_csv(CSV_PATH, nrows=0)
        if set(df0.columns) != set(header):
            raise ValueError
    except Exception:
        pd.DataFrame(columns=header).to_csv(CSV_PATH, index=False)


def show_turma_management():
    _ensure_turmas_csv()

    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
    df = df.astype(str).apply(lambda col: col.str.strip())

    col1, col2 = st.columns([3,1])
    
    if "ProfessorHome" not in st.session_state:
        st.session_state.current_page = "ProfessorHome"

    with col2:
        if st.button("🔙 Voltar"):
            st.session_state.page = "ProfessorHome"
            
    st.title("Gerenciar Turmas")
    st.subheader("🏷️ Lista de Turmas")
    st.dataframe(df)

    with st.expander("Adicionar Turma"):
        with st.form(key="add_turma", clear_on_submit=True):
            turma = st.text_input("Turma")
            descricao = st.text_input("Descrição")
            if st.form_submit_button("Adicionar"):
                cod_str = turma.strip()
                desc_str = descricao.strip()
                if (not cod_str) or (not desc_str):
                    st.error("Preencha todos os campos")
                else:
                    df_atual = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
                    df_atual = df_atual.astype(str).apply(lambda col: col.str.strip())
                    if cod_str in df_atual["turma"].values:
                        st.error("Código já cadastrado")
                    else:
                        new_row = pd.DataFrame([{
                            "turma": cod_str,
                            "descricao": desc_str
                        }])
                        df_concat = pd.concat([df_atual, new_row], ignore_index=True)
                        df_concat.to_csv(CSV_PATH, index=False)
                        st.success("Turma adicionada com sucesso")
                        st.rerun()

    with st.expander("Remover Turma"):
        with st.form(key="remove_turma", clear_on_submit=True):
            options = df["turma"] + " - " + df["descricao"]
            to_remove = st.selectbox("Selecione a turma", options)
            confirm_removal = st.selectbox("Tem certeza que deseja remover esta Turma?", ["Não", "Sim"])
            if st.form_submit_button("Remover"):
                if confirm_removal == "Sim":
                    cod = to_remove.split(" - ")[0]
                    df_atual = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
                    df_atual = df_atual.astype(str).apply(lambda col: col.str.strip())
                    df2 = df_atual[df_atual["turma"] != cod]
                    df2.to_csv(CSV_PATH, index=False)
                    st.success("Turma removida com sucesso")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.info("Ação de remoção cancelada.")