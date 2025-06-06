import streamlit as st
import pandas as pd
import os

CSV_DIR = "data"
ALUNOS_CSV_PATH = os.path.join(CSV_DIR, "alunos.csv")
TURMAS_CSV_PATH = os.path.join(CSV_DIR, "turmas.csv")
DISCIPLINAS_CSV_PATH = os.path.join(CSV_DIR, "disciplinas.csv")
NOTAS_CSV_PATH = os.path.join(CSV_DIR, "notas.csv")

def _ensure_notas_csv():
    os.makedirs(CSV_DIR, exist_ok=True)
    header = ["nome", "turma", "disciplina", "nota"]
    if not os.path.exists(NOTAS_CSV_PATH) or os.path.getsize(NOTAS_CSV_PATH) == 0:
        pd.DataFrame(columns=header).to_csv(NOTAS_CSV_PATH, index=False)

def show_notas_por_turma():
    _ensure_notas_csv()

    alunos_df = pd.read_csv(ALUNOS_CSV_PATH, dtype=str, keep_default_na=False)
    turmas_df = pd.read_csv(TURMAS_CSV_PATH, dtype=str, keep_default_na=False)
    disciplinas_df = pd.read_csv(DISCIPLINAS_CSV_PATH, dtype=str, keep_default_na=False)

    alunos_df = alunos_df.apply(lambda col: col.str.strip())
    turmas_df = turmas_df.apply(lambda col: col.str.strip())
    disciplinas_df = disciplinas_df.apply(lambda col: col.str.strip())

    turmas = turmas_df["turma"].dropna().unique().tolist()
    disciplinas = disciplinas_df["nome_disciplina"].dropna().unique().tolist()

    st.title("Notas por Turma")
    st.subheader("📝 Lista de Notas")

    notas_df = pd.read_csv(NOTAS_CSV_PATH, dtype=str, keep_default_na=False)
    notas_df = notas_df.apply(lambda col: col.str.strip())
    st.dataframe(notas_df)

    with st.expander("Adicionar/Atualizar Nota"):
        with st.form(key="add_nota", clear_on_submit=True):
            turma_selecionada = st.selectbox("Selecione a Turma", options=["Selecione..."] + turmas)
            nome_aluno = st.selectbox("Selecione o Aluno", options=["Selecione..."] + alunos_df["nome"].dropna().unique().tolist())
            disciplina_selecionada = st.selectbox("Selecione a Disciplina", options=["Selecione..."] + disciplinas)
            nota_input = st.text_input("Nota")

            if st.form_submit_button("Salvar"):
                if (
                    turma_selecionada == "Selecione..." or
                    nome_aluno == "Selecione..." or
                    disciplina_selecionada == "Selecione..." or
                    not nota_input.strip()
                ):
                    st.error("Preencha todos os campos corretamente")
                else:
                    df_atual = pd.read_csv(NOTAS_CSV_PATH, dtype=str, keep_default_na=False)
                    df_atual = df_atual.apply(lambda col: col.str.strip())

                    mask = (
                        (df_atual["nome"] == nome_aluno) &
                        (df_atual["turma"] == turma_selecionada) &
                        (df_atual["disciplina"] == disciplina_selecionada)
                    )

                    if mask.any():
                        df_atual.loc[mask, "nota"] = nota_input.strip()
                    else:
                        new_row = pd.DataFrame([{
                            "nome": nome_aluno,
                            "turma": turma_selecionada,
                            "disciplina": disciplina_selecionada,
                            "nota": nota_input.strip()
                        }])
                        df_atual = pd.concat([df_atual, new_row], ignore_index=True)

                    df_atual.to_csv(NOTAS_CSV_PATH, index=False)
                    st.success("Nota salva com sucesso")
                    st.rerun()

    with st.expander("Remover Nota"):
        with st.form(key="remove_nota", clear_on_submit=True):
            options_remover = notas_df["nome"] + " | " + notas_df["turma"] + " | " + notas_df["disciplina"]
            to_remove = st.selectbox("Selecione a nota para remover", options_remover.tolist())

            if st.form_submit_button("Remover"):
                parts = to_remove.split(" | ")
                nome = parts[0]
                turma_sel = parts[1]
                disc = parts[2]

                df_atual = pd.read_csv(NOTAS_CSV_PATH, dtype=str, keep_default_na=False)
                df_atual = df_atual.apply(lambda col: col.str.strip())
                df2 = df_atual[~(
                    (df_atual["nome"] == nome) &
                    (df_atual["turma"] == turma_sel) &
                    (df_atual["disciplina"] == disc)
                )]
                df2.to_csv(NOTAS_CSV_PATH, index=False)
                st.success("Nota removida com sucesso")
                st.rerun()
