from pathlib import Path

import pandas as pd
import streamlit as st

from src.pages.InfoPage import show_info
from src.utils.Auth import logout


DATA_DIR = Path('data')
USERS_CSV = DATA_DIR / 'users.csv'
ALUNOS_CSV = DATA_DIR / 'alunos.csv'
NOTAS_CSV = DATA_DIR / 'notas.csv'

USERS_HEADER = ['id','username','password','user_type','name']
ALUNOS_HEADER = ['user_id','matricula','nome','turma']
NOTAS_HEADER = ['id','user_id','nome','matricula','codigo','nome_disciplina','nota']


def load_df(path: Path, header: list) -> pd.DataFrame:
    path.parent.mkdir(exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=header)
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    return df.map(lambda x: x.strip())


def show_aluno_home():
    st.set_page_config(page_title='Área do Aluno', page_icon='🎓', layout='wide')
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'AlunoHome'

    st.sidebar.title(f"Bem-vindo, {st.session_state.current_user}!")
    st.sidebar.divider()
    if st.sidebar.button('Home', use_container_width=True):
        st.session_state.current_page = 'AlunoHome'
    if st.sidebar.button('Informações do Projeto', use_container_width=True):
        st.session_state.current_page = 'InfoPage'
    st.sidebar.divider()
    if st.sidebar.button('Sair', use_container_width=True):
        logout()

    if st.session_state.current_page == 'AlunoHome':
        users = load_df(USERS_CSV, USERS_HEADER)
        alunos = load_df(ALUNOS_CSV, ALUNOS_HEADER)
        notas  = load_df(NOTAS_CSV, NOTAS_HEADER)

        username = st.session_state.current_user
        user = users[users.name == username]
        if user.empty:
            st.error('Usuário não encontrado.')
            return

        user_id = user.iloc[0]['id']
        full_name = user.iloc[0]['name']

        st.title('Área do Aluno')
        st.write(f"Olá, **{full_name}**!")
        st.write('---')

        aluno = alunos[alunos.matricula == user_id]
        if not aluno.empty:
            turma = aluno.iloc[0]['turma']
            st.subheader(f"Turma: {turma}")
        else:
            st.info('Dados de matrícula não encontrados.')

        st.write('---')
        st.subheader('Minhas Disciplinas e Notas')

        minhas = notas[notas.matricula == user_id]
        if not minhas.empty:
            df = minhas[['nome_disciplina','nota']].rename(
                columns={'nome_disciplina':'Disciplina','nota':'Nota'}
            )
            st.dataframe(df, use_container_width=True)
        else:
            st.info('Nenhuma nota registrada.')

        st.write('---')
        st.caption('Sistema de Gerenciamento de Notas Escolares  •  Versão Acadêmica')

    elif st.session_state.current_page == 'InfoPage':
        show_info()