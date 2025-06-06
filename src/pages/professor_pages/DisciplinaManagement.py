import time
import streamlit as st
import pandas as pd
import os

CSV_DIR   = "data"
CSV_PATH  = os.path.join(CSV_DIR, "disciplinas.csv")

def _ensure_disciplinas_csv():
    os.makedirs(CSV_DIR, exist_ok=True)
    header = ["codigo", "nome_disciplina"]
    if (not os.path.exists(CSV_PATH)) or (os.path.getsize(CSV_PATH) == 0):
        pd.DataFrame(columns=header).to_csv(CSV_PATH, index=False)
        return
    try:
        df0 = pd.read_csv(CSV_PATH, nrows=0)
        if set(df0.columns) != set(header):
            raise ValueError
    except Exception:
        pd.DataFrame(columns=header).to_csv(CSV_PATH, index=False)

def show_disciplina_management():
    _ensure_disciplinas_csv()

    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
    df = df.astype(str).apply(lambda col: col.str.strip())

    col1, col2 = st.columns([3,1])
    
    if "ProfessorHome" not in st.session_state:
        st.session_state.current_page = "ProfessorHome"

    with col2:
        if st.button("🔙 Voltar"):
            st.session_state.page = "ProfessorHome"
    
    st.title("Gerenciar Disciplinas")
    st.subheader("📚 Lista de Disciplinas")
    st.dataframe(df)

    with st.expander("Adicionar Disciplina"):
        with st.form(key="add_disciplina", clear_on_submit=True):
            codigo         = st.text_input("Código da Disciplina")
            nome_disciplina = st.text_input("Nome da Disciplina")
            if st.form_submit_button("Adicionar"):
                cod_str  = codigo.strip()
                nome_str = nome_disciplina.strip()
                if (not cod_str) or (not nome_str):
                    st.error("Preencha todos os campos")
                else:
                    df_atual = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
                    df_atual = df_atual.astype(str).apply(lambda col: col.str.strip())
                    if cod_str in df_atual["codigo"].values:
                        st.error("Código já cadastrado")
                    else:
                        new_row = pd.DataFrame([{
                            "codigo": cod_str,
                            "nome_disciplina": nome_str
                        }])
                        df_concat = pd.concat([df_atual, new_row], ignore_index=True)
                        df_concat.to_csv(CSV_PATH, index=False)
                        st.success("Disciplina adicionada com sucesso")
                        st.rerun()

    with st.expander("Remover Disciplina"):
        with st.form(key="remove_disciplina", clear_on_submit=True):
            options   = df["codigo"] + " - " + df["nome_disciplina"]
            to_remove = st.selectbox("Selecione a disciplina", options)
            confirm_removal = st.selectbox("Tem certeza que deseja remover esta disciplina?", ["Não", "Sim"])
            if st.form_submit_button("Remover"):
                if confirm_removal == "Sim":
                    cod = to_remove.split(" - ")[0]
                    df_atual = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
                    df_atual = df_atual.astype(str).apply(lambda col: col.str.strip())
                    df2 = df_atual[df_atual["codigo"] != cod]
                    df2.to_csv(CSV_PATH, index=False)
                    st.success("Disciplina removida com sucesso")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.info("Ação de remoção cancelada.")