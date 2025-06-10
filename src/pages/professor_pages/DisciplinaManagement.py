from pathlib import Path
import time

import pandas as pd
import streamlit as st


DATA_DIR = Path('data')
DISCIPLINAS_CSV = DATA_DIR / 'disciplinas.csv'
HEADER = ['codigo','nome_disciplina']


def ensure_csv():
    DATA_DIR.mkdir(exist_ok=True)
    if not DISCIPLINAS_CSV.exists() or DISCIPLINAS_CSV.stat().st_size == 0:
        pd.DataFrame(columns=HEADER).to_csv(DISCIPLINAS_CSV,index=False)
    else:
        cols = pd.read_csv(DISCIPLINAS_CSV,nrows=0).columns.tolist()
        if set(cols)!=set(HEADER):
            pd.DataFrame(columns=HEADER).to_csv(DISCIPLINAS_CSV,index=False)


def load_disciplinas():
    ensure_csv()
    df = pd.read_csv(DISCIPLINAS_CSV,dtype=str,keep_default_na=False)
    return df.map(lambda x: x.strip())


def save_disciplinas(df: pd.DataFrame):
    df.to_csv(DISCIPLINAS_CSV,index=False)


def show_disciplina_management():
    df = load_disciplinas()

    if st.button('🔙 Voltar'):
        st.session_state.current_page = 'ProfessorHome'
        st.rerun()

    st.title('📚 Gerenciar Disciplinas')
    st.subheader('Lista de Disciplinas')
    st.dataframe(df)

    with st.expander('Adicionar Disciplina'):
        with st.form('add_disciplina',clear_on_submit=True):
            codigo = st.text_input('Código').strip()
            nome = st.text_input('Disciplina').strip()
            if st.form_submit_button('Adicionar'):
                if not codigo or not nome:
                    st.error('Preencha todos os campos')
                elif codigo in df['codigo'].tolist():
                    st.error('Código já cadastrado')
                else:
                    row = pd.DataFrame([{'codigo':codigo,'nome_disciplina':nome}])
                    updated = pd.concat([df,row],ignore_index=True)
                    save_disciplinas(updated)
                    st.success('Disciplina adicionada com sucesso')
                    time.sleep(1.5)
                    st.rerun()

    with st.expander('Remover Disciplina'):
        with st.form('remove_disciplina',clear_on_submit=True):
            options = df['codigo'] + ' – ' + df['nome_disciplina']
            sel = st.selectbox('Selecione',options.tolist())
            confirm = st.checkbox('Confirmar remoção')
            if st.form_submit_button('Remover'):
                if confirm:
                    code = sel.split(' – ')[0]
                    df2 = df[df['codigo']!=code]
                    save_disciplinas(df2)
                    st.success('Disciplina removida com sucesso')
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.warning('Para confirmar a remoção, marque a caixa de seleção.')