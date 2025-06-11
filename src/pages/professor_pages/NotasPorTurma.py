from pathlib import Path
import time

import pandas as pd
import streamlit as st


DATA_DIR = Path('data')
NOTAS_CSV = DATA_DIR / 'notas.csv'
ALUNOS_CSV = DATA_DIR / 'alunos.csv'
TURMAS_CSV = DATA_DIR / 'turmas.csv'
DISCIPLINAS_CSV = DATA_DIR / 'disciplinas.csv'

NOTAS_HEADER = ['id','matricula','codigo','nota']


def ensure_csv(path, header):
    DATA_DIR.mkdir(exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        pd.DataFrame(columns=header).to_csv(path, index=False)
    else:
        cols = pd.read_csv(path, nrows=0).columns.tolist()
        if set(cols) != set(header):
            pd.DataFrame(columns=header).to_csv(path, index=False)


def load_notas():
    ensure_csv(NOTAS_CSV, NOTAS_HEADER)
    df = pd.read_csv(NOTAS_CSV, dtype=str, keep_default_na=False)
    return df.apply(lambda col: col.str.strip())


def save_notas(df):
    df.to_csv(NOTAS_CSV, index=False)


def show_notas_por_turma():
    df_notas = load_notas()
    df_alunos = pd.read_csv(ALUNOS_CSV, dtype=str, keep_default_na=False).apply(lambda c: c.str.strip())
    df_turmas = pd.read_csv(TURMAS_CSV, dtype=str, keep_default_na=False).apply(lambda c: c.str.strip())
    df_disc = pd.read_csv(DISCIPLINAS_CSV, dtype=str, keep_default_na=False).apply(lambda c: c.str.strip())

    if st.button('🔙 Voltar'):
        st.session_state.current_page = 'ProfessorHome'
        st.rerun()

    st.title('📝 Notas por Turma')
    st.subheader('Lista de Notas')

    disp = (
        df_notas
        .merge(df_alunos[['matricula','nome','turma']], on='matricula', how='left')
        .merge(df_disc, on='codigo', how='left')
    )
    st.dataframe(disp[['id','matricula','nome','turma','codigo','nome_disciplina','nota']], use_container_width=True)

    with st.expander('Adicionar/Atualizar Nota'):
        with st.form('form_nota', clear_on_submit=True):
            turma_opts = df_turmas['turma'].tolist()
            aluno_opts = df_alunos.apply(lambda r: f"{r.matricula} – {r.nome}", axis=1).tolist()
            disc_opts = df_disc.apply(lambda r: f"{r.codigo} – {r.nome_disciplina}", axis=1).tolist()

            turma_sel = st.selectbox('Turma', ['Selecione...'] + turma_opts)
            aluno_sel = st.selectbox('Aluno', ['Selecione...'] + aluno_opts)
            disc_sel = st.selectbox('Disciplina', ['Selecione...'] + disc_opts)
            nota_in = st.text_input('Nota').strip()

            if st.form_submit_button('Salvar'):
                if turma_sel == 'Selecione...' or aluno_sel == 'Selecione...' or disc_sel == 'Selecione...' or not nota_in:
                    st.error('Preencha todos os campos')
                else:
                    matricula = aluno_sel.split(' – ')[0]
                    codigo = disc_sel.split(' – ')[0]
                    next_id = df_notas['id'].astype(int).max() + 1 if not df_notas.empty else 1
                    next_id = str(next_id).zfill(3)

                    mask = (df_notas['matricula'] == matricula) & (df_notas['codigo'] == codigo)
                    if mask.any():
                        df_notas.loc[mask, 'nota'] = nota_in
                    else:
                        new = pd.DataFrame([{
                            'id': next_id,
                            'matricula': matricula,
                            'codigo': codigo,
                            'nota': nota_in
                        }])
                        df_notas = pd.concat([df_notas, new], ignore_index=True)

                    save_notas(df_notas)
                    st.success('Nota salva com sucesso')
                    time.sleep(1.5)
                    st.rerun()

    with st.expander('Remover Nota'):
        with st.form('form_remove', clear_on_submit=True):
            opts = disp.apply(lambda r: f"{r.id} – {r.matricula} – {r.nome_disciplina}", axis=1).tolist()
            sel  = st.selectbox('Selecione nota', ['Selecione...'] + opts)
            confirm = st.checkbox('Confirmar remoção')
            if st.form_submit_button('Remover'):
                if sel == 'Selecione...':
                    st.info('Selecione uma nota válida')
                elif not confirm:
                    st.warning('Para confirmar a remoção, marque a caixa de seleção.')
                else:
                    note_id = sel.split(' – ')[0]
                    df_notas = df_notas[df_notas['id'] != note_id]
                    save_notas(df_notas)
                    st.success('Nota removida com sucesso')
                    time.sleep(1.5)
                    st.rerun()