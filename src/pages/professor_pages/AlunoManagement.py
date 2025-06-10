from pathlib import Path
import time

import pandas as pd
import streamlit as st


DATA_DIR = Path('data')
alunos_csv = DATA_DIR / 'alunos.csv'

CSV_HEADER = ['user_id','matricula','nome','turma']


def ensure_csv():
    DATA_DIR.mkdir(exist_ok=True)
    if not alunos_csv.exists() or alunos_csv.stat().st_size == 0:
        pd.DataFrame(columns=CSV_HEADER).to_csv(alunos_csv,index=False)


def load_alunos():
    ensure_csv()
    df = pd.read_csv(alunos_csv, dtype=str, keep_default_na=False)
    return df.map(lambda x: x.strip())


def save_alunos(df):
    df.to_csv(alunos_csv,index=False)


def show_aluno_management():
    df = load_alunos()

    if st.button('🔙 Voltar'):
        st.session_state.current_page = 'ProfessorHome'
        st.rerun()

    st.title('👥 Gerenciar Alunos')
    st.subheader('Lista de Alunos')
    st.dataframe(df)

    with st.expander('Adicionar Aluno'):
        with st.form('add_aluno',clear_on_submit=True):
            nome = st.text_input('Nome Completo').strip()
            matricula = st.text_input('Matrícula').strip()

            if df.empty:
                next_id = 1
            else:
                nums = pd.to_numeric(df.user_id,errors='coerce').fillna(0).astype(int)
                next_id = nums.max() + 1
            user_id = str(next_id).zfill(3)
            st.text_input('User ID (autogerado)',value=user_id,disabled=True)

            if st.form_submit_button('Adicionar'):
                if not nome or not matricula:
                    st.error('Preencha todos os campos.')
                elif matricula in df.matricula.tolist():
                    st.error('Matrícula já existe.')
                else:
                    new_row = pd.DataFrame([{
                        'user_id': user_id,
                        'matricula': matricula,
                        'nome': nome,
                        'turma': df.turma.iloc[0] if not df.turma.empty else ''
                    }])
                    df_new = pd.concat([df,new_row],ignore_index=True)
                    save_alunos(df_new)
                    st.success(f'Aluno {nome} ({user_id}) adicionado.')
                    time.sleep(1.5)
                    st.rerun()

    with st.expander('Remover Aluno'):
        with st.form('remove_aluno',clear_on_submit=True):
            opts = df.user_id + ' - ' + df.nome
            sel = st.selectbox('Selecione o aluno',opts.tolist())
            confirm = st.checkbox('Confirmar remoção')
            if st.form_submit_button('Remover'):
                if confirm:
                    uid = sel.split(' - ')[0]
                    df2 = df[df.user_id != uid]
                    save_alunos(df2)
                    st.success(f'Aluno {sel} removido.')
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.warning('Para confirmar a remoção, marque a caixa de seleção.')