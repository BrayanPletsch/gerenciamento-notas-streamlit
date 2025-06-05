import streamlit as st
import pandas as pd
import os

CSV_DIR  = "data"
CSV_PATH = os.path.join(CSV_DIR, "alunos.csv")

def _ensure_alunos_csv():
    os.makedirs(CSV_DIR, exist_ok=True)
    header = ["matricula", "nome", "turma"]
    if (not os.path.exists(CSV_PATH)) or (os.path.getsize(CSV_PATH) == 0):
        pd.DataFrame(columns=header).to_csv(CSV_PATH, index=False)
        return
    try:
        df0 = pd.read_csv(CSV_PATH, nrows=0)
        if set(df0.columns) != set(header):
            raise ValueError
    except Exception:
        pd.DataFrame(columns=header).to_csv(CSV_PATH, index=False)

def show_aluno_management():
    _ensure_alunos_csv()

    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
    df = df.astype(str).apply(lambda col: col.str.strip())
    st.title("Gerenciar Alunos")
    st.subheader("Lista de Alunos")
    st.dataframe(df)

    with st.expander("Adicionar Aluno"):
        with st.form(key="add_aluno", clear_on_submit=True):
            matricula = st.number_input("Matrícula do Aluno", min_value=1, step=1)
            nome      = st.text_input("Nome Completo")
            turma     = st.text_input("Turma")
            if st.form_submit_button("Adicionar"):
                mat_str = str(int(matricula))
                if (not mat_str) or (not nome.strip()) or (not turma.strip()):
                    st.error("Preencha todos os campos")
                else:
                    # Recarrega o CSV para evitar dados desatualizados
                    df_atual = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
                    df_atual = df_atual.astype(str).apply(lambda col: col.str.strip())

                    if mat_str in df_atual["matricula"].values:
                        st.error("Matrícula já cadastrada")
                    else:
                        new_row = pd.DataFrame([{
                            "matricula": mat_str,
                            "nome": nome.strip(),
                            "turma": turma.strip()
                        }])
                        df_concat = pd.concat([df_atual, new_row], ignore_index=True)
                        df_concat.to_csv(CSV_PATH, index=False)
                        st.success("Aluno adicionado com sucesso")

                        # Forçar o rerun imediato
                        if hasattr(st, "rerun"):
                            st.rerun()
                        else:
                            st.experimental_rerun()

    with st.expander("Remover Aluno"):
        with st.form(key="remove_aluno", clear_on_submit=True):
            options   = df["matricula"] + " - " + df["nome"]
            to_remove = st.selectbox("Selecione o aluno", options)
            if st.form_submit_button("Remover"):
                mat = to_remove.split(" - ")[0]

                df_atual = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
                df_atual = df_atual.astype(str).apply(lambda col: col.str.strip())
                df2 = df_atual[df_atual["matricula"] != mat]
                df2.to_csv(CSV_PATH, index=False)
                st.success("Aluno removido com sucesso")
                st.rerun()
