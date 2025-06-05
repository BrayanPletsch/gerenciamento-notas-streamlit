import streamlit as st
import pandas as pd
import os

CSV_DIR   = "data"
CSV_PATH  = os.path.join(CSV_DIR, "notas.csv")

def _ensure_notas_csv():
    os.makedirs(CSV_DIR, exist_ok=True)
    header = ["matricula", "turma", "disciplina", "nota"]
    if (not os.path.exists(CSV_PATH)) or (os.path.getsize(CSV_PATH) == 0):
        pd.DataFrame(columns=header).to_csv(CSV_PATH, index=False)
        return
    try:
        df0 = pd.read_csv(CSV_PATH, nrows=0)
        if set(df0.columns) != set(header):
            raise ValueError
    except Exception:
        pd.DataFrame(columns=header).to_csv(CSV_PATH, index=False)

def show_notas_por_turma():
    _ensure_notas_csv()

    df = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
    df = df.astype(str).apply(lambda col: col.str.strip())
    st.title("Notas por Turma")
    st.subheader("Lista de Notas")
    st.dataframe(df)

    with st.expander("Adicionar/Atualizar Nota"):
        with st.form(key="add_nota", clear_on_submit=True):
            matricula  = st.text_input("Matrícula do Aluno")
            turma       = st.text_input("Turma")
            disciplina = st.text_input("Disciplina")
            nota        = st.text_input("Nota")
            if st.form_submit_button("Salvar"):
                mat_str  = matricula.strip()
                turma_str = turma.strip()
                disc_str = disciplina.strip()
                nota_str = nota.strip()
                if (not mat_str) or (not turma_str) or (not disc_str) or (not nota_str):
                    st.error("Preencha todos os campos")
                else:
                    df_atual = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
                    df_atual = df_atual.astype(str).apply(lambda col: col.str.strip())
                    mask = (
                        (df_atual["matricula"] == mat_str) &
                        (df_atual["turma"] == turma_str) &
                        (df_atual["disciplina"] == disc_str)
                    )
                    if mask.any():
                        df_atual.loc[mask, "nota"] = nota_str
                    else:
                        new_row = pd.DataFrame([{
                            "matricula": mat_str,
                            "turma": turma_str,
                            "disciplina": disc_str,
                            "nota": nota_str
                        }])
                        df_atual = pd.concat([df_atual, new_row], ignore_index=True)
                    df_atual.to_csv(CSV_PATH, index=False)
                    st.success("Nota salva com sucesso")
                    st.rerun()

    with st.expander("Remover Nota"):
        with st.form(key="remove_nota", clear_on_submit=True):
            options = df["matricula"] + " | " + df["turma"] + " | " + df["disciplina"]
            to_remove = st.selectbox("Selecione a nota", options)
            if st.form_submit_button("Remover"):
                parts = to_remove.split(" | ")
                mat = parts[0]
                turma_sel = parts[1]
                disc = parts[2]
                df_atual = pd.read_csv(CSV_PATH, dtype=str, keep_default_na=False)
                df_atual = df_atual.astype(str).apply(lambda col: col.str.strip())
                df2 = df_atual[~(
                    (df_atual["matricula"] == mat) &
                    (df_atual["turma"] == turma_sel) &
                    (df_atual["disciplina"] == disc)
                )]
                df2.to_csv(CSV_PATH, index=False)
                st.success("Nota removida com sucesso")
                st.rerun()
