from pathlib import Path

import pandas as pd
import streamlit as st

from src.pages.InfoPage import show_info
from src.utils.Auth import logout


DATA_DIR = Path("data")
USERS_CSV = DATA_DIR / "users.csv"
ALUNOS_CSV = DATA_DIR / "alunos.csv"
NOTAS_CSV = DATA_DIR / "notas.csv"
DISCIPLINAS_CSV = DATA_DIR / "disciplinas.csv"

USERS_HEADER = ["id","username","password","user_type","name"]
ALUNOS_HEADER = ["user_id","matricula","nome","turma"]
NOTAS_HEADER = ["id","matricula","codigo","nota"]
DISCIPLINAS_HEADER = ["codigo","nome_disciplina"]


def ensure_csv(path: Path, header: list):
    DATA_DIR.mkdir(exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        pd.DataFrame(columns=header).to_csv(path, index=False)


def load_df(path: Path, header: list) -> pd.DataFrame:
    ensure_csv(path, header)
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    return df.apply(lambda col: col.str.strip())


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
        st.session_state.clear()
        st.cache_data.clear()
        logout()

    if st.session_state.current_page == 'AlunoHome':
        users = load_df(USERS_CSV, USERS_HEADER)
        alunos = load_df(ALUNOS_CSV, ALUNOS_HEADER)
        notas = load_df(NOTAS_CSV, NOTAS_HEADER)
        disciplinas = load_df(DISCIPLINAS_CSV, DISCIPLINAS_HEADER)

        username = st.session_state.current_user
        user_row = users[users.name == username]
        if user_row.empty:
            st.error('Usuário não encontrado.')
            return

        user_id = user_row.iloc[0]['id']
        full_name = user_row.iloc[0]['name']

        st.title('Área do Aluno')
        st.write(f"Olá, **{full_name}**!")
        st.write('---')

        aluno_row = alunos[alunos.matricula == user_id]
        professor_row = users[users.id == '001']
        if not aluno_row.empty:
            st.markdown(f"""
                        <h3>Professor(a) de Estrutura de Dados I: <strong style="color:#2D9FE5">{professor_row.iloc[0]['name']}</strong></h3>
                        <h3>Matrícula: <strong style="color:#2D9FE5">{aluno_row.iloc[0]['matricula']}</strong></h3>
                        <h3>Turma: <strong style="color:#2D9FE5">{aluno_row.iloc[0]['turma']}</strong></h3>
                """, unsafe_allow_html=True)
        else:
            st.info('Dados de matrícula não encontrados.')

        st.write('---')
        st.subheader('Minhas Disciplinas e Notas')

        minhas = notas[notas.matricula == user_id]
        if not minhas.empty:
            df = minhas.merge(disciplinas, on='codigo', how='left')
            df = df[['nome_disciplina','nota']].rename(
                columns={'nome_disciplina':'Disciplina','nota':'Nota'}
            )
            st.dataframe(df, use_container_width=True)
        else:
            st.info('Nenhuma nota registrada.')

        st.write('---')
        st.caption('Sistema de Gerenciamento de Notas Escolares • Versão Acadêmica')
    elif st.session_state.current_page == 'InfoPage':
        show_info()