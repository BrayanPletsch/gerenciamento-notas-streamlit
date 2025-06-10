from pathlib import Path
import time

import pandas as pd
import streamlit as st


DATA_DIR = Path('data')
alunos_csv = DATA_DIR / 'alunos.csv'
turmas_csv = DATA_DIR / 'turmas.csv'

ALUNOS_HEADER = ['user_id','matricula','nome','turma']
TURMAS_HEADER = ['turma']


def ensure_csvs():
    DATA_DIR.mkdir(exist_ok=True)
    if not alunos_csv.exists() or alunos_csv.stat().st_size == 0:
        pd.DataFrame(columns=ALUNOS_HEADER).to_csv(alunos_csv,index=False)
    if not turmas_csv.exists() or turmas_csv.stat().st_size == 0:
        pd.DataFrame(columns=TURMAS_HEADER).to_csv(turmas_csv,index=False)


def load_alunos():
    ensure_csvs()
    df = pd.read_csv(alunos_csv,dtype=str,keep_default_na=False)
    return df.map(lambda x: x.strip())


def load_turmas():
    ensure_csvs()
    df = pd.read_csv(turmas_csv,dtype=str,keep_default_na=False)
    return df['turma'].str.strip().tolist()


def save_alunos(df):
    df.to_csv(alunos_csv,index=False)


def show_aluno_management():
    df_alunos = load_alunos()
    turmas = load_turmas()

    if st.button('🔙 Voltar'):
        st.session_state.current_page = 'ProfessorHome'
        st.rerun()

    st.title('👥 Gerenciar Alunos')
    st.subheader('Lista de Alunos')
    st.dataframe(df_alunos)

    with st.expander('Adicionar Aluno'):
        with st.form('add_aluno',clear_on_submit=True):
            nome = st.text_input('Nome Completo').strip()
            matricula = st.text_input('Matrícula').strip()
            turma = st.selectbox('Turma',['Selecione...']+turmas)

            if df_alunos.empty:
                next_id = 1
            else:
                nums = pd.to_numeric(df_alunos.user_id,errors='coerce').fillna(0).astype(int)
                next_id = nums.max()+1
            user_id = str(next_id).zfill(3)

            if st.form_submit_button('Adicionar'):
                if not nome or not matricula or turma=='Selecione...':
                    st.error('Preencha todos os campos.')
                elif matricula in df_alunos.matricula.tolist():
                    st.error('Matrícula já existe.')
                else:
                    new_row = pd.DataFrame([{
                        'user_id':user_id,
                        'matricula':matricula,
                        'nome':nome,
                        'turma':turma
                    }])
                    df_new = pd.concat([df_alunos,new_row],ignore_index=True)
                    save_alunos(df_new)
                    st.success(f'Aluno {nome} ({user_id}) adicionado com sucesso.')
                    time.sleep(1.5)
                    st.rerun()

    with st.expander('Remover Aluno'):
        with st.form('remove_aluno',clear_on_submit=True):
            opts = df_alunos.user_id + ' - ' + df_alunos.nome
            sel = st.selectbox('Selecione o aluno',opts.tolist())
            confirm = st.checkbox('Confirmar remoção')
            if st.form_submit_button('Remover'):
                if not confirm:
                    st.warning('Para confirmar a remoção, marque a caixa de seleção.')
                else:
                    uid = sel.split(' - ')[0]
                    df2 = df_alunos[df_alunos.user_id!=uid]
                    save_alunos(df2)
                    st.success(f'Aluno {sel} removido com sucesso.')
                    time.sleep(1.5)
                    st.rerun()