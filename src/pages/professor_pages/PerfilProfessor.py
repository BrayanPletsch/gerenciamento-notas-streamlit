from pathlib import Path

import pandas as pd
import streamlit as st


DATA_DIR = Path("data")
TURMAS_CSV = DATA_DIR / "turmas.csv"
DISCIPLINAS_CSV = DATA_DIR / "disciplinas.csv"

HEADER_TURMAS = ["turma", "descricao"]
HEADER_DISC = ["codigo", "nome_disciplina"]


def ensure_csv(path: Path, header: list):
    DATA_DIR.mkdir(exist_ok=True)
    if not path.exists() or path.stat().st_size == 0:
        pd.DataFrame(columns=header).to_csv(path, index=False)


def load_column(path: Path, header: list, column: str) -> list:
    ensure_csv(path, header)
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    return df[column].str.strip().tolist()


def show_meu_perfil():
    user = st.session_state.get("current_user", "Desconhecido")
    st.markdown("""
        <h1 style='color:#facc15; text-align: center;'>👨‍🏫 Meu Perfil</h1>
        <p><strong>Nome do Professor:</strong> {}</p>
    """.format(user), unsafe_allow_html=True)

    turmas = load_column(TURMAS_CSV, HEADER_TURMAS, "turma")
    disciplinas = load_column(DISCIPLINAS_CSV, HEADER_DISC, "nome_disciplina")

    if turmas or disciplinas:
        st.markdown("---")
        st.markdown("### 📚 Turmas e Disciplinas Disponíveis em seu Perfil")
        items = ([{"type":"Turma","value":t,"color":"#facc15"} for t in turmas]
                 + [{"type":"Disciplina","value":d,"color":"#3b82f6"} for d in disciplinas])
        cols = st.columns(min(len(items), 4))
        for idx,item in enumerate(items):
            with cols[idx % len(cols)]:
                st.markdown(f"""
                    <div style="background-color:#1e293b; padding:16px; border-radius:10px; margin:8px 0; text-align:center;">
                        <h4 style="color:{item['color']}; margin:5px 0;">{item['type']}</h4>
                        <p style="color:white; margin:0;">{item['value']}</p>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhuma turma ou disciplina disponível.")