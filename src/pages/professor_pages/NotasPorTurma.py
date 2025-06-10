from pathlib import Path
import time

import pandas as pd
import streamlit as st


DATA_DIR = Path('data')
NOTAS_CSV = DATA_DIR / 'notas.csv'
NOTAS_HEADER = ['id','matricula','nome','turma','codigo','nome_disciplina','nota']


def ensure_notas_csv():
    DATA_DIR.mkdir(exist_ok=True)
    if not NOTAS_CSV.exists() or NOTAS_CSV.stat().st_size == 0:
        pd.DataFrame(columns=NOTAS_HEADER).to_csv(NOTAS_CSV, index=False)
    else:
        cols = pd.read_csv(NOTAS_CSV, nrows=0).columns.tolist()
        if set(cols) != set(NOTAS_HEADER):
            pd.DataFrame(columns=NOTAS_HEADER).to_csv(NOTAS_CSV, index=False)


def load_notas():
    ensure_notas_csv()
    df = pd.read_csv(NOTAS_CSV, dtype=str, keep_default_na=False)
    return df.map(lambda x: x.strip())


def save_notas(df):
    df.to_csv(NOTAS_CSV, index=False)


def show_notas_por_turma():
    notas = load_notas()

    if st.button('🔙 Voltar'):
        st.session_state.current_page = 'ProfessorHome'
        st.rerun()

    st.title('📝 Notas por Turma')
    st.subheader('Lista de Notas')
    st.dataframe(notas)

    with st.expander('Adicionar / Atualizar Nota'):
        with st.form('form_nota', clear_on_submit=True):
            turmas = notas['turma'].dropna().unique().tolist()
            alunos = notas.apply(lambda r: f'{r.matricula} – {r.nome}', axis=1).unique().tolist()
            disciplinas = notas.apply(lambda r: f'{r.codigo} – {r.nome_disciplina}', axis=1).unique().tolist()

            turma_sel = st.selectbox('Turma', ['Selecione...'] + turmas)
            aluno_sel = st.selectbox('Aluno', ['Selecione...'] + alunos)
            disc_sel = st.selectbox('Disciplina', ['Selecione...'] + disciplinas)
            nota_in = st.text_input('Nota').strip()

            if st.form_submit_button('Salvar'):
                if turma_sel == 'Selecione...' or aluno_sel == 'Selecione...' or disc_sel == 'Selecione...' or not nota_in:
                    st.error('Preencha todos os campos')
                else:
                    matricula = aluno_sel.split(' – ')[0]
                    codigo = disc_sel.split(' – ')[0]
                    nome = aluno_sel.split(' – ')[1]
                    turma = turma_sel
                    nome_disc = disc_sel.split(' – ')[1]

                    next_id = (
                        str(int(notas.id.astype(int).max()) + 1).zfill(3)
                        if not notas.empty else '001'
                    )

                    mask = (notas['matricula'] == matricula) & (notas['codigo'] == codigo)
                    if mask.any():
                        notas.loc[mask, 'nota'] = nota_in
                    else:
                        new = pd.DataFrame([{
                            'id': next_id,
                            'matricula': matricula,
                            'nome': nome,
                            'turma': turma,
                            'codigo': codigo,
                            'nome_disciplina': nome_disc,
                            'nota': nota_in
                        }])
                        notas = pd.concat([notas, new], ignore_index=True)

                    save_notas(notas)
                    st.success('Nota salva com sucesso')
                    time.sleep(1.5)
                    st.rerun()

    with st.expander('Remover Nota'):
        with st.form('form_remove', clear_on_submit=True):
            opts = notas.apply(lambda r: f'{r.id} – {r.matricula} – {r.nome_disciplina}', axis=1).tolist()
            sel = st.selectbox('Selecione nota', ['Selecione...'] + opts)
            confirm = st.checkbox('Confirmar remoção')
            if st.form_submit_button('Remover'):
                if sel == 'Selecione...':
                    st.info('Selecione uma nota válida')
                elif not confirm:
                    st.warning('Para confirmar a remoção, marque a caixa de seleção.')
                else:
                    note_id = sel.split(' – ')[0]
                    notas = notas[notas.id != note_id]
                    save_notas(notas)
                    st.success('Nota removida com sucesso')
                    time.sleep(1.5)
                    st.rerun()