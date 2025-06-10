from pathlib import Path
import time

import pandas as pd
import streamlit as st


DATA_DIR = Path('data')
TURMAS_CSV = DATA_DIR / 'turmas.csv'
HEADER = ['turma','descricao']


def ensure_csv():
    DATA_DIR.mkdir(exist_ok=True)
    if not TURMAS_CSV.exists() or TURMAS_CSV.stat().st_size == 0:
        pd.DataFrame(columns=HEADER).to_csv(TURMAS_CSV, index=False)
    else:
        cols = pd.read_csv(TURMAS_CSV, nrows=0).columns.tolist()
        if set(cols) != set(HEADER):
            pd.DataFrame(columns=HEADER).to_csv(TURMAS_CSV, index=False)


def load_turmas():
    ensure_csv()
    df = pd.read_csv(TURMAS_CSV, dtype=str, keep_default_na=False)
    return df.map(lambda x: x.strip())


def save_turmas(df: pd.DataFrame):
    df.to_csv(TURMAS_CSV, index=False)


def show_turma_management():
    df = load_turmas()

    if st.button('🔙 Voltar'):
        st.session_state.current_page = 'ProfessorHome'
        st.rerun()

    st.title('🏷️ Gerenciar Turmas')
    st.subheader('Lista de Turmas')
    st.dataframe(df)

    with st.expander('Adicionar Turma'):
        with st.form('add_turma', clear_on_submit=True):
            code = st.text_input('Código da Turma').strip()
            desc = st.text_input('Descrição').strip()
            if st.form_submit_button('Adicionar'):
                if not code or not desc:
                    st.error('Preencha todos os campos')
                elif code in df['turma'].tolist():
                    st.error('Turma já existe')
                else:
                    new_row = pd.DataFrame([{'turma': code, 'descricao': desc}])
                    updated = pd.concat([df, new_row], ignore_index=True)
                    save_turmas(updated)
                    st.success('Turma adicionada com sucesso')
                    time.sleep(1.5)
                    st.rerun()

    with st.expander('Remover Turma'):
        with st.form('remove_turma', clear_on_submit=True):
            choices = df['turma'] + ' – ' + df['descricao']
            sel = st.selectbox('Selecione a turma', choices.tolist())
            confirm = st.checkbox('Confirmar remoção')
            if st.form_submit_button('Remover'):
                if confirm:
                    code = sel.split(' – ')[0]
                    filtered = df[df['turma'] != code]
                    save_turmas(filtered)
                    st.success('Turma removida com sucesso')
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.warning('Para confirmar a remoção, marque a caixa de seleção.')